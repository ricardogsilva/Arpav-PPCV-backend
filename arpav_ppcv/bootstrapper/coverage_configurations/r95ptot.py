"""
- [x] r95ptot_30yr_anomaly_annual_agree_model_ensemble
- [x] r95ptot_30yr_anomaly_annual_model_ec_earth_cclm4_8_17
- [x] r95ptot_30yr_anomaly_annual_model_ec_earth_racmo22e
- [x] r95ptot_30yr_anomaly_annual_model_ec_earth_rca4
- [x] r95ptot_30yr_anomaly_annual_model_hadgem2_es_racmo22e
- [x] r95ptot_30yr_anomaly_annual_model_mpi_esm_lr_remo2009

"""
from ...schemas.coverages import (
    CoverageConfigurationCreate,
    ConfigurationParameterPossibleValueCreate,
)


def generate_configurations(
    conf_param_values,
) -> list[CoverageConfigurationCreate]:
    return [
        CoverageConfigurationCreate(
            name="r95ptot_30yr_anomaly_annual_agree_model_ensemble",
            netcdf_main_dataset_name="r95ptot",
            wms_main_layer_name="r95ptot-uncertainty_group",
            thredds_url_pattern="ensembletwbc/std/clipped/pr_change_cumulative_check_avgagree_{time_window}_{scenario}_{year_period}_VFVGTAA.nc",
            unit="%",
            palette="uncert-stippled/div-BrBG",
            color_scale_min=-160,
            color_scale_max=160,
            possible_values=[
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
            name="r95ptot_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="r95ptot",
            wms_main_layer_name="r95ptot",
            thredds_url_pattern="indici5rcm/clipped/pr_change_cumulative_EC-EARTH_CCLM4-8-17_{year_period}_{scenario}_{time_window}_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBG",
            color_scale_min=-160,
            color_scale_max=160,
            possible_values=[
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
            name="r95ptot_30yr_anomaly_annual_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="r95ptot",
            wms_main_layer_name="r95ptot",
            thredds_url_pattern="indici5rcm/clipped/pr_change_cumulative_EC-EARTH_RACMO22E_{year_period}_{scenario}_{time_window}_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBG",
            color_scale_min=-160,
            color_scale_max=160,
            possible_values=[
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
            name="r95ptot_30yr_anomaly_annual_model_ec_earth_rca4",
            netcdf_main_dataset_name="r95ptot",
            wms_main_layer_name="r95ptot",
            thredds_url_pattern="indici5rcm/clipped/pr_change_cumulative_EC-EARTH_RCA4_{year_period}_{scenario}_{time_window}_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBG",
            color_scale_min=-160,
            color_scale_max=160,
            possible_values=[
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
            name="r95ptot_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="r95ptot",
            wms_main_layer_name="r95ptot",
            thredds_url_pattern="indici5rcm/clipped/pr_change_cumulative_HadGEM2-ES_RACMO22E_{year_period}_{scenario}_{time_window}_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBG",
            color_scale_min=-160,
            color_scale_max=160,
            possible_values=[
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
            name="r95ptot_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="r95ptot",
            wms_main_layer_name="r95ptot",
            thredds_url_pattern="indici5rcm/clipped/pr_change_cumulative_MPI-ESM-LR_REMO2009_{year_period}_{scenario}_{time_window}_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBG",
            color_scale_min=-160,
            color_scale_max=160,
            possible_values=[
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
        "r95ptot_30yr_anomaly_annual_agree_model_ensemble": [
            "r95ptot_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            "r95ptot_30yr_anomaly_annual_model_ec_earth_racmo22e",
            "r95ptot_30yr_anomaly_annual_model_ec_earth_rca4",
            "r95ptot_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            "r95ptot_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
        ],
        "r95ptot_30yr_anomaly_annual_model_ec_earth_cclm4_8_17": [
            "r95ptot_30yr_anomaly_annual_agree_model_ensemble",
            "r95ptot_30yr_anomaly_annual_model_ec_earth_racmo22e",
            "r95ptot_30yr_anomaly_annual_model_ec_earth_rca4",
            "r95ptot_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            "r95ptot_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
        ],
        "r95ptot_30yr_anomaly_annual_model_ec_earth_racmo22e": [
            "r95ptot_30yr_anomaly_annual_agree_model_ensemble",
            "r95ptot_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            "r95ptot_30yr_anomaly_annual_model_ec_earth_rca4",
            "r95ptot_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            "r95ptot_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
        ],
        "r95ptot_30yr_anomaly_annual_model_ec_earth_rca4": [
            "r95ptot_30yr_anomaly_annual_agree_model_ensemble",
            "r95ptot_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            "r95ptot_30yr_anomaly_annual_model_ec_earth_racmo22e",
            "r95ptot_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            "r95ptot_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
        ],
        "r95ptot_30yr_anomaly_annual_model_hadgem2_es_racmo22e": [
            "r95ptot_30yr_anomaly_annual_agree_model_ensemble",
            "r95ptot_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            "r95ptot_30yr_anomaly_annual_model_ec_earth_racmo22e",
            "r95ptot_30yr_anomaly_annual_model_ec_earth_rca4",
            "r95ptot_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
        ],
        "r95ptot_30yr_anomaly_annual_model_mpi_esm_lr_remo2009": [
            "r95ptot_30yr_anomaly_annual_agree_model_ensemble",
            "r95ptot_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            "r95ptot_30yr_anomaly_annual_model_ec_earth_racmo22e",
            "r95ptot_30yr_anomaly_annual_model_ec_earth_rca4",
            "r95ptot_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
        ],
    }


def get_uncertainty_map() -> dict[str, tuple[str, str]]:
    return {}
