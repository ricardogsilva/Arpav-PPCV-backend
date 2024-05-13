import datetime as dt
import uuid

import pydantic
from fastapi import Request

from .base import WebResourceList
from ....schemas import coverages as app_models


class ForecastModelScenario(pydantic.BaseModel):
    name: str
    code: str


class ConfigurationParameterPossibleValueRead(pydantic.BaseModel):
    configuration_parameter_name: str
    configuration_parameter_value: str


class CoverageConfigurationReadListItem(pydantic.BaseModel):
    url: pydantic.AnyHttpUrl
    id: uuid.UUID
    name: str
    coverage_id_pattern: str
    possible_values: list[ConfigurationParameterPossibleValueRead]

    @classmethod
    def from_db_instance(
            cls,
            instance: app_models.CoverageConfiguration,
            request: Request,
    ) -> "CoverageConfigurationReadListItem":
        url = request.url_for(
            "get_coverage_configuration",
            **{"coverage_configuration_id": instance.id}
        )
        return cls(
            **instance.model_dump(),
            url=str(url),
            possible_values=[
                ConfigurationParameterPossibleValueRead(
                    configuration_parameter_name=pv.configuration_parameter_value.configuration_parameter.name,
                    configuration_parameter_value=pv.configuration_parameter_value.name
                ) for pv in instance.possible_values
            ]
        )


class CoverageConfigurationReadDetail(CoverageConfigurationReadListItem):
    url: pydantic.AnyHttpUrl
    unit: str
    palette: str
    color_scale_min: float
    color_scale_max: float
    allowed_coverage_identifiers: list[str]

    @classmethod
    def from_db_instance(
            cls,
            instance: app_models.CoverageConfiguration,
            allowed_coverage_identifiers: list[str],
            request: Request,
    ) -> "CoverageConfigurationReadDetail":
        url = request.url_for(
            "get_coverage_configuration",
            **{"coverage_configuration_id": instance.id}
        )
        return cls(
            **instance.model_dump(),
            url=str(url),
            possible_values=[
                ConfigurationParameterPossibleValueRead(
                    configuration_parameter_name=pv.configuration_parameter_value.configuration_parameter.name,
                    configuration_parameter_value=pv.configuration_parameter_value.name
                ) for pv in instance.possible_values
            ],
            allowed_coverage_identifiers=allowed_coverage_identifiers
        )


class CoverageConfigurationList(WebResourceList):
    items: list[CoverageConfigurationReadListItem]
    list_item_type = CoverageConfigurationReadListItem
    path_operation_name = "list_coverage_configurations"


class CoverageIdentifierList(WebResourceList):
    items: list[str]
    list_item_type = str
    path_operation_name = "list_coverage_identifiers"


class ForecastModelScenarioList(WebResourceList):
    items: list[ForecastModelScenario]


class TimeSeriesItem(pydantic.BaseModel):
    value: float
    series: str
    datetime: dt.datetime


class TimeSeries(pydantic.BaseModel):
    values: list[TimeSeriesItem]
