import logging
import urllib.parse
import uuid
from typing import (
    Annotated,
    Optional,
)

import httpx
import pydantic
import shapely.io
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Request,
    Response,
    status,
)
from sqlmodel import Session

from .... import (
    database as db,
    operations,
)
from ....config import ArpavPpcvSettings
from ....thredds import utils as thredds_utils
from ....schemas.base import (
    CoverageDataSmoothingStrategy,
    ObservationDataSmoothingStrategy,
)
from ... import dependencies
from ..schemas import coverages as coverage_schemas


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/coverage-configurations",
    response_model=coverage_schemas.CoverageConfigurationList
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
    coverage_configurations, filtered_total = db.list_coverage_configurations(
        db_session,
        limit=list_params.limit,
        offset=list_params.offset,
        include_total=True
    )
    _, unfiltered_total = db.list_coverage_configurations(
        db_session, limit=1, offset=0, include_total=True
    )
    return coverage_schemas.CoverageConfigurationList.from_items(
        coverage_configurations,
        request,
        limit=list_params.limit,
        offset=list_params.offset,
        filtered_total=filtered_total,
        unfiltered_total=unfiltered_total
    )


@router.get(
    "/coverage-configurations/{coverage_configuration_id}",
    response_model=coverage_schemas.CoverageConfigurationReadDetail,
)
def get_coverage_configuration(
        request: Request,
        db_session: Annotated[Session, Depends(dependencies.get_db_session)],
        coverage_configuration_id: pydantic.UUID4
):
    db_coverage_configuration = db.get_coverage_configuration(
        db_session, coverage_configuration_id)
    allowed_coverage_identifiers = db.list_allowed_coverage_identifiers(
        db_session, coverage_configuration_id=db_coverage_configuration.id)
    return coverage_schemas.CoverageConfigurationReadDetail.from_db_instance(
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
    db_coverage_configuration = db.get_coverage_configuration_by_coverage_identifier(
        db_session, coverage_identifier)
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


@router.get(
    "/time-series/{coverage_identifier}", response_model=coverage_schemas.TimeSeriesList)
def get_time_series(
        db_session: Annotated[Session, Depends(dependencies.get_db_session)],
        settings: Annotated[ArpavPpcvSettings, Depends(dependencies.get_settings)],
        http_client: Annotated[httpx.Client, Depends(dependencies.get_sync_http_client)],
        coverage_identifier: str,
        coords: str,
        datetime: Optional[str] = "../..",
        include_coverage_data: bool = True,
        include_observation_data: bool = False,
        coverage_data_smoothing: Annotated[
            list[CoverageDataSmoothingStrategy],
            Query()
        ] = [ObservationDataSmoothingStrategy.NO_SMOOTHING],  # noqa
        observation_data_smoothing: Annotated[
            list[ObservationDataSmoothingStrategy],
            Query()
        ] = [ObservationDataSmoothingStrategy.NO_SMOOTHING],  # noqa
        include_coverage_uncertainty: bool = False,
        include_coverage_related_data: bool = False,
):
    db_coverage_configuration = db.get_coverage_configuration_by_coverage_identifier(
        db_session, coverage_identifier)
    if db_coverage_configuration is not None:
        geom = shapely.io.from_wkt(coords)
        if geom.geom_type == "MultiPoint":
            logger.warning(
                f"Expected coords parameter to be a WKT Point but "
                f"got {geom.geom_type!r} instead - Using the first point"
            )
            point_geom = geom.geoms[0]
        elif geom.geom_type == "Point":
            point_geom = geom
        else:
            logger.warning(
                f"Expected coords parameter to be a WKT Point but "
                f"got {geom.geom_type!r} instead - Using the centroid instead"
            )
            point_geom = geom.centroid
        time_series = operations.get_coverage_time_series(
            settings,
            db_session,
            http_client,
            coverage_configuration=db_coverage_configuration,
            coverage_identifier=coverage_identifier,
            point_geom=point_geom,
            temporal_range=datetime,
            include_coverage_data=include_coverage_data,
            include_observation_data=include_observation_data,
            coverage_data_smoothing=coverage_data_smoothing,
            observation_data_smoothing=observation_data_smoothing,
            include_coverage_uncertainty=include_coverage_uncertainty,
            include_coverage_related_data=include_coverage_related_data,
        )
        coverage_df = time_series[coverage_identifier]
        series = []
        if include_coverage_data:
            for series_name, series_measurements in coverage_df.to_dict().items():
                name_prefix, smoothing_strategy = series_name.rpartition("__")[::2]
                smoothed_with = CoverageDataSmoothingStrategy(smoothing_strategy)
                if (
                        smoothed_with == CoverageDataSmoothingStrategy.NO_SMOOTHING and
                        CoverageDataSmoothingStrategy.NO_SMOOTHING not in coverage_data_smoothing
                ):
                    continue  # client did not ask for the NO_SMOOTHING strategy
                else:
                    measurements = []
                    for timestamp, value in series_measurements.items():
                        measurements.append(
                            coverage_schemas.TimeSeriesItem(
                                value=value, datetime=timestamp)
                        )
                    series.append(
                        coverage_schemas.TimeSeries(
                            name=series_name,
                            values=measurements,
                            info={
                                "coverage_identifier": coverage_identifier,
                                "smoothing": smoothing_strategy.lower()
                            }
                        )
                    )

        if include_observation_data:
            variable = db_coverage_configuration.related_observation_variable
            for df_name, df in time_series.items():
                if df_name.startswith("station_"):
                    station_id = uuid.UUID(df_name.split("_")[1])
                    db_station = db.get_station(db_session, station_id)
                    for series_name, series_measurements in df.to_dict().items():
                        name_prefix, smoothing_strategy = series_name.rpartition("__")[::2]
                        smoothed_with = ObservationDataSmoothingStrategy(smoothing_strategy)
                        if (
                                smoothed_with == ObservationDataSmoothingStrategy.NO_SMOOTHING and
                                ObservationDataSmoothingStrategy.NO_SMOOTHING not in observation_data_smoothing
                        ):
                            continue  # client did not ask for the NO_SMOOTHING strategy
                        else:
                            measurements = []
                            for timestamp, value in series_measurements.items():
                                measurements.append(
                                    coverage_schemas.TimeSeriesItem(
                                        value=value, datetime=timestamp)
                                )
                            series.append(
                                coverage_schemas.TimeSeries(
                                    name=series_name,
                                    values=measurements,
                                    info={
                                        "station_id": str(db_station.id),
                                        "station_name": db_station.name,
                                        "variable_name": variable.name,
                                        "variable_description": variable.description,
                                        "smoothing": smoothing_strategy.lower()
                                    }
                                ),
                            )
        if include_coverage_uncertainty:
            ...
        if include_coverage_related_data:
            ...
        return coverage_schemas.TimeSeriesList(series=series)
    else:
        raise HTTPException(status_code=400, detail="Invalid coverage_identifier")

