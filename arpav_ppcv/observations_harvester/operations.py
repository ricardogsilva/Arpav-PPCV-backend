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
from ..schemas import observations

logger = logging.getLogger(__name__)


def harvest_stations(
        client: httpx.Client, db_session: sqlmodel.Session
) -> list[observations.StationCreate]:
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
            if (raw_start := raw_station.get("iniziovalidita")):
                try:
                    active_since = dt.date(*(int(i) for i in raw_start.split("-")))
                except TypeError:
                    logger.warning(
                        f"Could not extract a valid date from the input {raw_start!r}")
                    active_since = None
            else:
                active_since = None
            if (raw_end := raw_station.get("finevalidita")):
                try:
                    active_until = dt.date(*raw_end.split("-"))
                except TypeError:
                    logger.warning(
                        f"Could not extract a valid date from the input {raw_end!r}")
                    active_until = None
            else:
                active_until = None
            if (
                    station_code not in existing_stations and
                    station_code not in stations_create
            ):
                pt_4258 = shapely.Point(
                    raw_station["EPSG4258_LON"], raw_station["EPSG4258_LAT"])
                pt_4326 = shapely.ops.transform(coord_converter, pt_4258)
                station_create = observations.StationCreate(
                    code=station_code,
                    geom=geojson_pydantic.Point(
                        type="Point",
                        coordinates=(pt_4326.x, pt_4326.y)
                    ),
                    altitude_m=raw_station["altitude"],
                    name=raw_station["statnm"],
                    type_=raw_station["stattype"].lower().replace(" ", "_"),
                    active_since=active_since,
                    active_until=active_until,
                )
                stations_create[station_create.code] = station_create
    return list(stations_create.values())


def refresh_stations(
        client: httpx.Client,
        db_session: sqlmodel.Session
) -> list[observations.Station]:
    to_create = harvest_stations(client, db_session)
    logger.info(f"About to create {len(to_create)} stations...")
    created_variables = database.create_many_stations(db_session, to_create)
    return created_variables


def harvest_monthly_measurements(
        client: httpx.Client,
        db_session: sqlmodel.Session,
        station_id: Optional[uuid.UUID] = None,
        variable_id: Optional[uuid.UUID] = None,
) -> list[observations.MonthlyMeasurementCreate]:
    existing_stations = _get_stations(db_session, station_id)
    existing_variables = _get_variables(db_session, variable_id)
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
                    measurement_id = _build_monthly_measurement_id(db_measurement)
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
                    monthly_measurement_create = observations.MonthlyMeasurementCreate(
                        station_id=station.id,
                        variable_id=variable.id,
                        value=raw_measurement["valore"],
                        date=dt.date(raw_measurement["anno"], month, 1),
                    )
                    measurement_id = _build_monthly_measurement_id(
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
) -> list[observations.MonthlyMeasurement]:
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


def harvest_seasonal_measurements(
        client: httpx.Client,
        db_session: sqlmodel.Session,
        station_id: Optional[uuid.UUID] = None,
        variable_id: Optional[uuid.UUID] = None,
) -> list[observations.SeasonalMeasurementCreate]:
    existing_stations = _get_stations(db_session, station_id)
    existing_variables = _get_variables(db_session, variable_id)
    measurements_create = []
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
            for current_season in observations.Season:
                logger.info(
                    f"\t\tProcessing season {current_season!r}...")
                existing_measurements = database.collect_all_seasonal_measurements(
                    db_session,
                    station_id_filter=station.id,
                    variable_id_filter=variable.id,
                    season_filter=current_season
                )
                existing = {}
                for db_measurement in existing_measurements:
                    measurement_id = _build_seasonal_measurement_id(db_measurement)
                    existing[measurement_id] = db_measurement

                season_query_param = {
                    observations.Season.WINTER: 1,
                    observations.Season.SPRING: 2,
                    observations.Season.SUMMER: 3,
                    observations.Season.AUTUMN: 4,
                }[current_season]
                response = client.get(
                    "https://api.arpa.veneto.it/REST/v1/clima_indicatori",
                    params={
                        "statcd": station.code,
                        "indicatore": variable.name,
                        "tabella": "S",
                        "periodo": season_query_param
                    }
                )
                response.raise_for_status()
                for raw_measurement in response.json().get("data", []):
                    measurement_create = observations.SeasonalMeasurementCreate(
                        station_id=station.id,
                        variable_id=variable.id,
                        value=raw_measurement["valore"],
                        year=int(raw_measurement["anno"]),
                        season=current_season,
                    )
                    measurement_id = _build_seasonal_measurement_id(measurement_create)
                    if measurement_id not in existing:
                        measurements_create.append(measurement_create)
    return measurements_create


