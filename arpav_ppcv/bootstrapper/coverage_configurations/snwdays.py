"""
- [x] snwdays_annual_absolute_model_ensemble
- [x] snwdays_annual_absolute_model_ensemble_upper_uncertainty
- [x] snwdays_annual_absolute_model_ensemble_lower_uncertainty
- [x] snwdays_annual_absolute_model_ec_earth_cclm4_8_17
- [x] snwdays_annual_absolute_model_ec_earth_racmo22e
- [x] snwdays_annual_absolute_model_ec_earth_rca4
- [x] snwdays_annual_absolute_model_hadgem2_es_racmo22e
- [x] snwdays_annual_absolute_model_mpi_esm_lr_remo2009

- [x] 30year anomaly
  - [x] snwdays_30yr_anomaly_annual_agree_model_ensemble
  - [x] snwdays_30yr_anomaly_annual_model_ec_earth_cclm4_8_17
  - [x] snwdays_30yr_anomaly_annual_model_ec_earth_racmo22e
  - [x] snwdays_30yr_anomaly_annual_model_ec_earth_rca4
  - [x] snwdays_30yr_anomaly_annual_model_hadgem2_es_racmo22e
  - [x] snwdays_30yr_anomaly_annual_model_mpi_esm_lr_remo2009
"""
from ...schemas.coverages import (
    CoverageConfigurationCreate,
    ConfigurationParameterPossibleValueCreate,
)


def generate_snwdays_configurations(
    conf_param_values,
) -> list[CoverageConfigurationCreate]:
    return [
        CoverageConfigurationCreate(
            name="snwdays_annual_absolute_model_ensemble",
            netcdf_main_dataset_name="snwdays",
            thredds_url_pattern="ensymbc/std/clipped/snwdays_1mm_2oc_avg_ts19762100_{scenario}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=100,
            possible_values=[
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
            ],
        ),
        CoverageConfigurationCreate(
            name="snwdays_annual_absolute_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="snwdays",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ymbc/clipped/snwdays_1mm_2oc_EC-EARTH_CCLM4-8-17_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=100,
            possible_values=[
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
            ],
        ),
        CoverageConfigurationCreate(
            name="snwdays_annual_absolute_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="snwdays",
            thredds_url_pattern="EC-EARTH_RACMO22Eymbc/clipped/snwdays_1mm_2oc_EC-EARTH_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=100,
            possible_values=[
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
            ],
        ),
        CoverageConfigurationCreate(
            name="snwdays_annual_absolute_model_ec_earth_rca4",
            netcdf_main_dataset_name="snwdays",
            thredds_url_pattern="EC-EARTH_RCA4ymbc/clipped/snwdays_1mm_2oc_EC-EARTH_RCA4_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=100,
            possible_values=[
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
            ],
        ),
        CoverageConfigurationCreate(
            name="snwdays_annual_absolute_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="snwdays",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eymbc/clipped/snwdays_1mm_2oc_HadGEM2-ES_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=100,
            possible_values=[
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
            ],
        ),
        CoverageConfigurationCreate(
            name="snwdays_annual_absolute_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="snwdays",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ymbc/clipped/snwdays_1mm_2oc_MPI-ESM-LR_REMO2009_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=100,
            possible_values=[
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
            ],
        ),
        CoverageConfigurationCreate(
            name="snwdays_annual_absolute_model_ensemble_upper_uncertainty",
            netcdf_main_dataset_name="snwdays_stdup",
            thredds_url_pattern="ensymbc/std/clipped/snwdays_1mm_2oc_stdup_ts19762100_{scenario}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=100,
            possible_values=[
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
            ],
        ),
        CoverageConfigurationCreate(
            name="snwdays_annual_absolute_model_ensemble_lower_uncertainty",
            netcdf_main_dataset_name="snwdays_stddown",
            thredds_url_pattern="ensymbc/std/clipped/snwdays_1mm_2oc_stddown_ts19762100_{scenario}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=100,
            possible_values=[
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
            ],
        ),
        # ---
        CoverageConfigurationCreate(
            name="snwdays_30yr_anomaly_annual_agree_model_ensemble",
            netcdf_main_dataset_name="snwdays",
            thredds_url_pattern="ensembletwbc/std/clipped/snwdays_an_1mm_2oc_avgagree_{time_window}_{scenario}_ls_VFVG.nc",
            unit="gg",
            palette="uncert-stippled/seq-YlOrBr-inv",
            color_scale_min=-50,
            color_scale_max=0,
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
            ],
        ),
        CoverageConfigurationCreate(
            name="snwdays_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="snwdays",
            thredds_url_pattern="indici5rcm/clipped/snwdays_an_1mm_2oc_EC-EARTH_CCLM4-8-17_{scenario}_{time_window}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrBr-inv",
            color_scale_min=-50,
            color_scale_max=0,
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
            ],
        ),
        CoverageConfigurationCreate(
            name="snwdays_30yr_anomaly_annual_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="snwdays",
            thredds_url_pattern="indici5rcm/clipped/snwdays_an_1mm_2oc_EC-EARTH_RACMO22E_{scenario}_{time_window}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrBr-inv",
            color_scale_min=-50,
            color_scale_max=0,
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
            ],
        ),
        CoverageConfigurationCreate(
            name="snwdays_30yr_anomaly_annual_model_ec_earth_rca4",
            netcdf_main_dataset_name="snwdays",
            thredds_url_pattern="indici5rcm/clipped/snwdays_an_1mm_2oc_EC-EARTH_RCA4_{scenario}_{time_window}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrBr-inv",
            color_scale_min=-50,
            color_scale_max=0,
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
            ],
        ),
        CoverageConfigurationCreate(
            name="snwdays_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="snwdays",
            thredds_url_pattern="indici5rcm/clipped/snwdays_an_1mm_2oc_HadGEM2-ES_RACMO22E_{scenario}_{time_window}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrBr-inv",
            color_scale_min=-50,
            color_scale_max=0,
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
            ],
        ),
        CoverageConfigurationCreate(
            name="snwdays_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="snwdays",
            thredds_url_pattern="indici5rcm/clipped/snwdays_an_1mm_2oc_MPI-ESM-LR_REMO2009_{scenario}_{time_window}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrBr-inv",
            color_scale_min=-50,
            color_scale_max=0,
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
            ],
        ),
    ]
