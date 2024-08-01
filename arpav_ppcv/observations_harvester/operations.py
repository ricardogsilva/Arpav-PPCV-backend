import datetime as dt
import logging
import uuid
from collections.abc import (
    AsyncGenerator,
    Sequence,
)
from typing import (
    Callable,
    Optional,
)

import anyio
import geojson_pydantic
import httpx
import pyproj
import shapely
import shapely.ops
import sqlmodel

from .. import (
    database,
)
from ..schemas.base import Season
from ..schemas import observations

logger = logging.getLogger(__name__)


async def fetch_remote_stations(
    client: httpx.AsyncClient,
    variables: Sequence[observations.Variable],
    fetch_stations_with_months: Sequence[int],
    fetch_stations_with_seasons: Sequence[int],
    fetch_stations_with_yearly_measurements: bool,
) -> AsyncGenerator[dict, None]:
    station_url = (
        "https://api.arpa.veneto.it/REST/v1/clima_indicatori/staz_attive_lunghe"
    )
    for variable in variables:
        logger.info(
            f"Retrieving stations with monthly measurements for variable "
            f"{variable.name!r}..."
        )
        for month in fetch_stations_with_months:
            logger.info(f"Processing month {month}...")
            month_response = await client.get(
                station_url,
                params={
                    "indicatore": variable.name,
                    "tabella": "M",
                    "periodo": str(month),
                },
            )
            month_response.raise_for_status()
            for raw_station in month_response.json().get("data", []):
                yield raw_station
        for season in fetch_stations_with_seasons:
            logger.info(f"Processing season {season}...")
            season_response = await client.get(
                station_url,
                params={
                    "indicatore": variable.name,
                    "tabella": "S",
                    "periodo": str(season),
                },
            )
            season_response.raise_for_status()
            for raw_station in season_response.json().get("data", []):
                yield raw_station
        if fetch_stations_with_yearly_measurements:
            logger.info("Processing year...")
            year_response = await client.get(
                station_url,
                params={
                    "indicatore": variable.name,
                    "tabella": "A",
                    "periodo": "0",
                },
            )
            year_response.raise_for_status()
            for raw_station in year_response.json().get("data", []):
                yield raw_station


def parse_station(
    raw_station: dict, coord_converter: Callable
) -> observations.StationCreate:
    station_code = str(raw_station["statcd"])
    if raw_start := raw_station.get("iniziovalidita"):
        try:
            active_since = dt.date(*(int(i) for i in raw_start.split("-")))
        except TypeError:
            logger.warning(
                f"Could not extract a valid date from the input {raw_start!r}"
            )
            active_since = None
    else:
        active_since = None
    if raw_end := raw_station.get("finevalidita"):
        try:
            active_until = dt.date(*raw_end.split("-"))
        except TypeError:
            logger.warning(f"Could not extract a valid date from the input {raw_end!r}")
            active_until = None
    else:
        active_until = None
    pt_4258 = shapely.Point(raw_station["EPSG4258_LON"], raw_station["EPSG4258_LAT"])
    pt_4326 = shapely.ops.transform(coord_converter, pt_4258)
    return observations.StationCreate(
        code=station_code,
        geom=geojson_pydantic.Point(type="Point", coordinates=(pt_4326.x, pt_4326.y)),
        altitude_m=raw_station["altitude"],
        name=raw_station["statnm"],
        type_=raw_station.get("stattype", "").lower().replace(" ", "_"),
        active_since=active_since,
        active_until=active_until,
    )


async def harvest_stations(
    client: httpx.AsyncClient,
    variables_to_refresh: Sequence[observations.Variable],
    fetch_stations_with_months: Sequence[int],
    fetch_stations_with_seasons: Sequence[int],
    fetch_stations_with_yearly_measurements: bool,
) -> set[observations.StationCreate]:
    coord_converter = pyproj.Transformer.from_crs(
        pyproj.CRS("epsg:4258"), pyproj.CRS("epsg:4326"), always_xy=True
    ).transform
    stations = set()
    async for raw_station in fetch_remote_stations(
        client,
        variables_to_refresh,
        fetch_stations_with_months,
        fetch_stations_with_seasons,
        fetch_stations_with_yearly_measurements,
    ):
        stations.add(parse_station(raw_station, coord_converter))
    return stations


