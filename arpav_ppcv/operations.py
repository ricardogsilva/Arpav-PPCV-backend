import datetime as dt

import httpx
import shapely.io
import sqlmodel

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
        geom = shapely.io.from_wkt(coordinates)

        ncss_url = "/".join((
            settings.thredds_server.base_url,
            settings.thredds_server.netcdf_subset_service_url_fragment,
            coverage_configuration.get_thredds_url_fragment(coverage_identifier)
        ))

        coverage_data = ncss.query_dataset(
            http_client,
            thredds_ncss_url=ncss_url,
            variable_name=None,
            longitude=geom.x,
            latitude=geom.y,
            time_start=start,
            time_end=end,
        )
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
