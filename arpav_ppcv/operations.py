import datetime as dt
import functools
import io
from typing import Optional

import httpx
import pandas as pd
import pyproj
import shapely
import shapely.io
import sqlmodel
from dateutil.parser import isoparse
from geoalchemy2.shape import to_shape
from pyproj.enums import TransformDirection
from shapely.ops import transform

from . import database
from .schemas import (
    coverages,
    observations,
)
from .config import ArpavPpcvSettings
from .thredds import ncss


def get_coverage_time_series(
        settings: ArpavPpcvSettings,
        session: sqlmodel.Session,
        http_client: httpx.Client,
        coverage_configuration: coverages.CoverageConfiguration,
        coverage_identifier: str,
        point_geom: shapely.Point,
        temporal_range: str,
        include_coverage_data: bool = True,
        include_observation_data: bool = False,
        coverage_data_smoothing: coverages.CoverageDataSmoothingStrategy | None = None,
        observation_data_smoothing: observations.ObservationDataSmoothingStrategy | None = None,
        include_coverage_uncertainty: bool = False,
        include_coverage_related_data: bool = False,
) -> dict[str, pd.DataFrame]:
    start, end = _parse_temporal_range(temporal_range)
    ncss_url = "/".join((
        settings.thredds_server.base_url,
        settings.thredds_server.netcdf_subset_service_url_fragment,
        coverage_configuration.get_thredds_url_fragment(coverage_identifier)
    ))
    raw_coverage_data = ncss.query_dataset(
        http_client,
        thredds_ncss_url=ncss_url,
        variable_name=coverage_configuration.netcdf_main_dataset_name,
        longitude=point_geom.x,
        latitude=point_geom.y,
        time_start=start,
        time_end=end,
    )
    measurements = {}
    if raw_coverage_data is not None:
        if include_coverage_data:
            coverage_data = _process_coverage_data(
                raw_coverage_data,
                coverage_configuration,
                coverage_data_smoothing,
                start,
                end
            )
            measurements[coverage_configuration.name] = coverage_data
        if include_observation_data:
            point_buffer_geom = _get_spatial_buffer(
                point_geom, settings.nearest_station_radius_meters)
            nearby_stations = database.collect_all_stations(
                session, polygon_intersection_filter=point_buffer_geom)
            if len(nearby_stations) > 0:
                sorted_stations = sorted(
                    nearby_stations, key=lambda s: to_shape(s.geom).distance(point_geom))
                # order nearby stations by distance and then iterate through them in order to
                # try to get measurements for the relevant variable and temporal aggregation
                for station in sorted_stations:
                    ...
            else:
                ...
    else:
        raise RuntimeError("Could not retrieve coverage data")
    return measurements


def _process_coverage_data(
        raw_data: str,
        coverage_configuration: coverages.CoverageConfiguration,
        data_smoothing: Optional[coverages.CoverageDataSmoothingStrategy],
        time_start: Optional[dt.datetime],
        time_end: Optional[dt.datetime],
) -> pd.DataFrame:
    # - filter out columns we don't care about
    # - filter out values outside the temporal range
    df = pd.read_csv(io.StringIO(raw_data), parse_dates=["time"])

    # get name of the colum that holds the main variable
    variable_name = coverage_configuration.netcdf_main_dataset_name
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
        df = df.rename(columns={col_name: variable_name})

        # - filter out values outside the temporal range
        df.set_index("time", inplace=True)
        if time_start is not None:
            df = df[time_start:]
        if time_end is not None:
            df = df[:time_end]

        if data_smoothing is not None:
            ...
    return df


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