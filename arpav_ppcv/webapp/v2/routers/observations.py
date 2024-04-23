import logging
from typing import Annotated

import pydantic
from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from sqlmodel import Session

from .... import database
from ... import dependencies
from ..schemas import observations

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/stations", response_model=observations.StationList)
def list_stations(
        request: Request,
        db_session: Annotated[Session, Depends(dependencies.get_db_session)],
        list_params: Annotated[dependencies.CommonListFilterParameters, Depends()]
):
    """List known stations."""
    stations, filtered_total = database.list_stations(
        db_session,
        limit=list_params.limit,
        offset=list_params.offset,
        include_total=True
    )
    _, unfiltered_total = database.list_stations(
        db_session, limit=1, offset=0, include_total=True
    )
    return observations.StationList.from_items(
        stations,
        request,
        limit=list_params.limit,
        offset=list_params.offset,
        filtered_total=filtered_total,
        unfiltered_total=unfiltered_total
    )


@router.get(
    "/stations/{station_id}",
    response_model=observations.StationReadListItem,
)
def get_station(
        request: Request,
        db_session: Annotated[Session, Depends(dependencies.get_db_session)],
        station_id: pydantic.UUID4,
):
    db_station = database.get_station(db_session, station_id)
    return observations.StationReadListItem.from_db_instance(db_station, request)


@router.get("/variables", response_model=observations.VariableList)
def list_variables(
        request: Request,
        db_session: Annotated[Session, Depends(dependencies.get_db_session)],
        list_params: Annotated[dependencies.CommonListFilterParameters, Depends()]
):
    """List known variables."""
    variables, filtered_total = database.list_variables(
        db_session,
        limit=list_params.limit,
        offset=list_params.offset,
        include_total=True
    )
    _, unfiltered_total = database.list_variables(
        db_session, limit=1, offset=0, include_total=True
    )
    return observations.VariableList.from_items(
        variables,
        request,
        limit=list_params.limit,
        offset=list_params.offset,
        filtered_total=filtered_total,
        unfiltered_total=unfiltered_total
    )


@router.get(
    "/variables/{variable_id}",
    response_model=observations.VariableReadListItem,
)
def get_variable(
        request: Request,
        db_session: Annotated[Session, Depends(dependencies.get_db_session)],
        variable_id: pydantic.UUID4,
):
    db_variable = database.get_variable(db_session, variable_id)
    return observations.VariableReadListItem.from_db_instance(db_variable, request)


@router.get(
    "/monthly-measurements", response_model=observations.MonthlyMeasurementList)
def list_monthly_measurements(
        request: Request,
        db_session: Annotated[Session, Depends(dependencies.get_db_session)],
        list_params: Annotated[dependencies.CommonListFilterParameters, Depends()],
        station_code: str | None = None,
        variable_name: str | None = None,
):
    """List known monthly measurements."""
    if station_code is not None:
        db_station = database.get_station_by_code(db_session, station_code)
        if db_station is not None:
            station_id = db_station.id
        else:
            raise ValueError("Invalid station code")
    else:
        station_id = None
    if variable_name is not None:
        db_variable = database.get_variable_by_name(db_session, variable_name)
        if db_variable is not None:
            variable_id = db_variable.id
        else:
            raise ValueError("Invalid variable name")
    else:
        variable_id = None
    monthly_measurements, filtered_total = database.list_monthly_measurements(
        db_session,
        limit=list_params.limit,
        offset=list_params.offset,
        station_id_filter=station_id,
        variable_id_filter=variable_id,
        include_total=True
    )
    _, unfiltered_total = database.list_monthly_measurements(
        db_session, limit=1, offset=0, include_total=True
    )
    return observations.MonthlyMeasurementList.from_items(
        monthly_measurements,
        request,
        limit=list_params.limit,
        offset=list_params.offset,
        filtered_total=filtered_total,
        unfiltered_total=unfiltered_total
    )


@router.get(
    "/monthly-measurements/{monthly_measurement_id}",
    response_model=observations.MonthlyMeasurementReadListItem,
)
def get_monthly_measurement(
        request: Request,
        db_session: Annotated[Session, Depends(dependencies.get_db_session)],
        monthly_measurement_id: pydantic.UUID4,
):
    db_monthly_measurement = database.get_monthly_measurement(
        db_session, monthly_measurement_id)
    return observations.MonthlyMeasurementReadListItem.from_db_instance(
        db_monthly_measurement, request)
