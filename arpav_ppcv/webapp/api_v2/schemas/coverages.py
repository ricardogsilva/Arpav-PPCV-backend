import uuid
import typing
from typing import Optional

import pydantic
from fastapi import Request

from ....config import (
    ArpavPpcvSettings,
    LOCALE_EN,
    LOCALE_IT,
)
from ....schemas import coverages as app_models
from .base import WebResourceList


class ConfigurationParameterValueEmbeddedInConfigurationParameter(pydantic.BaseModel):
    name: str
    display_name_english: str
    display_name_italian: str
    description_english: str | None
    description_italian: str | None


class ConfigurationParameterReadListItem(pydantic.BaseModel):
    name: str
    display_name_english: str
    display_name_italian: str
    description_english: str | None
    description_italian: str | None
    allowed_values: list[ConfigurationParameterValueEmbeddedInConfigurationParameter]

    @classmethod
    def from_db_instance(
        cls,
        instance: app_models.ConfigurationParameter,
        request: Request,
    ):
        return cls(
            **instance.model_dump(
                exclude={
                    "display_name_english",
                    "display_name_italian",
                }
            ),
            display_name_english=instance.display_name_english or instance.name,
            display_name_italian=instance.display_name_italian or instance.name,
            allowed_values=[
                ConfigurationParameterValueEmbeddedInConfigurationParameter(
                    **pv.model_dump(
                        exclude={
                            "display_name_english",
                            "display_name_italian",
                        }
                    ),
                    display_name_english=pv.display_name_english or pv.name,
                    display_name_italian=pv.display_name_italian or pv.name,
                )
                for pv in instance.allowed_values
            ],
        )


class ConfigurationParameterPossibleValueRead(pydantic.BaseModel):
    configuration_parameter_name: str
    configuration_parameter_display_name_english: str
    configuration_parameter_display_name_italian: str
    configuration_parameter_value: str


class CoverageConfigurationReadListItem(pydantic.BaseModel):
    url: pydantic.AnyHttpUrl
    id: uuid.UUID
    name: str
    display_name_english: str
    display_name_italian: str
    wms_main_layer_name: str | None
    wms_secondary_layer_name: str | None
    coverage_id_pattern: str
    possible_values: list[ConfigurationParameterPossibleValueRead]

    @classmethod
    def from_db_instance(
        cls,
        instance: app_models.CoverageConfiguration,
        request: Request,
    ) -> "CoverageConfigurationReadListItem":
        url = request.url_for(
            "get_coverage_configuration", **{"coverage_configuration_id": instance.id}
        )
        return cls(
            **instance.model_dump(
                exclude={
                    "display_name_english",
                    "display_name_italian",
                }
            ),
            display_name_english=instance.display_name_english or instance.name,
            display_name_italian=instance.display_name_italian or instance.name,
            url=str(url),
            possible_values=[
                ConfigurationParameterPossibleValueRead(
                    configuration_parameter_name=pv.configuration_parameter_value.configuration_parameter.name,
                    configuration_parameter_display_name_english=(
                        pv.configuration_parameter_value.configuration_parameter.display_name_english
                        or pv.configuration_parameter_value.configuration_parameter.name
                    ),
                    configuration_parameter_display_name_italian=(
                        pv.configuration_parameter_value.configuration_parameter.display_name_italian
                        or pv.configuration_parameter_value.configuration_parameter.name
                    ),
                    configuration_parameter_value=pv.configuration_parameter_value.name,
                )
                for pv in instance.possible_values
            ],
        )


