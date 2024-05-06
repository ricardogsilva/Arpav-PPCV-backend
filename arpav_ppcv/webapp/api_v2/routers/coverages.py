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
from ....operations import thredds as thredds_ops
from ... import dependencies
from ..schemas import coverages
from ..schemas.base import (
    ListMeta,
    ListLinks,
)


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

    A coverage configuration can be used to generate ids that refer to individual
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
