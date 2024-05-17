import datetime as dt
import functools
import io
import logging
from typing import Optional

import httpx
import pandas as pd
import pyproj
import shapely
import shapely.io
import sqlmodel
from dateutil.parser import isoparse
from geoalchemy2.shape import to_shape
from loess.loess_1d import loess_1d
from pyproj.enums import TransformDirection
from shapely.ops import transform

from . import database
from .config import ArpavPpcvSettings
from .schemas import (
    base,
    coverages,
    observations,
)
from .thredds import ncss

logger = logging.getLogger(__name__)


def get_coverage_time_series(
        settings: ArpavPpcvSettings,
        session: sqlmodel.Session,
        http_client: httpx.Client,
        coverage: coverages.CoverageInternal,
        point_geom: shapely.Point,
        temporal_range: str,
        coverage_smoothing_strategies: list[base.CoverageDataSmoothingStrategy],
        observation_smoothing_strategies: list[base.ObservationDataSmoothingStrategy],
        include_coverage_data: bool = True,
        include_observation_data: bool = False,
        include_coverage_uncertainty: bool = False,
        include_coverage_related_data: bool = False,
) -> dict[str, pd.DataFrame]:
    """Retrieve time series for a coverage."""
    start, end = _parse_temporal_range(temporal_range)
    coverage_data_ncss_url = "/".join((
        settings.thredds_server.base_url,
        settings.thredds_server.netcdf_subset_service_url_fragment,
        coverage.configuration.get_thredds_url_fragment(coverage.identifier)
    ))
    raw_coverage_data = ncss.query_dataset(
        http_client,
        thredds_ncss_url=coverage_data_ncss_url,
        variable_name=coverage.configuration.netcdf_main_dataset_name,
        longitude=point_geom.x,
        latitude=point_geom.y,
        time_start=start,
        time_end=end,
    )
    measurements = {}
    if include_coverage_data:
        coverage_data = _process_coverage_data(
            raw_coverage_data,
            coverage,
            coverage_smoothing_strategies,
            start,
            end
        )
        measurements[coverage.identifier] = coverage_data
        if include_coverage_uncertainty:
            has_uncertainty_cov_confs = any((
                coverage.configuration.uncertainty_lower_bounds_coverage_configuration,
                coverage.configuration.uncertainty_upper_bounds_coverage_configuration,
            ))
            if has_uncertainty_cov_confs:
                uncertainty_data = _get_coverage_uncertainty_time_series(
                    settings, http_client, coverage.configuration, coverage.identifier,
                    point_geom, start, end, coverage_smoothing_strategies,
                )
                measurements.update(**uncertainty_data)
        if include_coverage_related_data:
            # TODO: how to map to related data?
            ...
    if include_observation_data:
        if coverage.configuration.related_observation_variable is not None:
            station_data = _get_station_data(
                session,
                settings,
                point_geom,
                coverage.configuration,
                coverage.identifier,
            )
            if station_data is not None:
                raw_station_data, station = station_data
                data_ = _process_seasonal_station_data(
                    coverage.configuration.related_observation_variable,
                    raw_station_data, observation_smoothing_strategies, start, end
                )
                station_data_series_key = "_".join((
                    "station",
                    str(station.id),
                    coverage.configuration.related_observation_variable.name,
                ))
                measurements[station_data_series_key] = data_
            else:
                logger.info("No station data found, skipping...")
        else:
            logger.info(
                "Cannot include observation data - no observation variable is related "
                "to this coverage configuration"
            )
    return measurements