class CoverageConfigurationReadDetail(CoverageConfigurationReadListItem):
    url: pydantic.AnyHttpUrl
    unit: str
    palette: str
    color_scale_min: float
    color_scale_max: float
    allowed_coverage_identifiers: list[str]
    description_english: str | None
    description_italian: str | None

    @classmethod
    def from_db_instance(
        cls,
        instance: app_models.CoverageConfiguration,
        allowed_coverage_identifiers: list[str],
        request: Request,
    ) -> "CoverageConfigurationReadDetail":
        url = request.url_for(
            "get_coverage_configuration", **{"coverage_configuration_id": instance.id}
        )
        return cls(
            **instance.model_dump(),
            url=str(url),
            possible_values=[
                ConfigurationParameterPossibleValueRead(
                    configuration_parameter_name=pv.configuration_parameter_value.configuration_parameter.name,
                    configuration_parameter_display_name_english=(
                        pv.configuration_parameter_value.configuration_parameter.display_name_english
                        or pv.configuration_parameter_value.configuration_parameter.name
                    ),
                    configuration_parameter_display_name_italian=(
                        pv.configuration_parameter_value.configuration_parameter.display_name_italian
                        or pv.configuration_parameter_value.configuration_parameter.name
                    ),
                    configuration_parameter_value=pv.configuration_parameter_value.name,
                )
                for pv in instance.possible_values
            ],
            allowed_coverage_identifiers=allowed_coverage_identifiers,
        )


class CoverageConfigurationList(WebResourceList):
    items: list[CoverageConfigurationReadListItem]
    list_item_type = CoverageConfigurationReadListItem
    path_operation_name = "list_coverage_configurations"


class CoverageIdentifierReadListItem(pydantic.BaseModel):
    identifier: str
    related_coverage_configuration_url: str
    wms_base_url: str
    wms_main_layer_name: str | None = None
    wms_secondary_layer_name: str | None = None
    time_series_base_url: str
    uses_different_data_for_time_series: bool = False
    possible_values: list[ConfigurationParameterPossibleValueRead]

    @classmethod
    def from_db_instance(
        cls,
        instance: app_models.CoverageInternal,
        settings: ArpavPpcvSettings,
        related_time_series_coverage: Optional[app_models.CoverageInternal],
        request: Request,
    ) -> "CoverageIdentifierReadListItem":
        thredds_url_fragment = instance.configuration.get_thredds_url_fragment(
            instance.identifier
        )
        wms_base_url = "/".join(
            (
                settings.thredds_server.base_url,
                settings.thredds_server.wms_service_url_fragment,
                thredds_url_fragment,
            )
        )
        if related_time_series_coverage is not None:
            time_series_id = related_time_series_coverage.identifier
            uses_different_data_for_time_series = True
        else:
            time_series_id = instance.identifier
            uses_different_data_for_time_series = False

        return cls(
            identifier=instance.identifier,
            wms_base_url=wms_base_url,
            wms_main_layer_name=instance.configuration.wms_main_layer_name,
            wms_secondary_layer_name=instance.configuration.wms_secondary_layer_name,
            time_series_base_url=str(
                request.url_for("get_time_series", coverage_identifier=time_series_id)
            ),
            uses_different_data_for_time_series=uses_different_data_for_time_series,
            related_coverage_configuration_url=str(
                request.url_for(
                    "get_coverage_configuration",
                    coverage_configuration_id=instance.configuration.id,
                )
            ),
            possible_values=[
                ConfigurationParameterPossibleValueRead(
                    configuration_parameter_name=pv.configuration_parameter_value.configuration_parameter.name,
                    configuration_parameter_display_name_english=(
                        pv.configuration_parameter_value.configuration_parameter.display_name_english
                        or pv.configuration_parameter_value.configuration_parameter.name
                    ),
                    configuration_parameter_display_name_italian=(
                        pv.configuration_parameter_value.configuration_parameter.display_name_italian
                        or pv.configuration_parameter_value.configuration_parameter.name
                    ),
                    configuration_parameter_value=pv.configuration_parameter_value.name,
                )
                for pv in instance.configuration.retrieve_used_values(
                    instance.identifier
                )
            ],
        )


class CoverageIdentifierList(WebResourceList):
    items: list[CoverageIdentifierReadListItem]
    path_operation_name = "list_coverage_identifiers"

    @classmethod
    def from_items(
        cls,
        items: typing.Sequence[app_models.CoverageInternal],
        request: Request,
        *,
        settings: ArpavPpcvSettings,
        limit: int,
        offset: int,
        filtered_total: int,
        unfiltered_total: int,
    ):
        return cls(
            meta=cls._get_meta(len(items), unfiltered_total, filtered_total),
            links=cls._get_list_links(
                request, limit, offset, filtered_total, len(items)
            ),
            items=[
                CoverageIdentifierReadListItem.from_db_instance(i, settings, request)
                for i in items
            ],
        )


