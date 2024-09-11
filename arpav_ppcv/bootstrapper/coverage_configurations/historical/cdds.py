from ....schemas.coverages import (
    CoverageConfigurationCreate,
    ConfigurationParameterPossibleValueCreate,
)

_DISPLAY_NAME_ENGLISH = "Cooling degree days"
_DISPLAY_NAME_ITALIAN = "Gradi giorno di raffrescamento"
_DESCRIPTION_ENGLISH = (
    "Sum of the average daily temperature minus 21°C if the average "
    "daily temperature is greater than 24°C."
)
_DESCRIPTION_ITALIAN = (
    "Somma della temperatura media giornaliera meno 21°C se la "
    "temperatura media giornaliera è maggiore di 24°C."
)
_HISTORICAL_COLLECTION = "historical"
_OBSERVATION_VARIABLE = "cdds"
_UNIT = "CDD ºC"
_COLOR_SCALE_MIN = 0
_COLOR_SCALE_MAX = 320


def generate_configurations(
    conf_param_values, variables
) -> list[CoverageConfigurationCreate]:
    cov_confs = [
        CoverageConfigurationCreate(
            name="cdds_30yr_yearly",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="{observation_year_period}_avg",
            wms_main_layer_name="{observation_year_period}_avg",
            thredds_url_pattern="cline_30yr/CDD_jrc_1991-2020.nc",
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
            name="cdds_annual_yearly",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="CDD_jrc",
            wms_main_layer_name="CDD_jrc",
            thredds_url_pattern="cline_yr/CDD_jrc_{observation_year_period}_1992-2023_py85.nc",
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
        ),
    ]
    return cov_confs