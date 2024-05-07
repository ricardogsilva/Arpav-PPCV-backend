import logging
import urllib.parse
from typing import Annotated

import httpx
import pydantic
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from sqlmodel import Session

from .... import database
from ....config import ArpavPpcvSettings
from ....thredds import utils as thredds_utils
from ... import dependencies
from ..schemas import coverages


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/coverage-configurations",
    response_model=coverages.CoverageConfigurationList
)
async def list_coverage_configurations(
        request: Request,
        db_session: Annotated[Session, Depends(dependencies.get_db_session)],
        list_params: Annotated[dependencies.CommonListFilterParameters, Depends()],
):
    """### List coverage configurations.

    A coverage configuration represents a set of multiple NetCDF files that are
    available in the ARPAV THREDDS server.

    A coverage configuration can be used to generate *coverage identifiers* that
    refer to individual NetCDF files by constructing a string based on the
    `dataset_id_pattern` property. For example, If there is a coverage configuration
    with the following properties:

    ```yaml
    name: myds
    coverage_id_pattern: {name}-something-{scenario}-{year_period}
    possible_values:
      - configuration_parameter_name: scenario
        configuration_parameter_value: scen1
      - configuration_parameter_name: scenario
        configuration_parameter_value: scen2
      - configuration_parameter_name: year_period
        configuration_parameter_value: winter
      - configuration_parameter_name: year_period
        configuration_parameter_value: autumn
    ```

    Then the following would be valid coverage identifiers:

    - `myds-something-scen1-winter`
    - `myds-something-scen1-autumn`
    - `myds-something-scen2-winter`
    - `myds-something-scen2-autumn`

    Each of these coverage identifiers could further be used to gain access to the WMS
    endpoint.

    """
    coverage_configurations, filtered_total = database.list_coverage_configurations(
        db_session,
        limit=list_params.limit,
        offset=list_params.offset,
        include_total=True
    )
    _, unfiltered_total = database.list_coverage_configurations(
        db_session, limit=1, offset=0, include_total=True
    )
    return coverages.CoverageConfigurationList.from_items(
        coverage_configurations,
        request,
        limit=list_params.limit,
        offset=list_params.offset,
        filtered_total=filtered_total,
        unfiltered_total=unfiltered_total
    )


@router.get(
    "/coverage-configurations/{coverage_configuration_id}",
    response_model=coverages.CoverageConfigurationReadDetail,
)
def get_coverage_configuration(
        request: Request,
        db_session: Annotated[Session, Depends(dependencies.get_db_session)],
        coverage_configuration_id: pydantic.UUID4
):
    db_coverage_configuration = database.get_coverage_configuration(
        db_session, coverage_configuration_id)
    allowed_coverage_identifiers = database.list_allowed_coverage_identifiers(
        db_session, coverage_configuration_id=db_coverage_configuration.id)
    return coverages.CoverageConfigurationReadDetail.from_db_instance(
        db_coverage_configuration, allowed_coverage_identifiers, request)


@router.get("/wms/{coverage_identifier}")
async def wms_endpoint(
        request: Request,
        db_session: Annotated[Session, Depends(dependencies.get_db_session)],
        settings: Annotated[ArpavPpcvSettings, Depends(dependencies.get_settings)],
        http_client: Annotated[httpx.AsyncClient, Depends(dependencies.get_http_client)],
        coverage_identifier: str,
        version: str = "1.3.0",
):
    """### Serve coverage via OGC Web Map Service.

    Pass additional relevant WMS query parameters directly to this endpoint.
    """
    coverage_configuration_name = coverage_identifier.partition("-")[0]
    db_coverage_configuration = database.get_coverage_configuration_by_name(
        db_session, coverage_configuration_name)
    if db_coverage_configuration is not None:
        try:
            thredds_url_fragment = db_coverage_configuration.get_thredds_url_fragment(coverage_identifier)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid coverage_identifier")
        else:
            base_wms_url = "/".join((
                settings.thredds_server.base_url,
                settings.thredds_server.wms_service_url_fragment,
                thredds_url_fragment
            ))
            parsed_url = urllib.parse.urlparse(base_wms_url)
            logger.info(f"{base_wms_url=}")
            query_params = {k.lower(): v for k, v in request.query_params.items()}
            logger.debug(f"original query params: {query_params=}")
            if query_params.get("request") in ("GetMap", "GetLegendGraphic"):
                query_params = thredds_utils.tweak_wms_get_map_request(
                    query_params,
                    ncwms_palette=db_coverage_configuration.palette,
                    ncwms_color_scale_range=(
                        db_coverage_configuration.color_scale_min,
                        db_coverage_configuration.color_scale_max),
                    uncertainty_visualization_scale_range=(
                        settings.thredds_server.uncertainty_visualization_scale_range)
                )
            elif query_params.get("request") == "GetCapabilities":
                # TODO: need to tweak the reported URLs
                # the response to a GetCapabilities request includes URLs for each
                # operation and some clients (like QGIS) use them for GetMap and
                # GetLegendGraphic - need to ensure these do not refer to the underlying
                # THREDDS server
                ...
            logger.debug(f"{query_params=}")
            wms_url = parsed_url._replace(
                query=urllib.parse.urlencode(
                    {
                        **query_params,
                        "service": "WMS",
                        "version": version,
                    }
                )
            ).geturl()
            logger.info(f"{wms_url=}")
            try:
                wms_response = await thredds_utils.proxy_request(wms_url, http_client)
            except httpx.HTTPStatusError as err:
                logger.exception(msg=f"THREDDS server replied with an error: {err.response.text}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=err.response.text
                )
            except httpx.HTTPError as err:
                logger.exception(msg=f"THREDDS server replied with an error")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                ) from err
            else:
                response = Response(
                    content=wms_response.content,
                    status_code=wms_response.status_code,
                    headers=dict(wms_response.headers)
                )
            return response
    else:
        raise HTTPException(status_code=400, detail="Invalid coverage_identifier")