def refresh_seasonal_measurements(
        client: httpx.Client,
        db_session: sqlmodel.Session,
        station_id: Optional[uuid.UUID] = None,
        variable_id: Optional[uuid.UUID] = None,
) -> list[observations.SeasonalMeasurement]:
    to_create = harvest_seasonal_measurements(
        client,
        db_session,
        station_id=station_id,
        variable_id=variable_id
    )
    logger.info(f"About to create {len(to_create)} seasonal measurements...")
    created_measurements = database.create_many_seasonal_measurements(
        db_session, to_create)
    return created_measurements


def _build_monthly_measurement_id(
        measurement: observations.MonthlyMeasurement | observations.MonthlyMeasurementCreate
) -> str:
    return (
        f"{measurement.station_id}-{measurement.variable_id}-"
        f"{measurement.date.strftime('%Y%m')}"
    )


def _build_seasonal_measurement_id(
        measurement: observations.SeasonalMeasurement | observations.SeasonalMeasurementCreate
) -> str:
    return (
        f"{measurement.station_id}-{measurement.variable_id}-"
        f"{measurement.season.value}"
    )


def _build_yearly_measurement_id(
        measurement: observations.YearlyMeasurement | observations.YearlyMeasurementCreate
) -> str:
    return (
        f"{measurement.station_id}-{measurement.variable_id}-{measurement.year}"
    )


def _get_stations(
        db_session: sqlmodel.Session,
        station_id: Optional[uuid.UUID]
) -> list[observations.Station]:
    if station_id is not None:
        result = [database.get_station(db_session, station_id)]
    else:
        result = database.collect_all_stations(db_session)
    return result


def _get_variables(
        db_session: sqlmodel.Session,
        variable_id: Optional[uuid.UUID]
) -> list[observations.Variable]:
    if variable_id is not None:
        result = [database.get_variable(db_session, variable_id)]
    else:
        result = database.collect_all_variables(db_session)
    return result


def harvest_yearly_measurements(
        client: httpx.Client,
        db_session: sqlmodel.Session,
        station_id: Optional[uuid.UUID] = None,
        variable_id: Optional[uuid.UUID] = None,
) -> list[observations.YearlyMeasurementCreate]:
    existing_stations = _get_stations(db_session, station_id)
    existing_variables = _get_variables(db_session, variable_id)
    yearly_measurements_create = []
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
            existing_measurements = database.collect_all_yearly_measurements(
                db_session,
                station_id_filter=station.id,
                variable_id_filter=variable.id,
            )
            existing = {}
            for db_measurement in existing_measurements:
                measurement_id = _build_yearly_measurement_id(db_measurement)
                existing[measurement_id] = db_measurement
            response = client.get(
                "https://api.arpa.veneto.it/REST/v1/clima_indicatori",
                params={
                    "statcd": station.code,
                    "indicatore": variable.name,
                    "tabella": "A",
                    "periodo": "0",
                }
            )
            response.raise_for_status()
            for raw_measurement in response.json().get("data", []):
                yearly_measurement_create = observations.YearlyMeasurementCreate(
                    station_id=station.id,
                    variable_id=variable.id,
                    value=raw_measurement["valore"],
                    year=int(raw_measurement["anno"]),
                )
                measurement_id = _build_yearly_measurement_id(
                    yearly_measurement_create)
                if measurement_id not in existing:
                    yearly_measurements_create.append(
                        yearly_measurement_create)
    return yearly_measurements_create


def refresh_yearly_measurements(
        client: httpx.Client,
        db_session: sqlmodel.Session,
        station_id: Optional[uuid.UUID] = None,
        variable_id: Optional[uuid.UUID] = None,
) -> list[observations.YearlyMeasurement]:
    to_create = harvest_yearly_measurements(
        client,
        db_session,
        station_id=station_id,
        variable_id=variable_id
    )
    logger.info(f"About to create {len(to_create)} yearly measurements...")
    created_measurements = database.create_many_yearly_measurements(
        db_session, to_create)
    return created_measurements
