import datetime as dt
from typing import Sequence

import httpx
import sqlmodel
import prefect
import pyproj

from arpav_ppcv import database
from arpav_ppcv.config import get_settings
from arpav_ppcv.observations_harvester import operations
from arpav_ppcv.schemas import (
    base,
    observations,
)

# this is a module global because we need to configure the prefect flow and
# task with values from it
settings = get_settings()


@prefect.task(
    retries=settings.prefect.num_task_retries,
    retry_delay_seconds=settings.prefect.task_retry_delay_seconds,
)
def harvest_stations(
    client: httpx.Client,
    variable: observations.Variable,
    fetch_stations_with_months: bool,
    fetch_stations_with_seasons: bool,
    fetch_stations_with_yearly_measurements: bool,
) -> set[observations.StationCreate]:
    coord_converter = pyproj.Transformer.from_crs(
        pyproj.CRS("epsg:4258"), pyproj.CRS("epsg:4326"), always_xy=True
    ).transform
    stations = set()
    retriever = operations.sync_fetch_remote_stations(
        client=client,
        variables=[variable],
        fetch_stations_with_months=fetch_stations_with_months,
        fetch_stations_with_seasons=fetch_stations_with_seasons,
        fetch_stations_with_yearly_measurements=fetch_stations_with_yearly_measurements,
    )
    for raw_station in retriever:
        stations.add(operations.parse_station(raw_station, coord_converter))
    return stations


@prefect.task(
    retries=settings.prefect.num_task_retries,
    retry_delay_seconds=settings.prefect.task_retry_delay_seconds,
)
def find_new_stations(
    db_stations: Sequence[observations.Station],
    new_stations: Sequence[observations.StationCreate],
) -> list[observations.StationCreate]:
    possibly_new_stations = {s.code: s for s in new_stations}
    existing_stations = {s.code: s for s in db_stations}
    to_create = []
    for possibly_new_station in possibly_new_stations.values():
        if existing_stations.get(possibly_new_station.code) is None:
            print(
                f"About to create station {possibly_new_station.code} - "
                f"{possibly_new_station.name}..."
            )
            to_create.append(possibly_new_station)
        else:
            print(
                f"Station {possibly_new_station.code} - {possibly_new_station.name} "
                f"is already known"
            )
    for existing_station in existing_stations.values():
        if possibly_new_stations.get(existing_station.code) is None:
            print(
                f"Station {existing_station.code} - {existing_station.name} is not "
                f"found on the remote. Maybe it can be deleted? The system does not "
                f"delete stations so please check manually if this should be deleted "
                f"or not"
            )
    return to_create


@prefect.flow(
    log_prints=True,
    retries=settings.prefect.num_flow_retries,
    retry_delay_seconds=settings.prefect.flow_retry_delay_seconds,
)
def refresh_stations(
    variable_name: str | None = None,
    refresh_stations_with_monthly_data: bool = True,
    refresh_stations_with_seasonal_data: bool = True,
    refresh_stations_with_yearly_data: bool = True,
):
    settings = get_settings()
    client = httpx.Client()
    with sqlmodel.Session(database.get_engine(settings)) as db_session:
        db_variables = _get_variables(db_session, variable_name)
        if len(db_variables) > 0:
            to_filter_for_new_stations = set()
            to_wait_on = []
            for variable in db_variables:
                print(
                    f"refreshing stations that have values for "
                    f"variable {variable.name!r}..."
                )
                if refresh_stations_with_monthly_data:
                    monthly_future = harvest_stations.submit(
                        client,
                        variable,
                        fetch_stations_with_months=True,
                        fetch_stations_with_seasons=False,
                        fetch_stations_with_yearly_measurements=False,
                    )
                    to_wait_on.append(monthly_future)
                if refresh_stations_with_seasonal_data:
                    seasonal_future = harvest_stations.submit(
                        client,
                        variable,
                        fetch_stations_with_months=False,
                        fetch_stations_with_seasons=True,
                        fetch_stations_with_yearly_measurements=False,
                    )
                    to_wait_on.append(seasonal_future)
                if refresh_stations_with_yearly_data:
                    yearly_future = harvest_stations.submit(
                        client,
                        variable,
                        fetch_stations_with_months=False,
                        fetch_stations_with_seasons=False,
                        fetch_stations_with_yearly_measurements=True,
                    )
                    to_wait_on.append(yearly_future)
            for future in to_wait_on:
                to_filter_for_new_stations.update(future.result())
            to_create = find_new_stations(
                database.collect_all_stations(db_session),
                list(to_filter_for_new_stations),
            )
            if len(to_create) > 0:
                print(f"Found {len(to_create)} new stations. Creating them now...")
                for s in to_create:
                    print(f"- ({s.code}) {s.name}")
                database.create_many_stations(db_session, to_create)
            else:
                print("No new stations found.")
        else:
            print("There are no variables to process, skipping...")


