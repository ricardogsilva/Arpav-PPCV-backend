from ....schemas.coverages import (
    CoverageConfigurationCreate,
    ConfigurationParameterPossibleValueCreate,
)

_DISPLAY_NAME_ENGLISH = "Consecutive dry days"
_DISPLAY_NAME_ITALIAN = "Giorni secchi"
_DESCRIPTION_ENGLISH = (
    "Maximum number of consecutive dry days (daily precipitation less than 1 mm)"
)
_DESCRIPTION_ITALIAN = (
    "Numero massimo di giorni consecutivi asciutti (precipitazione giornaliera "
    "inferiore a 1 mm)"
)


def generate_configurations(
    conf_param_values,
) -> list[CoverageConfigurationCreate]:
    return [
        CoverageConfigurationCreate(
            name="cdd_30yr_anomaly_seasonal_agree_model_ensemble",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdd",
            wms_main_layer_name="consecutive_dry_days_index_per_time_period-uncertainty_group",
            wms_secondary_layer_name="consecutive_dry_days_index_per_time_period",
            thredds_url_pattern="ensembletwbc/std/clipped/eca_cdd_an_avgagree_{time_window}_{scenario}_{year_period}_ls_VFVGTAA.nc",
            unit="gg",
            palette="uncert-stippled/div-BrBG-inv",
            color_scale_min=-40,
            color_scale_max=40,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("collection", "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdd")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("aggregation_period", "30yr")
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
                        ("time_window", "tw1")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw2")
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
        CoverageConfigurationCreate(
            name="cdd_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdd",
            wms_main_layer_name="consecutive_dry_days_index_per_time_period",
            thredds_url_pattern="indici5rcm/clipped/eca_cdd_an_EC-EARTH_CCLM4-8-17_{scenario}_{year_period}_{time_window}_ls_VFVGTAA.nc",
            unit="gg",
            palette="default/div-BrBG-inv",
            color_scale_min=-40,
            color_scale_max=40,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("collection", "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdd")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("aggregation_period", "30yr")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("measure", "anomaly")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_model", "ec_earth_cclm_4_8_17")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw1")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw2")
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
        CoverageConfigurationCreate(
            name="cdd_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdd",
            wms_main_layer_name="consecutive_dry_days_index_per_time_period",
            thredds_url_pattern="indici5rcm/clipped/eca_cdd_an_EC-EARTH_RACMO22E_{scenario}_{year_period}_{time_window}_ls_VFVGTAA.nc",
            unit="gg",
            palette="default/div-BrBG-inv",
            color_scale_min=-40,
            color_scale_max=40,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("collection", "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdd")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("aggregation_period", "30yr")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("measure", "anomaly")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_model", "ec_earth_racmo22e")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw1")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw2")
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
        CoverageConfigurationCreate(
            name="cdd_30yr_anomaly_seasonal_model_ec_earth_rca4",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdd",
            wms_main_layer_name="consecutive_dry_days_index_per_time_period",
            thredds_url_pattern="indici5rcm/clipped/eca_cdd_an_EC-EARTH_RCA4_{scenario}_{year_period}_{time_window}_ls_VFVGTAA.nc",
            unit="gg",
            palette="default/div-BrBG-inv",
            color_scale_min=-40,
            color_scale_max=40,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("collection", "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdd")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("aggregation_period", "30yr")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("measure", "anomaly")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_model", "ec_earth_rca4")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw1")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw2")
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
        CoverageConfigurationCreate(
            name="cdd_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdd",
            wms_main_layer_name="consecutive_dry_days_index_per_time_period",
            thredds_url_pattern="indici5rcm/clipped/eca_cdd_an_HadGEM2-ES_RACMO22E_{scenario}_{year_period}_{time_window}_ls_VFVGTAA.nc",
            unit="gg",
            palette="default/div-BrBG-inv",
            color_scale_min=-40,
            color_scale_max=40,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("collection", "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdd")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("aggregation_period", "30yr")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("measure", "anomaly")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_model", "hadgem2_racmo22e")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw1")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw2")
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
        CoverageConfigurationCreate(
            name="cdd_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdd",
            wms_main_layer_name="consecutive_dry_days_index_per_time_period",
            thredds_url_pattern="indici5rcm/clipped/eca_cdd_an_MPI-ESM-LR_REMO2009_{scenario}_{year_period}_{time_window}_ls_VFVGTAA.nc",
            unit="gg",
            palette="default/div-BrBG-inv",
            color_scale_min=-40,
            color_scale_max=40,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("collection", "forecast")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdd")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("aggregation_period", "30yr")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("measure", "anomaly")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_model", "mpi_esm_lr_remo2009")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw1")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("time_window", "tw2")
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


def get_related_map() -> dict[str, list[str]]:
    return {
        "cdd_30yr_anomaly_seasonal_agree_model_ensemble": [
            "cdd_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            "cdd_30yr_anomaly_annual_model_ec_earth_racmo22e",
            "cdd_30yr_anomaly_annual_model_ec_earth_rca4",
            "cdd_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            "cdd_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
        ],
        "cdd_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17": [
            "cdd_30yr_anomaly_seasonal_agree_model_ensemble",
            "cdd_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            "cdd_30yr_anomaly_seasonal_model_ec_earth_rca4",
            "cdd_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
            "cdd_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
        ],
        "cdd_30yr_anomaly_seasonal_model_ec_earth_racmo22e": [
            "cdd_30yr_anomaly_seasonal_agree_model_ensemble",
            "cdd_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            "cdd_30yr_anomaly_seasonal_model_ec_earth_rca4",
            "cdd_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
            "cdd_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
        ],
        "cdd_30yr_anomaly_seasonal_model_ec_earth_rca4": [
            "cdd_30yr_anomaly_seasonal_agree_model_ensemble",
            "cdd_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            "cdd_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            "cdd_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
            "cdd_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
        ],
        "cdd_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e": [
            "cdd_30yr_anomaly_seasonal_agree_model_ensemble",
            "cdd_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            "cdd_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            "cdd_30yr_anomaly_seasonal_model_ec_earth_rca4",
            "cdd_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
        ],
        "cdd_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009": [
            "cdd_30yr_anomaly_seasonal_agree_model_ensemble",
            "cdd_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            "cdd_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            "cdd_30yr_anomaly_seasonal_model_ec_earth_rca4",
            "cdd_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
        ],
    }


def get_uncertainty_map() -> dict[str, tuple[str, str]]:
    return {}
