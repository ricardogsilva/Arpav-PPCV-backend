"""
- [x] seasonal
  - [x] tasmax_seasonal_absolute_model_ensemble
  - [x] tasmax_seasonal_absolute_model_ensemble_upper_uncertainty
  - [x] tasmax_seasonal_absolute_model_ensemble_lower_uncertainty
  - [x] tasmax_seasonal_absolute_model_ec_earth_cclm4_8_17
  - [x] tasmax_seasonal_absolute_model_ec_earth_racmo22e
  - [x] tasmax_seasonal_absolute_model_ec_earth_rca4
  - [x] tasmax_seasonal_absolute_model_hadgem2_es_racmo22e
  - [x] tasmax_seasonal_absolute_model_mpi_esm_lr_remo2009

- [x] annual
  - [x] tasmax_annual_absolute_model_ensemble
  - [x] tasmax_annual_absolute_model_ensemble_upper_uncertainty
  - [x] tasmax_annual_absolute_model_ensemble_lower_uncertainty
  - [x] tasmax_annual_absolute_model_ec_earth_cclm4_8_17
  - [x] tasmax_annual_absolute_model_ec_earth_racmo22e
  - [x] tasmax_annual_absolute_model_ec_earth_rca4
  - [x] tasmax_annual_absolute_model_hadgem2_es_racmo22e
  - [x] tasmax_annual_absolute_model_mpi_esm_lr_remo2009

- [x] 30year anomaly
  - [x] tasmax_30yr_anomaly_seasonal_agree_model_ensemble
  - [x] tasmax_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17
  - [x] tasmax_30yr_anomaly_seasonal_model_ec_earth_racmo22e
  - [x] tasmax_30yr_anomaly_seasonal_model_ec_earth_rca4
  - [x] tasmax_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e
  - [x] tasmax_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009
"""
from ...schemas.base import ObservationAggregationType
from ...schemas.coverages import (
    CoverageConfigurationCreate,
    ConfigurationParameterPossibleValueCreate,
)


def generate_tasmax_configurations(
    conf_param_values, variables
) -> list[CoverageConfigurationCreate]:
    return [
        CoverageConfigurationCreate(
            name="tasmax_seasonal_absolute_model_ensemble",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="ensymbc/clipped/tasmax_avg_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-3,
            color_scale_max=32,
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
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmax_annual_absolute_model_ensemble",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="ensymbc/clipped/tasmax_avg_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-3,
            color_scale_max=32,
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
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmax_seasonal_absolute_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ymbc/clipped/tasmax_EC-EARTH_CCLM4-8-17_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-3,
            color_scale_max=32,
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
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmax_annual_absolute_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ymbc/clipped/tasmax_EC-EARTH_CCLM4-8-17_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
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
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmax_seasonal_absolute_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="EC-EARTH_RACMO22Eymbc/clipped/tasmax_EC-EARTH_RACMO22E_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-3,
            color_scale_max=32,
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
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmax_annual_absolute_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="EC-EARTH_RACMO22Eymbc/clipped/tasmax_EC-EARTH_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
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
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmax_seasonal_absolute_model_ec_earth_rca4",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="EC-EARTH_RCA4ymbc/clipped/tasmax_EC-EARTH_RCA4_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-3,
            color_scale_max=32,
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
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmax_annual_absolute_model_ec_earth_rca4",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="EC-EARTH_RCA4ymbc/clipped/tasmax_EC-EARTH_RCA4_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
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
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmax_seasonal_absolute_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eymbc/clipped/tasmax_HadGEM2-ES_RACMO22E_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-3,
            color_scale_max=32,
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
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmax_annual_absolute_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eymbc/clipped/tasmax_HadGEM2-ES_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
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
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmax_seasonal_absolute_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ymbc/clipped/tasmax_MPI-ESM-LR_REMO2009_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-3,
            color_scale_max=32,
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
            observation_variable_id=(
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmax_annual_absolute_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ymbc/clipped/tasmax_MPI-ESM-LR_REMO2009_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
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
                v.id if (v := variables.get("TXd")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmax_seasonal_absolute_model_ensemble_upper_uncertainty",
            netcdf_main_dataset_name="tasmax_stdup",
            thredds_url_pattern="ensymbc/std/clipped/tasmax_stdup_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
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
            name="tasmax_seasonal_absolute_model_ensemble_lower_uncertainty",
            netcdf_main_dataset_name="tasmax_stddown",
            thredds_url_pattern="ensymbc/std/clipped/tasmax_stddown_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
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
            name="tasmax_annual_absolute_model_ensemble_upper_uncertainty",
            netcdf_main_dataset_name="tasmax_stdup",
            thredds_url_pattern="ensymbc/std/clipped/tasmax_stdup_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
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
            name="tasmax_annual_absolute_model_ensemble_lower_uncertainty",
            netcdf_main_dataset_name="tasmax_stddown",
            thredds_url_pattern="ensymbc/std/clipped/tasmax_stddown_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=7,
            color_scale_max=37,
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
            name="tasmax_30yr_anomaly_seasonal_agree_model_ensemble",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="ensembletwbc/std/clipped/tasmax_avgagree_anom_{time_window}_{scenario}_{year_period}_VFVGTAA.nc",
            unit="ºC",
            palette="uncert-stippled/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
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
            name="tasmax_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="taspr5rcm/clipped/tasmax_EC-EARTH_CCLM4-8-17_{scenario}_seas_{time_window}{year_period}_VFVGTAA.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
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
            name="tasmax_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="taspr5rcm/clipped/tasmax_EC-EARTH_RACMO22E_{scenario}_seas_{time_window}{year_period}_VFVGTAA.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
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
            name="tasmax_30yr_anomaly_seasonal_model_ec_earth_rca4",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="taspr5rcm/clipped/tasmax_EC-EARTH_RCA4_{scenario}_seas_{time_window}{year_period}_VFVGTAA.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
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
            name="tasmax_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="taspr5rcm/clipped/tasmax_HadGEM2-ES_RACMO22E_{scenario}_seas_{time_window}{year_period}_VFVGTAA.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
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
            name="tasmax_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="taspr5rcm/clipped/tasmax_MPI-ESM-LR_REMO2009_{scenario}_seas_{time_window}{year_period}_VFVGTAA.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
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
