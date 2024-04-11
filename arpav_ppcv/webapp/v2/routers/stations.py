from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlmodel import Session

from .... import database
from ... import dependencies
from ..schemas.base import (
    ListMeta,
    ListLinks,
)
from ..schemas.stations import (
    StationList,
    StationReadListItem,
)

router = APIRouter()


@router.get("/stations/", response_model=StationList)
def list_stations(
        db_session: Annotated[Session, Depends(dependencies.get_db_session)],
        list_params: Annotated[dependencies.CommonListFilterParameters, Depends()]
):
    stations, filtered_total = database.list_stations(
        db_session,
        limit=list_params.limit,
        offset=list_params.offset,
        include_total=True
    )
    _, unfiltered_total = database.list_stations(
        db_session, limit=1, offset=0, include_total=True
    )
    return StationList(
        meta=ListMeta(
            returned_records=len(stations),
            total_filtered_records=filtered_total,
            total_records=unfiltered_total,
        ),
        links=ListLinks(
            self=""
        ),
        items=[
            StationReadListItem(**s.model_dump()) for s in stations
        ]
    )
