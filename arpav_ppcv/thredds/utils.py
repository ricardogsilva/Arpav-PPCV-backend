import logging

import httpx

from . import models

logger = logging.getLogger(__name__)


def build_dataset_service_url(
        dataset_configuration_id: str,
        pattern_fields: dict[str, str],
        *,
        url_path_pattern: str,
        thredds_base_url: str,
        service_url_fragment: str,
) -> str:
    rendered = url_path_pattern.format(
        **{
            "configuration_id": dataset_configuration_id,
            **pattern_fields
        }
    )
    return "/".join((thredds_base_url, service_url_fragment, rendered))


def get_parameter_internal_value(name: str, value: str) -> str:
    if name == "scenario":
        parsed_value = models.ForecastScenario[value.upper()].value.code
    elif name == "year_period":
        parsed_value = models.ForecastYearPeriod[value.upper()].value.code
    else:
        parsed_value = value
    return parsed_value


async def proxy_request(url: str, http_client: httpx.AsyncClient) -> httpx.Response:
    response = await http_client.get(url)
    response.raise_for_status()
    return response