def refresh_stations(
    client: httpx.AsyncClient,
    db_session: sqlmodel.Session,
    variables_to_refresh: Sequence[observations.Variable],
    fetch_stations_with_months: Optional[Sequence[int]] = None,
    fetch_stations_with_seasons: Optional[Sequence[int]] = None,
    fetch_stations_with_yearly_measurements: bool = False,
) -> list[observations.Station]:
    months = fetch_stations_with_months or list(range(1, 13))
    seasons = fetch_stations_with_seasons or list(range(1, 5))
    stations_found_on_remote = anyio.run(
        harvest_stations,
        client,
        variables_to_refresh,
        months,
        seasons,
        fetch_stations_with_yearly_measurements,
    )
    possibly_new_stations = {s.code: s for s in stations_found_on_remote}
    existing_stations = {s.code: s for s in database.collect_all_stations(db_session)}
    to_create = []
    for possibly_new_station in possibly_new_stations.values():
        if existing_stations.get(possibly_new_station.code) is None:
            logger.info(
                f"About to create station {possibly_new_station.code} - "
                f"{possibly_new_station.name}..."
            )
            to_create.append(possibly_new_station)
        else:
            logger.debug(
                f"Station {possibly_new_station.code} - {possibly_new_station.name} "
                f"is already known"
            )
    for existing_station in existing_stations.values():
        if possibly_new_stations.get(existing_station.code) is None:
            logger.warning(
                f"Station {existing_station.code} - {existing_station.name} is not "
                f"found on the remote. Maybe it can be deleted? The system does not "
                f"delete stations so please check manually if this should be deleted "
                f"or not"
            )
    return database.create_many_stations(db_session, to_create)


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
                logger.info(f"\t\tProcessing month {month!r} ({month}/12)...")
                existing_measurements = database.collect_all_monthly_measurements(
                    db_session,
                    station_id_filter=station.id,
                    variable_id_filter=variable.id,
                    month_filter=month,
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
                        "periodo": month,
                    },
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
                        monthly_measurement_create
                    )
                    if measurement_id not in existing:
                        monthly_measurements_create.append(monthly_measurement_create)
    return monthly_measurements_create


def refresh_monthly_measurements(
    client: httpx.Client,
    db_session: sqlmodel.Session,
    station_id: Optional[uuid.UUID] = None,
    variable_id: Optional[uuid.UUID] = None,
) -> list[observations.MonthlyMeasurement]:
    to_create = harvest_monthly_measurements(
        client, db_session, station_id=station_id, variable_id=variable_id
    )
    logger.info(f"About to create {len(to_create)} monthly measurements...")
    created_monthly_measurements = database.create_many_monthly_measurements(
        db_session, to_create
    )
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
            for current_season in Season:
                logger.info(f"\t\tProcessing season {current_season!r}...")
                existing_measurements = database.collect_all_seasonal_measurements(
                    db_session,
                    station_id_filter=station.id,
                    variable_id_filter=variable.id,
                    season_filter=current_season,
                )
                existing = {}
                for db_measurement in existing_measurements:
                    measurement_id = _build_seasonal_measurement_id(db_measurement)
                    existing[measurement_id] = db_measurement

                season_query_param = {
                    Season.WINTER: 1,
                    Season.SPRING: 2,
                    Season.SUMMER: 3,
                    Season.AUTUMN: 4,
                }[current_season]
                response = client.get(
                    "https://api.arpa.veneto.it/REST/v1/clima_indicatori",
                    params={
                        "statcd": station.code,
                        "indicatore": variable.name,
                        "tabella": "S",
                        "periodo": season_query_param,
                    },
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
        client, db_session, station_id=station_id, variable_id=variable_id
    )
    logger.info(f"About to create {len(to_create)} seasonal measurements...")
    created_measurements = database.create_many_seasonal_measurements(
        db_session, to_create
    )
    return created_measurements


def _build_monthly_measurement_id(
    measurement: observations.MonthlyMeasurement
    | observations.MonthlyMeasurementCreate,
) -> str:
    return (
        f"{measurement.station_id}-{measurement.variable_id}-"
        f"{measurement.date.strftime('%Y%m')}"
    )


def _build_seasonal_measurement_id(
    measurement: observations.SeasonalMeasurement
    | observations.SeasonalMeasurementCreate,
) -> str:
    return (
        f"{measurement.station_id}-{measurement.variable_id}-"
        f"{measurement.season.value}"
    )


def _build_yearly_measurement_id(
    measurement: observations.YearlyMeasurement | observations.YearlyMeasurementCreate,
) -> str:
    return f"{measurement.station_id}-{measurement.variable_id}-{measurement.year}"


def _get_stations(
    db_session: sqlmodel.Session, station_id: Optional[uuid.UUID]
) -> list[observations.Station]:
    if station_id is not None:
        result = [database.get_station(db_session, station_id)]
    else:
        result = database.collect_all_stations(db_session)
    return result


def _get_variables(
    db_session: sqlmodel.Session, variable_id: Optional[uuid.UUID]
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
                },
            )
            response.raise_for_status()
            for raw_measurement in response.json().get("data", []):
                yearly_measurement_create = observations.YearlyMeasurementCreate(
                    station_id=station.id,
                    variable_id=variable.id,
                    value=raw_measurement["valore"],
                    year=int(raw_measurement["anno"]),
                )
                measurement_id = _build_yearly_measurement_id(yearly_measurement_create)
                if measurement_id not in existing:
                    yearly_measurements_create.append(yearly_measurement_create)
    return yearly_measurements_create


def refresh_yearly_measurements(
    client: httpx.Client,
    db_session: sqlmodel.Session,
    station_id: Optional[uuid.UUID] = None,
    variable_id: Optional[uuid.UUID] = None,
) -> list[observations.YearlyMeasurement]:
    to_create = harvest_yearly_measurements(
        client, db_session, station_id=station_id, variable_id=variable_id
    )
    logger.info(f"About to create {len(to_create)} yearly measurements...")
    created_measurements = database.create_many_yearly_measurements(
        db_session, to_create
    )
    return created_measurements
