import datetime as dt
import logging
import uuid
from typing import Optional

import geojson_pydantic
import httpx
import pyproj
import shapely
import shapely.ops
import sqlmodel

from .. import (
    database,
)
from ..schemas import models

logger = logging.getLogger(__name__)


def harvest_variables(
        client: httpx.Client,
        db_session: sqlmodel.Session
) -> tuple[
    list[models.VariableCreate],
    list[tuple[models.Variable, models.VariableUpdate]]
]:
    """
    Queries remote API and returns a tuple with variables to create and update.
    """
    existing_variables = {v.name: v for v in database.collect_all_variables(db_session)}
    response = client.get(
        "https://api.arpa.veneto.it/REST/v1/clima_indicatori/tipo_indicatore",
    )
    response.raise_for_status()
    to_create = []
    to_update = []
    for var_info in response.json().get("data", []):
        variable_create = models.VariableCreate(
            name=var_info["indicatore"],
            description=var_info["descrizione"],
            unit=var_info.get("unita", ""),
        )
        if variable_create.name not in existing_variables:
            to_create.append(variable_create)
        else:
            existing_variable = existing_variables[variable_create.name]
            if existing_variable.description != variable_create.description:
                to_update.append(
                    (
                        existing_variable,
                        models.VariableUpdate(description=variable_create.description)
                    )
                )
    return to_create, to_update


def refresh_variables(
        client: httpx.Client,
        db_session: sqlmodel.Session
) -> tuple[list[models.Variable], list[models.Variable]]:
    to_create, to_update = harvest_variables(client, db_session)
    logger.info(f"About to create {len(to_create)} variables...")
    created_variables = database.create_many_variables(db_session, to_create)
    logger.info(f"About to update {len(to_update)} variables...")
    updated_variables = []
    for db_var, var_update in to_update:
        updated = database.update_variable(db_session, db_var, var_update)
        updated_variables.append(updated)
    return created_variables, updated_variables


def harvest_stations(
        client: httpx.Client, db_session: sqlmodel.Session
) -> list[models.StationCreate]:
    existing_stations = {s.code: s for s in database.collect_all_stations(db_session)}
    stations_create = {}
    coord_converter = pyproj.Transformer.from_crs(
        pyproj.CRS("epsg:4258"),
        pyproj.CRS("epsg:4326"),
        always_xy=True
    ).transform
    existing_variables = database.collect_all_variables(db_session)
    for idx, variable in enumerate(existing_variables):
        logger.info(
            f"({idx+1}/{len(existing_variables)}) Processing stations for "
            f"variable {variable.name!r}..."
        )
        response = client.get(
            "https://api.arpa.veneto.it/REST/v1/clima_indicatori/staz_attive",
            params={"indicatore": variable.name}
        )
        response.raise_for_status()
        for raw_station in response.json().get("data", []):
            station_code = str(raw_station["statcd"])
            if (
                    station_code not in existing_stations and
                    station_code not in stations_create
            ):
                pt_4258 = shapely.Point(
                    raw_station["EPSG4258_LON"], raw_station["EPSG4258_LAT"])
                pt_4326 = shapely.ops.transform(coord_converter, pt_4258)
                station_create = models.StationCreate(
                    code=station_code,
                    geom=geojson_pydantic.Point(
                        type="Point",
                        coordinates=(pt_4326.x, pt_4326.y)
                    ),
                    altitude_m=raw_station["altitude"],
                    name=raw_station["statnm"],
                    type_=raw_station["stattype"].lower().replace(" ", "_"),
                )
                stations_create[station_create.code] = station_create
    return list(stations_create.values())


def refresh_stations(
        client: httpx.Client,
        db_session: sqlmodel.Session
) -> list[models.Station]:
    to_create = harvest_stations(client, db_session)
    logger.info(f"About to create {len(to_create)} stations...")
    created_variables = database.create_many_stations(db_session, to_create)
    return created_variables


def harvest_monthly_measurements(
        client: httpx.Client,
        db_session: sqlmodel.Session,
        station_id: Optional[uuid.UUID] = None,
        variable_id: Optional[uuid.UUID] = None,
) -> list[models.MonthlyMeasurementCreate]:
    if station_id is not None:
        existing_stations = [database.get_station(db_session, station_id)]
    else:
        existing_stations = database.collect_all_stations(db_session)
    if variable_id is not None:
        existing_variables = [database.get_variable(db_session, variable_id)]
    else:
        existing_variables = database.collect_all_variables(db_session)
    monthly_measurements_create = []
    for station_idx, station in enumerate(existing_stations):
        logger.info(
            f"Processing station {station.code!r} ({station_idx+1}/"
            f"{len(existing_stations)})..."
        )
        for var_idx, variable in enumerate(existing_variables):
            logger.info(
                f"\tProcessing variable {variable.name!r} ({var_idx+1}/"
                f"{len(existing_variables)})..."
            )
            for month in range(1, 13):
                logger.info(
                    f"\t\tProcessing month {month!r} ({month}/12)...")
                existing_measurements = database.collect_all_monthly_measurements(
                    db_session,
                    station_id_filter=station.id,
                    variable_id_filter=variable.id,
                    month_filter=month
                )
                existing = {}
                for db_measurement in existing_measurements:
                    measurement_id = _build_measurement_id(db_measurement)
                    existing[measurement_id] = db_measurement
                response = client.get(
                    "https://api.arpa.veneto.it/REST/v1/clima_indicatori",
                    params={
                        "statcd": station.code,
                        "indicatore": variable.name,
                        "tabella": "M",
                        "periodo": month
                    }
                )
                response.raise_for_status()
                for raw_measurement in response.json().get("data", []):
                    monthly_measurement_create = models.MonthlyMeasurementCreate(
                        station_id=station.id,
                        variable_id=variable.id,
                        value=raw_measurement["valore"],
                        date=dt.date(raw_measurement["anno"], month, 1),
                    )
                    measurement_id = _build_measurement_id(
                        monthly_measurement_create)
                    if measurement_id not in existing:
                        monthly_measurements_create.append(
                            monthly_measurement_create)
    return monthly_measurements_create


def refresh_monthly_measurements(
        client: httpx.Client,
        db_session: sqlmodel.Session,
        station_id: Optional[uuid.UUID] = None,
        variable_id: Optional[uuid.UUID] = None,
) -> list[models.MonthlyMeasurement]:
    to_create = harvest_monthly_measurements(
        client,
        db_session,
        station_id=station_id,
        variable_id=variable_id
    )
    logger.info(f"About to create {len(to_create)} monthly measurements...")
    created_monthly_measurements = database.create_many_monthly_measurements(
        db_session, to_create)
    return created_monthly_measurements


def _build_measurement_id(
        measurement: models.MonthlyMeasurement | models.MonthlyMeasurementCreate):
    return (
        f"{measurement.station_id}-{measurement.variable_id}-"
        f"{measurement.date.strftime('%Y%m')}"
    )