class ConfigurationParameterList(WebResourceList):
    items: list[ConfigurationParameterReadListItem]
    list_item_type = ConfigurationParameterReadListItem
    path_operation_name = "list_configuration_parameters"


class ConfigurationParameterMenuTranslation(pydantic.BaseModel):
    name: dict[str, str]
    description: dict[str, str]


class ForecastMenuTranslations(pydantic.BaseModel):
    variable: dict[str, ConfigurationParameterMenuTranslation]
    aggregation_period: dict[str, ConfigurationParameterMenuTranslation]
    measure: dict[str, ConfigurationParameterMenuTranslation]
    other_parameters: dict[str, dict[str, ConfigurationParameterMenuTranslation]]

    @classmethod
    def from_items(
        cls, variable_menu_trees: typing.Sequence[app_models.ForecastVariableMenuTree]
    ):
        result = {}
        for variable_menu_tree in variable_menu_trees:
            variable_cp = variable_menu_tree["climatological_variable"]
            aggregation_period_cp = variable_menu_tree["aggregation_period"]
            measure_cp = variable_menu_tree["measure"]
            vars = result.setdefault("variable", {})
            vars[variable_cp.name] = ConfigurationParameterMenuTranslation(
                name={
                    LOCALE_EN.language: variable_cp.display_name_english,
                    LOCALE_IT.language: variable_cp.display_name_english,
                },
                description={
                    LOCALE_EN.language: variable_cp.description_english,
                    LOCALE_IT.language: variable_cp.description_italian,
                },
            )
            aggreg_periods = result.setdefault("aggregation_period", {})
            aggreg_periods[
                aggregation_period_cp.name
            ] = ConfigurationParameterMenuTranslation(
                name={
                    LOCALE_EN.language: aggregation_period_cp.display_name_english,
                    LOCALE_IT.language: aggregation_period_cp.display_name_english,
                },
                description={
                    LOCALE_EN.language: aggregation_period_cp.description_english,
                    LOCALE_IT.language: aggregation_period_cp.description_italian,
                },
            )
            measures = result.setdefault("measure", {})
            measures[measure_cp.name] = ConfigurationParameterMenuTranslation(
                name={
                    LOCALE_EN.language: measure_cp.display_name_english,
                    LOCALE_IT.language: measure_cp.display_name_english,
                },
                description={
                    LOCALE_EN.language: measure_cp.description_english,
                    LOCALE_IT.language: measure_cp.description_italian,
                },
            )
            others = result.setdefault("other_parameters", {})
            for combination_info in variable_menu_tree["combinations"].values():
                cp = combination_info["configuration_parameter"]
                param_ = others.setdefault(cp.name, {})
                for cpv in cp.allowed_values:
                    param_[cpv.name] = ConfigurationParameterMenuTranslation(
                        name={
                            LOCALE_EN.language: cpv.display_name_english,
                            LOCALE_IT.language: cpv.display_name_english,
                        },
                        description={
                            LOCALE_EN.language: cpv.description_english,
                            LOCALE_IT.language: cpv.description_italian,
                        },
                    )
        return cls(
            variable=result["variable"],
            aggregation_period=result["aggregation_period"],
            measure=result["measure"],
            other_parameters=result["other_parameters"],
        )


class VariableCombinations(pydantic.BaseModel):
    variable: str
    aggregation_period: str
    measure: str
    other_parameters: dict[str, list[str]]

    @classmethod
    def from_items(cls, menu_tree: app_models.ForecastVariableMenuTree):
        combinations = {}
        for param_name, param_combinations in menu_tree["combinations"].items():
            combinations[param_name] = []
            for valid_value in param_combinations["values"]:
                combinations[param_name].append(valid_value.name)

        return cls(
            variable=menu_tree["climatological_variable"].name,
            aggregation_period=menu_tree["aggregation_period"].name,
            measure=menu_tree["measure"].name,
            other_parameters=combinations,
        )


class ForecastVariableCombinationsList(pydantic.BaseModel):
    combinations: list[VariableCombinations]
    translations: ForecastMenuTranslations
