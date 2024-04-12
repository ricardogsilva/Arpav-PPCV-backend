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
from ..schemas.base import (
    ListMeta,
    ListLinks,
)
from ..schemas.observations import (
    StationList,
    StationReadListItem,
    VariableList,
    VariableReadListItem,
    MonthlyMeasurementList,
    MonthlyMeasurementListItem,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/stations/", response_model=StationList)
def list_stations(
        request: Request,
        db_session: Annotated[Session, Depends(dependencies.get_db_session)],
        list_params: Annotated[dependencies.CommonListFilterParameters, Depends()]
):
    """List known stations."""
    logger.debug("debug hi!")
    logger.info("info hi!")
    logger.warning("warning hi!")
    logger.critical("critical hi!")
    print("normal hi!")
    print(f"{__name__=}")
    stations, filtered_total = database.list_stations(
        db_session,
        limit=list_params.limit,
        offset=list_params.offset,
        include_total=True
    )
    _, unfiltered_total = database.list_stations(
        db_session, limit=1, offset=0, include_total=True
    )
    return StationList.from_items(
        stations,
        request,
        limit=list_params.limit,
        offset=list_params.offset,
        filtered_total=filtered_total,
        unfiltered_total=unfiltered_total
    )

@router.get(
    "/stations/{station_id}",
    response_model=StationReadListItem,
)
def get_station(
        request: Request,
        db_session: Annotated[Session, Depends(dependencies.get_db_session)],
        station_id: pydantic.UUID4,
):
    db_station = database.get_station(db_session, station_id)
    return StationReadListItem.from_db_instance(db_station, request)


@router.get("/variables/", response_model=VariableList)
def list_variables(
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
    return VariableList(
        meta=ListMeta(
            returned_records=len(variables),
            total_filtered_records=filtered_total,
            total_records=unfiltered_total,
        ),
        links=ListLinks(
            self=""
        ),
        items=[
            VariableReadListItem(**v.model_dump()) for v in variables
        ]
    )


@router.get("/monthly-measurements/", response_model=MonthlyMeasurementList)
def list_variables(
        db_session: Annotated[Session, Depends(dependencies.get_db_session)],
        list_params: Annotated[dependencies.CommonListFilterParameters, Depends()]
):
    """List known monthly measurements."""
    monthly_measurements, filtered_total = database.list_monthly_measurements(
        db_session,
        limit=list_params.limit,
        offset=list_params.offset,
        include_total=True
    )
    _, unfiltered_total = database.list_monthly_measurements(
        db_session, limit=1, offset=0, include_total=True
    )
    return MonthlyMeasurementList(
        meta=ListMeta(
            returned_records=len(monthly_measurements),
            total_filtered_records=filtered_total,
            total_records=unfiltered_total,
        ),
        links=ListLinks(
            self=""
        ),
        items=[
            MonthlyMeasurementListItem(**v.model_dump()) for v in monthly_measurements
        ]
    )
