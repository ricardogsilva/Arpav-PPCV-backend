from ....schemas.base import ObservationAggregationType
from ....schemas.coverages import (
    CoverageConfigurationCreate,
    ConfigurationParameterPossibleValueCreate,
)

_DISPLAY_NAME_ENGLISH = "Precipitation"
_DISPLAY_NAME_ITALIAN = "Precipitazione"
_DESCRIPTION_ENGLISH = "Daily precipitation near the ground"
_DESCRIPTION_ITALIAN = "Precipitazione giornaliera vicino al suolo"
_HISTORICAL_COLLECTION = "historical"
_OBSERVATION_VARIABLE = "prcptot"
_UNIT = "mm"
_COLOR_SCALE_MIN = 300
_COLOR_SCALE_MAX = 1300
_RELATED_OBSERVATION_VARIABLE_NAME = "PRCPTOT"


def generate_configurations(
    conf_param_values, variables
) -> list[CoverageConfigurationCreate]:
    cov_confs = [
        CoverageConfigurationCreate(
            name="prcptot_30yr_yearly",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="{observation_year_period}_avg",
            wms_main_layer_name="{observation_year_period}_avg",
            thredds_url_pattern="cline_30yr/PRCPTOT_1991-2020.nc",
            unit=_UNIT,
            palette="default/seq-YlOrRd",
            color_scale_min=_COLOR_SCALE_MIN,
            color_scale_max=_COLOR_SCALE_MAX,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("collection", _HISTORICAL_COLLECTION)
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("observation_variable", _OBSERVATION_VARIABLE)
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("aggregation_period", "30yr")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("measure", "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("observation_year_period", "A00")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="prcptot_annual_yearly",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="PRCPTOT",
            wms_main_layer_name="PRCPTOT",
            thredds_url_pattern="cline_yr/PRCPTOT_{observation_year_period}_1992-2023_py85.nc",
            unit=_UNIT,
            palette="default/seq-YlOrRd",
            color_scale_min=_COLOR_SCALE_MIN,
            color_scale_max=_COLOR_SCALE_MAX,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("collection", _HISTORICAL_COLLECTION)
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("observation_variable", _OBSERVATION_VARIABLE)
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("aggregation_period", "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("measure", "absolute")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("observation_year_period", "A00")
                    ].id
                ),
            ],
            observation_variable_id=(
                v.id
                if (v := variables.get(_RELATED_OBSERVATION_VARIABLE_NAME)) is not None
                else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
    ]
    for season_name, season_id, duration in (
        ("winter", "S01", "1992-2024"),
        ("spring", "S02", "1992-2024"),
        ("summer", "S03", "1992-2023"),
        ("autumn", "S04", "1992-2023"),
    ):
        cov_confs.extend(
            [
                CoverageConfigurationCreate(
                    name=f"prcptot_30yr_{season_name}",
                    display_name_english=_DISPLAY_NAME_ENGLISH,
                    display_name_italian=_DISPLAY_NAME_ITALIAN,
                    description_english=_DESCRIPTION_ENGLISH,
                    description_italian=_DESCRIPTION_ITALIAN,
                    netcdf_main_dataset_name="{observation_year_period}_avg",
                    wms_main_layer_name="{observation_year_period}_avg",
                    thredds_url_pattern="cline_30yr/PRCPTOT_1991-2020.nc",
                    unit=_UNIT,
                    palette="default/seq-YlOrRd",
                    color_scale_min=_COLOR_SCALE_MIN,
                    color_scale_max=_COLOR_SCALE_MAX,
                    possible_values=[
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("collection", _HISTORICAL_COLLECTION)
                            ].id
                        ),
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("observation_variable", _OBSERVATION_VARIABLE)
                            ].id
                        ),
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("aggregation_period", "30yr")
                            ].id
                        ),
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("measure", "absolute")
                            ].id
                        ),
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("observation_year_period", season_id)
                            ].id
                        ),
                    ],
                ),
                CoverageConfigurationCreate(
                    name=f"prcptot_annual_{season_name}",
                    display_name_english=_DISPLAY_NAME_ENGLISH,
                    display_name_italian=_DISPLAY_NAME_ITALIAN,
                    description_english=_DESCRIPTION_ENGLISH,
                    description_italian=_DESCRIPTION_ITALIAN,
                    netcdf_main_dataset_name="PRCPTOT",
                    wms_main_layer_name="PRCPTOT",
                    thredds_url_pattern=(
                        f"cline_yr/PRCPTOT_{{observation_year_period}}_{duration}_py85.nc"
                    ),
                    unit=_UNIT,
                    palette="default/seq-YlOrRd",
                    color_scale_min=_COLOR_SCALE_MIN,
                    color_scale_max=_COLOR_SCALE_MAX,
                    possible_values=[
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("collection", _HISTORICAL_COLLECTION)
                            ].id
                        ),
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("observation_variable", _OBSERVATION_VARIABLE)
                            ].id
                        ),
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("aggregation_period", "annual")
                            ].id
                        ),
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("measure", "absolute")
                            ].id
                        ),
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("observation_year_period", season_id)
                            ].id
                        ),
                    ],
                    observation_variable_id=(
                        v.id
                        if (v := variables.get(_RELATED_OBSERVATION_VARIABLE_NAME))
                        is not None
                        else None
                    ),
                    observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
                ),
            ]
        )
    for month_name, month_id, duration in (
        ("january", "M01", "1992-2024"),
        ("february", "M02", "1992-2024"),
        ("march", "M03", "1992-2024"),
        ("april", "M04", "1992-2024"),
        ("may", "M05", "1992-2024"),
        ("june", "M06", "1992-2024"),
        ("july", "M07", "1992-2024"),
        ("august", "M08", "1992-2023"),
        ("september", "M09", "1992-2023"),
        ("october", "M10", "1992-2023"),
        ("november", "M11", "1992-2023"),
        ("december", "M12", "1992-2023"),
    ):
        cov_confs.extend(
            [
                CoverageConfigurationCreate(
                    name=f"prcptot_30yr_{month_name}",
                    display_name_english=_DISPLAY_NAME_ENGLISH,
                    display_name_italian=_DISPLAY_NAME_ITALIAN,
                    description_english=_DESCRIPTION_ENGLISH,
                    description_italian=_DESCRIPTION_ITALIAN,
                    netcdf_main_dataset_name="{observation_year_period}_avg",
                    wms_main_layer_name="{observation_year_period}_avg",
                    thredds_url_pattern="cline_30yr/PRCPTOT_1991-2020.nc",
                    unit=_UNIT,
                    palette="default/seq-YlOrRd",
                    color_scale_min=_COLOR_SCALE_MIN,
                    color_scale_max=_COLOR_SCALE_MAX,
                    possible_values=[
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("collection", _HISTORICAL_COLLECTION)
                            ].id
                        ),
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("observation_variable", _OBSERVATION_VARIABLE)
                            ].id
                        ),
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("aggregation_period", "30yr")
                            ].id
                        ),
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("measure", "absolute")
                            ].id
                        ),
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("observation_year_period", month_id)
                            ].id
                        ),
                    ],
                ),
                CoverageConfigurationCreate(
                    name=f"prcptot_annual_{month_name}",
                    display_name_english=_DISPLAY_NAME_ENGLISH,
                    display_name_italian=_DISPLAY_NAME_ITALIAN,
                    description_english=_DESCRIPTION_ENGLISH,
                    description_italian=_DESCRIPTION_ITALIAN,
                    netcdf_main_dataset_name="PRCPTOT",
                    wms_main_layer_name="PRCPTOT",
                    thredds_url_pattern=(
                        f"cline_yr/PRCPTOT_{{observation_year_period}}_{duration}_py85.nc"
                    ),
                    unit=_UNIT,
                    palette="default/seq-YlOrRd",
                    color_scale_min=_COLOR_SCALE_MIN,
                    color_scale_max=_COLOR_SCALE_MAX,
                    possible_values=[
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("collection", _HISTORICAL_COLLECTION)
                            ].id
                        ),
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("observation_variable", _OBSERVATION_VARIABLE)
                            ].id
                        ),
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("aggregation_period", "annual")
                            ].id
                        ),
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("measure", "absolute")
                            ].id
                        ),
                        ConfigurationParameterPossibleValueCreate(
                            configuration_parameter_value_id=conf_param_values[
                                ("observation_year_period", month_id)
                            ].id
                        ),
                    ],
                    observation_variable_id=(
                        v.id
                        if (v := variables.get(_RELATED_OBSERVATION_VARIABLE_NAME))
                        is not None
                        else None
                    ),
                    observation_variable_aggregation_type=ObservationAggregationType.MONTHLY,
                ),
            ]
        )
    return cov_confs