def _get_station_data(
        session: sqlmodel.Session,
        settings: ArpavPpcvSettings,
        point_geom: shapely.Point,
        coverage_configuration: coverages.CoverageConfiguration,
        coverage_identifier: str,
) -> Optional[
    tuple[
        list[
            observations.MonthlyMeasurement |
            observations.SeasonalMeasurement |
            observations.YearlyMeasurement
            ],
        observations.Station
    ]
]:
    point_buffer_geom = _get_spatial_buffer(
        point_geom, settings.nearest_station_radius_meters)
    nearby_stations = database.collect_all_stations(
        session, polygon_intersection_filter=point_buffer_geom)
    if len(nearby_stations) > 0:
        retriever_kwargs = {
            "variable_id_filter": coverage_configuration.observation_variable_id
        }
        aggregation_type = coverage_configuration.observation_variable_aggregation_type
        if aggregation_type == base.ObservationAggregationType.MONTHLY:
            retriever = functools.partial(
                database.collect_all_monthly_measurements,
                session,
                **retriever_kwargs,
                month_filter=None
            )
        elif aggregation_type == base.ObservationAggregationType.SEASONAL:
            retriever = functools.partial(
                database.collect_all_seasonal_measurements,
                session,
                **retriever_kwargs,
                season_filter=coverage_configuration.get_seasonal_aggregation_query_filter(
                    coverage_identifier)
            )
        else:  # ANNUAL
            retriever = functools.partial(
                database.collect_all_yearly_measurements,
                session,
                **retriever_kwargs,
            )
        sorted_stations = sorted(
            nearby_stations, key=lambda s: to_shape(s.geom).distance(point_geom))
        # order nearby stations by distance and then iterate through them in order to
        # try to get measurements for the relevant variable and temporal aggregation
        logger.debug(f"{sorted_stations=}")
        for station in sorted_stations:
            logger.debug(f"Processing station {station.id}...")
            raw_station_data = retriever(station_id_filter=station.id)
            if len(raw_station_data) > 0:
                # stop with the first station that has data
                result = (raw_station_data, station)
                break
        else:
            result = None
            logger.info("Nearby stations do not have data")
    else:
        logger.info(
            f"There are no nearby stations from {shapely.io.to_wkt(point_geom)}")
        result = None
    return result


def _process_seasonal_station_data(
        variable: observations.Variable,
        raw_data: list[observations.SeasonalMeasurement],
        smoothing_strategies: list[base.ObservationDataSmoothingStrategy],
        time_start: Optional[dt.datetime],
        time_end: Optional[dt.datetime],
) -> pd.DataFrame:
    df = pd.DataFrame(
        [i.model_dump() for i in raw_data]
    )
    df = df[["value", "season", "year"]]
    df = df.rename(columns={"value": variable.name})

    df["season_month"] = df["season"].astype("string").replace({
        "Season.WINTER": "01",
        "Season.SPRING": "04",
        "Season.SUMMER": "07",
        "Season.AUTUMN": "10"
    })
    df["time"] = pd.to_datetime(
        df["year"].astype("string") + "-" + df["season_month"] + "-01",
        utc=True
    )
    df = df[[variable.name, "time"]]
    df.set_index("time", inplace=True)
    if time_start is not None:
        df = df[time_start:]
    if time_end is not None:
        df = df[:time_end]
    for strategy in smoothing_strategies:
        column_name = "__".join((variable.name, strategy.value))
        if strategy == base.ObservationDataSmoothingStrategy.NO_SMOOTHING:
            df[column_name] = df[variable.name]
        elif strategy == base.ObservationDataSmoothingStrategy.MOVING_AVERAGE_5_YEARS:
            df[column_name] = df[variable.name].rolling(window=5, center=True).mean()
    df = df.drop(columns=[variable.name])
    df = df.dropna()
    return df


def _process_coverage_data(
        raw_data: str,
        coverage: coverages.CoverageInternal,
        smoothing_strategies: list[base.CoverageDataSmoothingStrategy],
        time_start: Optional[dt.datetime],
        time_end: Optional[dt.datetime],
) -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(raw_data), parse_dates=["time"])

    # get name of the colum that holds the main variable
    variable_name = coverage.configuration.netcdf_main_dataset_name
    try:
        col_name = [c for c in df.columns if c.startswith(f"{variable_name}[")][0]
    except IndexError:
        raise RuntimeError(
            f"Could not extract main data series from dataframe "
            f"with columns {df.columns}"
        )
    else:
        # keep only time and main variable - we don't care about other stuff
        df = df[["time", col_name]]
        df = df.rename(columns={col_name: coverage.identifier})

        # - filter out values outside the temporal range
        df.set_index("time", inplace=True)
        if time_start is not None:
            df = df[time_start:]
        if time_end is not None:
            df = df[:time_end]
        for strategy in smoothing_strategies:
            column_name = "__".join((coverage.identifier, strategy.value))
            if strategy == base.CoverageDataSmoothingStrategy.NO_SMOOTHING:
                df[column_name] = df[coverage.identifier]
            elif strategy == base.CoverageDataSmoothingStrategy.MOVING_AVERAGE_11_YEARS:
                df[column_name] = df[coverage.identifier].rolling(
                    center=True, window=11).mean()
            elif strategy == base.CoverageDataSmoothingStrategy.LOESS_SMOOTHING:
                _, loess_smoothed, _ = loess_1d(
                    df.index.astype("int64"),
                    df[coverage.identifier],
                )
                df[column_name] = loess_smoothed
        df = df.drop(columns=[coverage.identifier])
        df = df.dropna()
        return df


