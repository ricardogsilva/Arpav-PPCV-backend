"""Utilities for interacting with the THREDDS NetCDF Subset Service (NCSS).

Get more detail about NCSS at:

https://docs.unidata.ucar.edu/tds/current/userguide/netcdf_subset_service_ref.html

"""
import datetime as dt
import logging
import xml.etree.ElementTree as etree

import httpx
import shapely

from ..exceptions import CoverageDataRetrievalError
from . import models

logger = logging.getLogger(__name__)


def get_dataset_description(
        http_client: httpx.Client,
        thredds_ncss_url: str,
) -> models.ThreddsDatasetDescription:
    response = http_client.get(f"{thredds_ncss_url}/dataset.xml")
    response.raise_for_status()
    root = etree.fromstring(response.text)
    variables = []
    for var_info in root.findall("./gridSet/grid"):
        variables.append(
            models.ThreddsDatasetDescriptionVariable(
                name=var_info.get("name"),
                description=var_info.get("desc"),
                units=var_info.findall("./*[@name='units']")[0].get("value")
            )
        )
    time_span_el = root.findall("./TimeSpan")[0]
    temporal_bounds = models.ThreddsDatasetDescriptionTemporalBounds(
        start=dt.datetime.fromisoformat(time_span_el.findall("./begin")[0].text),
        end=dt.datetime.fromisoformat(time_span_el.findall("./end")[0].text),
    )
    lat_lon_el = root.findall("./LatLonBox")[0]
    spatial_bounds = shapely.box(
        xmin=float(lat_lon_el.findall("./west")[0].text),
        ymin=float(lat_lon_el.findall("./south")[0].text),
        xmax=float(lat_lon_el.findall("./east")[0].text),
        ymax=float(lat_lon_el.findall("./north")[0].text)
    )
    return models.ThreddsDatasetDescription(
        variables=variables,
        spatial_bounds=spatial_bounds,
        temporal_bounds=temporal_bounds
    )


def query_dataset(
        http_client: httpx.Client,
        thredds_ncss_url: str,
        variable_name: str,
        longitude: float,
        latitude: float,
        time_start: dt.datetime | None = None,
        time_end: dt.datetime | None = None,
) -> str:
    """Query THREDDS for the specified variable."""
    if time_start is None or time_end is None:
        temporal_parameters = {
            "time": "all",
        }
    else:
        temporal_parameters = {
            "time_start": time_start.isoformat(),
            "time_end": time_end.isoformat(),
        }
    response = http_client.get(
        thredds_ncss_url,
        params={
            "var": variable_name,
            "latitude": latitude,
            "longitude": longitude,
            "accept": "CSV",
            **temporal_parameters,
        }
    )
    try:
        response.raise_for_status()
    except httpx.HTTPError as err:
        logger.exception(msg="Could not retrieve data")
        logger.debug(f"upstream NCSS error: {response.content}")
        raise CoverageDataRetrievalError() from err
    else:
        result = response.text
    return result