@prefect.task(
    retries=settings.prefect.num_task_retries,
    retry_delay_seconds=settings.prefect.task_retry_delay_seconds,
)
def harvest_monthly_measurements(
    client: httpx.Client,
    db_session: sqlmodel.Session,
    station: observations.Station,
    variable: observations.Variable,
    month: int,
) -> list[observations.MonthlyMeasurementCreate]:
    existing_measurements = database.collect_all_monthly_measurements(
        db_session,
        station_id_filter=station.id,
        variable_id_filter=variable.id,
        month_filter=month,
    )
    existing = {}
    for db_measurement in existing_measurements:
        measurement_id = operations.build_monthly_measurement_id(db_measurement)
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
    to_create = []
    for raw_measurement in response.json().get("data", []):
        measurement_create = observations.MonthlyMeasurementCreate(
            station_id=station.id,
            variable_id=variable.id,
            value=raw_measurement["valore"],
            date=dt.date(raw_measurement["anno"], month, 1),
        )
        measurement_id = operations.build_monthly_measurement_id(measurement_create)
        if measurement_id not in existing:
            to_create.append(measurement_create)
    return to_create


@prefect.flow(
    log_prints=True,
    retries=settings.prefect.num_flow_retries,
    retry_delay_seconds=settings.prefect.flow_retry_delay_seconds,
)
def refresh_monthly_measurements(
    station_code: str | None = None,
    variable_name: str | None = None,
    month: int | None = None,
):
    settings = get_settings()
    client = httpx.Client()
    with sqlmodel.Session(database.get_engine(settings)) as db_session:
        db_variables = _get_variables(db_session, variable_name)
        if len(db_variables) > 0:
            db_stations = _get_stations(db_session, station_code)
            if len(db_stations) > 0:
                for db_station in db_stations:
                    to_create = []
                    to_wait_for = []
                    print(f"Processing station: {db_station.name!r}...")
                    for db_variable in db_variables:
                        print(f"Processing variable: {db_variable.name!r}...")
                        months = _get_months(month)
                        if len(months) > 0:
                            for current_month in months:
                                print(f"Processing month: {current_month!r}...")
                                fut = harvest_monthly_measurements.submit(
                                    client,
                                    db_session,
                                    db_station,
                                    db_variable,
                                    current_month,
                                )
                                to_wait_for.append(fut)
                        else:
                            print("There are no months to process, skipping...")
                    for future in to_wait_for:
                        to_create.extend(future.result())
                    print(f"creating {len(to_create)} new monthly measurements...")
                    database.create_many_monthly_measurements(db_session, to_create)
            else:
                print("There are no stations to process, skipping...")
        else:
            print("There are no variables to process, skipping...")


@prefect.task(
    retries=settings.prefect.num_task_retries,
    retry_delay_seconds=settings.prefect.task_retry_delay_seconds,
)
def harvest_seasonal_measurements(
    client: httpx.Client,
    db_session: sqlmodel.Session,
    station: observations.Station,
    variable: observations.Variable,
    season: base.Season,
) -> list[observations.SeasonalMeasurementCreate]:
    existing_measurements = database.collect_all_seasonal_measurements(
        db_session,
        station_id_filter=station.id,
        variable_id_filter=variable.id,
        season_filter=season,
    )
    existing = {}
    for db_measurement in existing_measurements:
        measurement_id = operations.build_seasonal_measurement_id(db_measurement)
        existing[measurement_id] = db_measurement

    season_query_param = {
        base.Season.WINTER: 1,
        base.Season.SPRING: 2,
        base.Season.SUMMER: 3,
        base.Season.AUTUMN: 4,
    }[season]
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
    to_create = []
    for raw_measurement in response.json().get("data", []):
        measurement_create = observations.SeasonalMeasurementCreate(
            station_id=station.id,
            variable_id=variable.id,
            value=raw_measurement["valore"],
            year=int(raw_measurement["anno"]),
            season=season,
        )
        measurement_id = operations.build_seasonal_measurement_id(measurement_create)
        if measurement_id not in existing:
            to_create.append(measurement_create)
    return to_create


