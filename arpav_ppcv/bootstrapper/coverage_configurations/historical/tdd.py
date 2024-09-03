from ....schemas.coverages import (
    CoverageConfigurationCreate,
    ConfigurationParameterPossibleValueCreate,
)

_DISPLAY_NAME_ENGLISH = "Average temperature"
_DISPLAY_NAME_ITALIAN = "Temperatura media"
_DESCRIPTION_ENGLISH = "Average of average temperatures"
_DESCRIPTION_ITALIAN = "Media delle temperature medie"


def generate_configurations(
    conf_param_values, variables
) -> list[CoverageConfigurationCreate]:
    return [
        CoverageConfigurationCreate(
            name="tdd_30yr",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="tas",
            wms_main_layer_name="tas",
            thredds_url_pattern="cline_30yr/TDd_1991-2020.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("collection", "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "tas")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("aggregation_period", "annual")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("measure", "anomaly")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_model", "model_ensemble")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("scenario", "rcp26")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("scenario", "rcp45")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("scenario", "rcp85")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "DJF")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "MAM")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "JJA")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("year_period", "SON")
                    ].id
                ),
            ],
        ),
    ]
