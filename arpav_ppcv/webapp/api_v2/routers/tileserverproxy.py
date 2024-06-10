"""A FastAPI router that proxies requests to the tileserver."""

import logging
from typing import (
    Annotated,
)

import httpx
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.responses import (
    JSONResponse,
    Response,
)

from ... import dependencies
from ....config import ArpavPpcvSettings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/catalog")
async def get_vector_tiles_catalog(
    settings: Annotated[ArpavPpcvSettings, Depends(dependencies.get_settings)],
    http_client: Annotated[httpx.AsyncClient, Depends(dependencies.get_http_client)],
):
    response = await http_client.get(f"{settings.martin_tile_server_base_url}/catalog")
    return JSONResponse(
        status_code=response.status_code,
        content=response.json(),
    )


@router.get("/{layer}/{z}/{x}/{y}")
async def vector_tiles_endpoint(
    settings: Annotated[ArpavPpcvSettings, Depends(dependencies.get_settings)],
    http_client: Annotated[httpx.AsyncClient, Depends(dependencies.get_http_client)],
    layer: str,
    z: int,
    x: int,
    y: int,
):
    """Serve vector tiles."""
    response = await http_client.get(
        f"{settings.martin_tile_server_base_url}/{layer}/{z}/{x}/{y}"
    )
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
    )
