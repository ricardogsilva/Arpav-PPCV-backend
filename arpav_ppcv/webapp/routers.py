import logging
import urllib.parse
from typing import Annotated

import httpx
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)

from ..config import ArpavPpcvSettings
from ..schemas import models
from ..thredds import utils as thredds_utils
from ..operations import thredds as thredds_ops
from . import dependencies


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def landing_page():
    ...


@router.get(
    "/thredds-dataset-configurations/",
    response_model=models.ThreddsDatasetConfigurationList
)
async def list_thredds_dataset_configurations(
        request: Request,
        setttings: Annotated[ArpavPpcvSettings, Depends(dependencies.get_settings)]
):
    """List known THREDDS datasets."""
    items = []
    for ds_id, ds in thredds_ops.list_dataset_configurations(setttings).items():
        items.append(
            models.ThreddsDatasetConfiguration(
                identifier=ds_id,
                dataset_id_pattern=ds.dataset_id_pattern,
                unit=ds.unit,
                palette=ds.palette,
                range=ds.range,
                allowed_values=ds.allowed_values,
            )
        )
    return models.ThreddsDatasetConfigurationList(
        meta=models.ListMeta(
            returned_records=len(items),
            total_records=len(items),
            total_filtered_records=len(items)
        ),
        links=models.ListLinks(
            self=str(request.url_for("list_thredds_dataset_configurations"))
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
    """Serve dataset via OGC Web Map Service.

    Pass additional relevant WMS query parameters directly to this endpoint.
    """
    ds_config_id = dataset_id.partition("-")[0]
    ds_config = settings.thredds_server.datasets[ds_config_id]
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
    wms_url = parsed_url._replace(
        query=urllib.parse.urlencode(
            {
                **request.query_params,
                "service": "WMS",
                "version": version,
            }
        )
    ).geturl()
    logger.info(f"{wms_url=}")
    try:
        wms_response = await thredds_utils.proxy_request(wms_url, http_client)
    except httpx.HTTPError as err:
        logger.exception(msg=f"THREDDS server replied with an error")
        raise HTTPException(
            status_code=err.response.status_code,
            detail=err.response.text
        )
    return wms_response.content
