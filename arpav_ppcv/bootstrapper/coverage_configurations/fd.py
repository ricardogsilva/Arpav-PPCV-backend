"""
- [x] fd_annual_absolute_model_ensemble
- [x] fd_annual_absolute_model_ensemble_upper_uncertainty
- [x] fd_annual_absolute_model_ensemble_lower_uncertainty
- [x] fd_annual_absolute_model_ec_earth_cclm4_8_17
- [x] fd_annual_absolute_model_ec_earth_racmo22e
- [x] fd_annual_absolute_model_ec_earth_rca4
- [x] fd_annual_absolute_model_hadgem2_es_racmo22e
- [x] fd_annual_absolute_model_mpi_esm_lr_remo2009

- [x] 30year anomaly
  - [x] fd_30yr_anomaly_annual_agree_model_ensemble
  - [x] fd_30yr_anomaly_annual_model_ec_earth_cclm4_8_17
  - [x] fd_30yr_anomaly_annual_model_ec_earth_racmo22e
  - [x] fd_30yr_anomaly_annual_model_ec_earth_rca4
  - [x] fd_30yr_anomaly_annual_model_hadgem2_es_racmo22e
  - [x] fd_30yr_anomaly_annual_model_mpi_esm_lr_remo2009

"""
from ...schemas.base import ObservationAggregationType
from ...schemas.coverages import (
    CoverageConfigurationCreate,
    ConfigurationParameterPossibleValueCreate,
)


def generate_fd_configurations(
    conf_param_values, variables
) -> list[CoverageConfigurationCreate]:
    return [
        CoverageConfigurationCreate(
            name="fd_annual_absolute_model_ensemble",
            netcdf_main_dataset_name="fd",
            thredds_url_pattern="ensymbc/clipped/ecafd_0_avg_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-Blues-inv",
            color_scale_min=0,
            color_scale_max=200,
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
            observation_variable_id=(
                v.id if (v := variables.get("FD")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="fd_annual_absolute_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="fd",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ymbc/clipped/ecafd_0_EC-EARTH_CCLM4-8-17_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-Blues-inv",
            color_scale_min=0,
            color_scale_max=200,
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
            observation_variable_id=(
                v.id if (v := variables.get("FD")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="fd_annual_absolute_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="fd",
            thredds_url_pattern="EC-EARTH_RACMO22Eymbc/clipped/ecafd_0_EC-EARTH_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-Blues-inv",
            color_scale_min=0,
            color_scale_max=200,
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
            observation_variable_id=(
                v.id if (v := variables.get("FD")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="fd_annual_absolute_model_ec_earth_rca4",
            netcdf_main_dataset_name="fd",
            thredds_url_pattern="EC-EARTH_RCA4ymbc/clipped/ecafd_0_EC-EARTH_RCA4_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-Blues-inv",
            color_scale_min=0,
            color_scale_max=200,
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
            observation_variable_id=(
                v.id if (v := variables.get("FD")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="fd_annual_absolute_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="fd",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eymbc/clipped/ecafd_0_HadGEM2-ES_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-Blues-inv",
            color_scale_min=0,
            color_scale_max=200,
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
            observation_variable_id=(
                v.id if (v := variables.get("FD")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="fd_annual_absolute_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="fd",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ymbc/clipped/ecafd_0_MPI-ESM-LR_REMO2009_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-Blues-inv",
            color_scale_min=0,
            color_scale_max=200,
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
            observation_variable_id=(
                v.id if (v := variables.get("FD")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="fd_annual_absolute_model_ensemble_upper_uncertainty",
            netcdf_main_dataset_name="fd_stdup",
            thredds_url_pattern="ensymbc/std/clipped/ecafd_0_stdup_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-Blues-inv",
            color_scale_min=0,
            color_scale_max=200,
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
            name="fd_annual_absolute_model_ensemble_lower_uncertainty",
            netcdf_main_dataset_name="fd_stddown",
            thredds_url_pattern="ensymbc/std/clipped/ecafd_0_stddown_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-Blues-inv",
            color_scale_min=0,
            color_scale_max=200,
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
            name="fd_30yr_anomaly_annual_agree_model_ensemble",
            netcdf_main_dataset_name="fd",
            thredds_url_pattern="ensembletwbc/std/clipped/ecafdan_0_avgagree_{time_window}_{scenario}_ls_VFVG.nc",
            unit="gg",
            palette="uncert-stippled/seq-YlOrRd-inv",
            color_scale_min=-85,
            color_scale_max=5,
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
            name="fd_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="fd",
            thredds_url_pattern="indici5rcm/clipped/ecafdan_0_EC-EARTH_CCLM4-8-17_{scenario}_{time_window}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd-inv",
            color_scale_min=-85,
            color_scale_max=5,
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
            name="fd_30yr_anomaly_annual_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="fd",
            thredds_url_pattern="indici5rcm/clipped/ecafdan_0_EC-EARTH_RACMO22E_{scenario}_{time_window}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd-inv",
            color_scale_min=-85,
            color_scale_max=5,
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
            name="fd_30yr_anomaly_annual_model_ec_earth_rca4",
            netcdf_main_dataset_name="fd",
            thredds_url_pattern="indici5rcm/clipped/ecafdan_0_EC-EARTH_RCA4_{scenario}_{time_window}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd-inv",
            color_scale_min=-85,
            color_scale_max=5,
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
            name="fd_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="fd",
            thredds_url_pattern="indici5rcm/clipped/ecafdan_0_HadGEM2-ES_RACMO22E_{scenario}_{time_window}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd-inv",
            color_scale_min=-85,
            color_scale_max=5,
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
            name="fd_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="fd",
            thredds_url_pattern="indici5rcm/clipped/ecafdan_0_MPI-ESM-LR_REMO2009_{scenario}_{time_window}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd-inv",
            color_scale_min=-85,
            color_scale_max=5,
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