def _get_individual_uncertainty_time_series(
        settings: ArpavPpcvSettings,
        http_client: httpx.Client,
        used_values: list[coverages.ConfigurationParameterValue],
        uncert_coverage_configuration: coverages.CoverageConfiguration,
        point_geom: shapely.Point,
        time_start: Optional[dt.datetime],
        time_end: Optional[dt.datetime],
        smoothing_strategies: list[base.CoverageDataSmoothingStrategy],
) -> pd.DataFrame:
    cov_identifier = (
        uncert_coverage_configuration.build_coverage_identifier(used_values)
    )
    ncss_url = "/".join((
        settings.thredds_server.base_url,
        settings.thredds_server.netcdf_subset_service_url_fragment,
        uncert_coverage_configuration.get_thredds_url_fragment(cov_identifier)
    ))
    raw_coverage_data = ncss.query_dataset(
        http_client,
        thredds_ncss_url=ncss_url,
        variable_name=uncert_coverage_configuration.netcdf_main_dataset_name,
        longitude=point_geom.x,
        latitude=point_geom.y,
        time_start=time_start,
        time_end=time_end,
    )
    return _process_coverage_data(
        raw_coverage_data,
        uncert_coverage_configuration,
        cov_identifier,
        smoothing_strategies,
        time_start,
        time_end
    )


def _get_coverage_uncertainty_time_series(
        settings: ArpavPpcvSettings,
        http_client: httpx.Client,
        coverage_conf: coverages.CoverageConfiguration,
        coverage_identifier: str,
        point_geom: shapely.Point,
        time_start: Optional[dt.datetime],
        time_end: Optional[dt.datetime],
        smoothing_strategies: list[base.CoverageDataSmoothingStrategy],
) -> dict[str, pd.DataFrame]:
    used_possible_values = coverage_conf.retrieve_used_values(
        coverage_identifier)
    result = {}
    used_values = [
        pv.configuration_parameter_value for pv in used_possible_values]
    if lower_conf := coverage_conf.uncertainty_upper_bounds_coverage_configuration:
        result[f"{coverage_identifier}_uncertainty_lower_bounds"] = (
            _get_individual_uncertainty_time_series(
                settings, http_client, used_values, lower_conf,
                point_geom, time_start, time_end, smoothing_strategies
            )
        )
    if upper_conf := coverage_conf.uncertainty_upper_bounds_coverage_configuration:
        result[f"{coverage_identifier}_uncertainty_lower_bounds"] = (
            _get_individual_uncertainty_time_series(
                settings, http_client, used_values, upper_conf,
                point_geom, time_start, time_end, smoothing_strategies
            )
        )
    return result


def _parse_temporal_range(
        raw_temporal_range: str) -> tuple[dt.datetime | None, dt.datetime | None]:
    """Parse a temporal range string, converting time to UTC.

    The expected format for the input temporal range is described in the
    OGC API - EDR standard:

    https://docs.ogc.org/is/19-086r6/19-086r6.html#req_core_rc-time-response

    Basically it is a string with an optional start datetime and an optional end
    datetime.
    """

    raw_start, raw_end = raw_temporal_range.partition("/")[::2]
    open_interval_pattern = ".."
    if raw_start != open_interval_pattern:
        start = isoparse(raw_start).astimezone(dt.timezone.utc)
    else:
        start = None
    if raw_end != open_interval_pattern:
        end = isoparse(raw_end).astimezone(dt.timezone.utc)
    else:
        end = None
    return start, end


def _get_spatial_buffer(
        point_geom: shapely.Point, distance_meters: int) -> shapely.Polygon:
    """Buffer input point.

    This function expects the input point geometry to be in EPSG:4326 CRS and will
    return a buffer also in the same CRS. However, the buffer's distance is expected
    to be provided in meters. This function takes care of reprojecting the input
    geometry and the output buffer too.
    """
    coordinate_transformer = pyproj.Transformer.from_crs(
        pyproj.CRS("EPSG:4326"),
        pyproj.CRS("EPSG:3004"),
        always_xy=True
    ).transform
    forward_coordinate_transformer = functools.partial(
        coordinate_transformer, direction=TransformDirection.FORWARD)
    inverse_coordinate_transformer = functools.partial(
        coordinate_transformer, direction=TransformDirection.INVERSE)
    point_geom_projected = transform(
        forward_coordinate_transformer, point_geom)
    buffer_geom_projected = shapely.buffer(
        point_geom_projected,
        distance=distance_meters
    )
    return transform(
        inverse_coordinate_transformer, buffer_geom_projected)
