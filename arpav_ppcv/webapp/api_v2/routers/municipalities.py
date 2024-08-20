import logging
from typing import Annotated

import shapely.io
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)
from sqlmodel import Session

from .... import database as db
from ... import dependencies
from ...responses import GeoJsonResponse
from ..schemas.geojson import municipalities as municipalities_geojson

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/",
    response_class=GeoJsonResponse,
    response_model=municipalities_geojson.MunicipalityFeatureCollection,
)
def list_municipalities(
    request: Request,
    db_session: Annotated[Session, Depends(dependencies.get_db_session)],
    list_params: Annotated[dependencies.CommonListFilterParameters, Depends()],
    coords: str | None = None,
    name: str | None = None,
    province: str | None = None,
    region: str | None = None,
):
    """List Italian municipalities."""
    geom_filter_kwarg = {}
    if coords is not None:
        geom = shapely.io.from_wkt(coords)
        if geom.geom_type == "Point":
            geom_filter_kwarg = {"point_filter": geom}
        elif geom.geom_type == "Polygon":
            geom_filter_kwarg = {"polygon_intersection_filter": geom}
        else:
            raise HTTPException(
                status_code=400, detail="geometry be either point or polygon"
            )
    municipalities, filtered_total = db.list_municipalities(
        db_session,
        limit=list_params.limit,
        offset=list_params.offset,
        include_total=True,
        name_filter=name,
        province_name_filter=province,
        region_name_filter=region,
        **geom_filter_kwarg,
    )
    _, unfiltered_total = db.list_municipalities(
        db_session, limit=1, offset=0, include_total=True
    )
    return municipalities_geojson.MunicipalityFeatureCollection.from_items(
        municipalities,
        request,
        limit=list_params.limit,
        offset=list_params.offset,
        filtered_total=filtered_total,
        unfiltered_total=unfiltered_total,
    )
