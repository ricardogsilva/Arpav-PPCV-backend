import datetime as dt
import functools

import httpx
import pyproj
import shapely
import shapely.io
import sqlmodel
from geoalchemy2.shape import to_shape
from pyproj.enums import TransformDirection
from shapely.ops import transform

from . import database
from .config import ArpavPpcvSettings
from .thredds import ncss


def get_coverage_time_series(
        settings: ArpavPpcvSettings,
        session: sqlmodel.Session,
        http_client: httpx.Client,
        coverage_identifier: str,
        coordinates: str,  # a wkt Point
        temporal_range: str,
        include_coverage_data: bool = True,
        include_observation_data: bool = False,
        coverage_data_smoothing: str | None = None,
        observation_data_smoothing: str | None = None,
        include_coverage_uncertainty: bool = False,
        include_coverage_related_data: bool = False,
):
    coverage_configuration_name = coverage_identifier.partition("-")[0]
    coverage_configuration = database.get_coverage_configuration_by_name(
        session, coverage_configuration_name)
    if coverage_configuration is not None:
        start, end = _parse_temporal_range(temporal_range)
        point_geom = shapely.io.from_wkt(coordinates)
        ncss_url = "/".join((
            settings.thredds_server.base_url,
            settings.thredds_server.netcdf_subset_service_url_fragment,
            coverage_configuration.get_thredds_url_fragment(coverage_identifier)
        ))
        coverage_data = ncss.query_dataset(
            http_client,
            thredds_ncss_url=ncss_url,
            variable_name=None,
            longitude=point_geom.x,
            latitude=point_geom.y,
            time_start=start,
            time_end=end,
        )
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
            station_data = []
    else:
        raise ValueError("Invalid coverage identifier")


def _parse_temporal_range(
        raw_temporal_range: str) -> tuple[dt.datetime | None, dt.datetime | None]:
    """Parse a temporal range string.

    The expected format for the input temporal range is described in the
    OGC API - EDR standard:

    https://docs.ogc.org/is/19-086r6/19-086r6.html#req_core_rc-time-response

    Basically it is a string with an optional start datetime and an optional end
    datetime.
    """

    raw_start, raw_end = raw_temporal_range.partition("/")[::2]
    open_interval_pattern = ".."
    if raw_start != open_interval_pattern:
        start = dt.datetime.fromisoformat(raw_start)
    else:
        start = None
    if raw_end != open_interval_pattern:
        end = dt.datetime.fromisoformat(raw_end)
    else:
        end = None
    return start, end


def _get_spatial_buffer(point_geom: shapely.Point, distance_meters: int) -> shapely.Polygon:
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