@prefect.flow(
    log_prints=True,
    retries=settings.prefect.num_flow_retries,
    retry_delay_seconds=settings.prefect.flow_retry_delay_seconds,
)
def refresh_seasonal_measurements(
    station_code: str | None = None,
    variable_name: str | None = None,
    season_name: str | None = None,
):
    settings = get_settings()
    client = httpx.Client()
    with sqlmodel.Session(database.get_engine(settings)) as db_session:
        db_variables = _get_variables(db_session, variable_name)
        if len(db_variables) > 0:
            db_stations = _get_stations(db_session, station_code)
            if len(db_stations) > 0:
                for db_station in db_stations:
                    to_create = []
                    to_wait_for = []
                    print(f"Processing station: {db_station.name!r}...")
                    for db_variable in db_variables:
                        print(f"Processing variable: {db_variable.name!r}...")
                        seasons = _get_seasons(season_name)
                        if len(seasons) > 0:
                            for season in _get_seasons(season_name):
                                print(f"Processing season: {season!r}...")
                                fut = harvest_seasonal_measurements.submit(
                                    client, db_session, db_station, db_variable, season
                                )
                                to_wait_for.append(fut)
                        else:
                            print("There are no seasons to process, skipping...")
                    for future in to_wait_for:
                        to_create.extend(future.result())
                    print(f"creating {len(to_create)} new seasonal measurements...")
                    database.create_many_seasonal_measurements(db_session, to_create)
            else:
                print("There are no stations to process, skipping...")
        else:
            print("There are no variables to process, skipping...")


@prefect.task(
    retries=settings.prefect.num_task_retries,
    retry_delay_seconds=settings.prefect.task_retry_delay_seconds,
)
def harvest_yearly_measurements(
    client: httpx.Client,
    db_session: sqlmodel.Session,
    station: observations.Station,
    variable: observations.Variable,
) -> list[observations.YearlyMeasurementCreate]:
    to_create = []
    existing_measurements = database.collect_all_yearly_measurements(
        db_session,
        station_id_filter=station.id,
        variable_id_filter=variable.id,
    )
    existing = {}
    for db_measurement in existing_measurements:
        measurement_id = operations.build_yearly_measurement_id(db_measurement)
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
        measurement_id = operations.build_yearly_measurement_id(
            yearly_measurement_create
        )
        if measurement_id not in existing:
            to_create.append(yearly_measurement_create)
    return to_create


@prefect.flow(
    log_prints=True,
    retries=settings.prefect.num_flow_retries,
    retry_delay_seconds=settings.prefect.flow_retry_delay_seconds,
)
def refresh_yearly_measurements(
    station_code: str | None = None,
    variable_name: str | None = None,
):
    settings = get_settings()
    client = httpx.Client()
    with sqlmodel.Session(database.get_engine(settings)) as db_session:
        db_variables = _get_variables(db_session, variable_name)
        if len(db_variables) > 0:
            db_stations = _get_stations(db_session, station_code)
            if len(db_stations) > 0:
                for db_station in db_stations:
                    to_create = []
                    to_wait_for = []
                    print(f"Processing station: {db_station.name!r}...")
                    for db_variable in db_variables:
                        print(f"Processing variable: {db_variable.name!r}...")
                        fut = harvest_yearly_measurements.submit(
                            client, db_session, db_station, db_variable
                        )
                        to_wait_for.append(fut)
                    for future in to_wait_for:
                        to_create.extend(future.result())
                    print(f"creating {len(to_create)} new yearly measurements...")
                    database.create_many_yearly_measurements(db_session, to_create)
            else:
                print("There are no stations to process, skipping...")
        else:
            print("There are no variables to process, skipping...")


def _get_stations(
    db_session: sqlmodel.Session, station_code: str | None = None
) -> list[observations.Station]:
    if station_code is not None:
        station = database.get_station_by_code(db_session, station_code)
        result = [station] if station else []
    else:
        result = database.collect_all_stations(db_session)
    return result


def _get_variables(
    db_session: sqlmodel.Session, variable_name: str | None = None
) -> list[observations.Variable]:
    if variable_name is not None:
        variable = database.get_variable_by_name(db_session, variable_name)
        result = [variable] if variable else []
    else:
        result = database.collect_all_variables(db_session)
    return result


def _get_seasons(season_name: str | None = None) -> list[base.Season]:
    if season_name is not None:
        try:
            result = [base.Season(season_name.upper())]
        except ValueError:
            print(f"Invalid season name: {season_name!r}")
            result = []
    else:
        result = [s for s in base.Season]
    return result


def _get_months(month_index: int | None = None) -> list[int]:
    if month_index is not None:
        if 1 <= month_index <= 12:
            result = [month_index]
        else:
            print(f"Invalid month index: {month_index!r}")
            result = []
    else:
        result = list(range(1, 13))
    return result