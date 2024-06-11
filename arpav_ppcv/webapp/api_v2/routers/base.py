import importlib.metadata
import logging
import os
from typing import Annotated

import sqlmodel
from fastapi import (
    APIRouter,
    Depends,
)

from .... import database
from ... import dependencies
from ..schemas.base import AppInformation


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=AppInformation)
async def get_app_info():
    """Return information about the ARPAV-PPCV application."""
    return {
        "version": importlib.metadata.version("arpav_ppcv_backend"),
        "git_commit": os.getenv("GIT_COMMIT", "unknown"),
    }


@router.get("/info/{longitude}/{latitude")
def get_coordinates_info(
    db_session: Annotated[sqlmodel.Session, Depends(dependencies.get_db_session)],
    longitude: float,
    latitude: float,
):
    """Return information about a point location."""
    municipality = database.get_municipality_by_coordinates(
        db_session, longitude, latitude
    )
    logger.debug(f"{municipality=}")
