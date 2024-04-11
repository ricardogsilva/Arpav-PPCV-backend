import logging
import urllib.parse
from typing import Annotated

import httpx
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)

from ....config import ArpavPpcvSettings
from ..schemas.thredds import (
    ThreddsDatasetConfiguration,
    ThreddsDatasetConfigurationIdentifierList,
    ThreddsDatasetConfigurationList,
)
from ..schemas.base import (
    ListMeta,
    ListLinks,
)
from ....thredds import utils as thredds_utils
from ....operations import thredds as thredds_ops
from ... import dependencies


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def landing_page():
    ...


@router.get(
    "/thredds-dataset-configurations/",
    response_model=ThreddsDatasetConfigurationList
)
async def list_thredds_dataset_configurations(
        request: Request,
        setttings: Annotated[ArpavPpcvSettings, Depends(dependencies.get_settings)]
):
    """### List THREDDS dataset configurations.

    A THREDDS dataset configuration represents a set of multiple NetCDF files that are
    available in the ARPAV THREDDS server.

    A dataset configuration can be used to generate ids that refer to individual
    NetCDF files by constructing a string based on the `dataset_id_pattern` property.
    For example, If there is a dataset configuration with the following properties:

    ```yaml
    identifier: myds
    dataset_id_pattern: {identifier}-something-{scenario}-{year_period}
    allowed_values:
      scenario:
        - scen1
        - scen2
      year_period:
        - winter
        - autumn
    ```

    Then the following would be valid dataset identifiers:

    - `myds-something-scen1-winter`
    - `myds-something-scen1-autumn`
    - `myds-something-scen2-winter`
    - `myds-something-scen2-autumn`

    Each of these dataset identifiers could further be used to gain access to the WMS
    endpoint.

    """
    items = []
    for ds_id, ds in thredds_ops.list_dataset_configurations(setttings).items():
        items.append(
            ThreddsDatasetConfiguration(
                identifier=ds_id,
                dataset_id_pattern=ds.dataset_id_pattern,
                unit=ds.unit,
                palette=ds.palette,
                range=ds.range,
                allowed_values=ds.allowed_values,
            )
        )
    return ThreddsDatasetConfigurationList(
        meta=ListMeta(
            returned_records=len(items),
            total_records=len(items),
            total_filtered_records=len(items)
        ),
        links=ListLinks(
            self=str(request.url_for("list_thredds_dataset_configurations"))
        ),
        items=items
    )


@router.get(
    "/thredds_dataset_configurations/{configuration_id}/dataset-ids/",
    response_model=ThreddsDatasetConfigurationIdentifierList
)
async def list_dataset_identifiers(
        request: Request,
        settings: Annotated[ArpavPpcvSettings, Depends(dependencies.get_settings)],
        configuration_id: str):
    ds_config = settings.thredds_server.datasets[configuration_id]
    items = thredds_ops.list_dataset_identifiers(configuration_id, ds_config)
    return ThreddsDatasetConfigurationIdentifierList(
        meta=ListMeta(
            returned_records=len(items),
            total_records=len(items),
            total_filtered_records=len(items),
        ),
        links=ListLinks(
            self=str(
                request.url_for(
                    "list_dataset_identifiers",
                    configuration_id=configuration_id
                )
            )
        ),
        items=items
    )


@router.get("/wms/{dataset_id}")
async def wms_endpoint(
        request: Request,
        settings: Annotated[ArpavPpcvSettings, Depends(dependencies.get_settings)],
        http_client: Annotated[httpx.AsyncClient, Depends(dependencies.get_http_client)],
        dataset_id: str,
        version: str = "1.3.0",
):
    """### Serve dataset via OGC Web Map Service.

    Pass additional relevant WMS query parameters directly to this endpoint.
    """
    ds_config_id = dataset_id.partition("-")[0]
    logger.debug(f"{settings=}")
    try:
        ds_config = settings.thredds_server.datasets[ds_config_id]
    except KeyError as err:
        raise HTTPException(status_code=400, detail="Invalid dataset_id") from err
    else:
        id_parameters = ds_config.validate_dataset_id(dataset_id)
        parsed_id_parameters = {
            k: thredds_utils.get_parameter_internal_value(k, v)
            for k, v in id_parameters.items()
        }
        logger.debug(f"{parsed_id_parameters=}")
        base_wms_url = thredds_utils.build_dataset_service_url(
            ds_config_id,
            parsed_id_parameters,
            url_path_pattern=ds_config.thredds_url_pattern,
            thredds_base_url=settings.thredds_server.base_url,
            service_url_fragment=settings.thredds_server.wms_service_url_fragment
        )
        parsed_url = urllib.parse.urlparse(base_wms_url)
        logger.info(f"{base_wms_url=}")
        query_params = {k.lower(): v for k, v in request.query_params.items()}
        if query_params.get("request") in ("GetMap", "GetLegendGraphic"):
            query_params = thredds_utils.tweak_wms_get_map_request(
                query_params,
                ds_config,
                settings.thredds_server.uncertainty_visualization_scale_range
            )
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
