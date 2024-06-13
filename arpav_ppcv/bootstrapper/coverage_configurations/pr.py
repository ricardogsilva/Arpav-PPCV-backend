"""
- [x] anomaly
    - [x] pr_seasonal_anomaly_model_ensemble
    - [x] pr_seasonal_anomaly_model_ensemble_upper_uncertainty
    - [x] pr_seasonal_anomaly_model_ensemble_lower_uncertainty
    - [x] pr_seasonal_anomaly_model_ec_earth_cclm4_8_17
    - [x] pr_seasonal_anomaly_model_ec_earth_racmo22e
    - [x] pr_seasonal_anomaly_model_ec_earth_rca4
    - [x] pr_seasonal_anomaly_model_hadgem2_es_racmo22e
    - [x] pr_seasonal_anomaly_model_mpi_esm_lr_remo2009

- [x] absolute value
  - [x] seasonal
    - [x] pr_seasonal_absolute_model_ensemble
    - [x] pr_seasonal_absolute_model_ensemble_upper_uncertainty
    - [x] pr_seasonal_absolute_model_ensemble_lower_uncertainty
    - [x] pr_seasonal_absolute_model_ec_earth_cclm4_8_17
    - [x] pr_seasonal_absolute_model_ec_earth_racmo22e
    - [x] pr_seasonal_absolute_model_ec_earth_rca4
    - [x] pr_seasonal_absolute_model_hadgem2_es_racmo22e
    - [x] pr_seasonal_absolute_model_mpi_esm_lr_remo2009

  - [x] annual
    - [x] pr_annual_absolute_model_ensemble
    - [x] pr_annual_absolute_model_ensemble_upper_uncertainty
    - [x] pr_annual_absolute_model_ensemble_lower_uncertainty
    - [x] pr_annual_absolute_model_ec_earth_cclm4_8_17
    - [x] pr_annual_absolute_model_ec_earth_racmo22e
    - [x] pr_annual_absolute_model_ec_earth_rca4
    - [x] pr_annual_absolute_model_hadgem2_es_racmo22e
    - [x] pr_annual_absolute_model_mpi_esm_lr_remo2009

- [x] 30year anomaly
  - [x] pr_30yr_anomaly_seasonal_agree_model_ensemble
  - [x] pr_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17
  - [x] pr_30yr_anomaly_seasonal_model_ec_earth_racmo22e
  - [x] pr_30yr_anomaly_seasonal_model_ec_earth_rca4
  - [x] pr_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e
  - [x] pr_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009
"""
from ...schemas.base import ObservationAggregationType
from ...schemas.coverages import (
    CoverageConfigurationCreate,
    ConfigurationParameterPossibleValueCreate,
)


def generate_configurations(
    conf_param_values, variables
) -> list[CoverageConfigurationCreate]:
    return [
        CoverageConfigurationCreate(
            name="pr_seasonal_anomaly_model_ensemble",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="ens5ym/clipped/pr_anom_pp_ts_{scenario}_{year_period}_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBG",
            color_scale_min=-40,
            color_scale_max=40,
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
            name="pr_seasonal_anomaly_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ym/clipped/pr_EC-EARTH_CCLM4-8-17_{scenario}_{year_period}_anomaly_pp_percentage_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBG",
            color_scale_min=-40,
            color_scale_max=40,
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
            name="pr_seasonal_anomaly_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="EC-EARTH_RACMO22Eym/clipped/pr_EC-EARTH_RACMO22E_{scenario}_{year_period}_anomaly_pp_percentage_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBG",
            color_scale_min=-40,
            color_scale_max=40,
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
            name="pr_seasonal_anomaly_model_ec_earth_rca4",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="EC-EARTH_RCA4ym/clipped/pr_EC-EARTH_RCA4_{scenario}_{year_period}_anomaly_pp_percentage_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBG",
            color_scale_min=-40,
            color_scale_max=40,
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
            name="pr_seasonal_anomaly_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eym/clipped/pr_HadGEM2-ES_RACMO22E_{scenario}_{year_period}_anomaly_pp_percentage_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBG",
            color_scale_min=-40,
            color_scale_max=40,
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
            name="pr_seasonal_anomaly_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ym/clipped/pr_MPI-ESM-LR_REMO2009_{scenario}_{year_period}_anomaly_pp_percentage_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBG",
            color_scale_min=-40,
            color_scale_max=40,
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
            name="pr_seasonal_anomaly_model_ensemble_upper_uncertainty",
            netcdf_main_dataset_name="pr_stdup",
            thredds_url_pattern="ens5ym/std/clipped/pr_anom_stdup_pp_ts_{scenario}_{year_period}_VFVGTAA.nc",
            unit="%",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=0,
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
            name="pr_seasonal_anomaly_model_ensemble_lower_uncertainty",
            netcdf_main_dataset_name="pr_stddown",
            thredds_url_pattern="ens5ym/std/clipped/pr_anom_stddown_pp_ts_{scenario}_{year_period}_VFVGTAA.nc",
            unit="%",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=0,
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
            name="pr_seasonal_absolute_model_ensemble",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="ensymbc/clipped/pr_avg_{scenario}_{year_period}_ts19762100_ls_VFVGTAA.nc",
            unit="mm",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=800,
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
                v.id if (v := variables.get("PRCPTOT")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="pr_annual_absolute_model_ensemble",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="ensymbc/clipped/pr_avg_{scenario}_ts19762100_ls_VFVGTAA.nc",
            unit="mm",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=3200,
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
                v.id if (v := variables.get("PRCPTOT")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="pr_seasonal_absolute_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ymbc/clipped/pr_EC-EARTH_CCLM4-8-17_{scenario}_{year_period}_ts_ls_VFVGTAA.nc",
            unit="%",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=800,
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
                v.id if (v := variables.get("PRCPTOT")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="pr_annual_absolute_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ymbc/clipped/pr_EC-EARTH_CCLM4-8-17_{scenario}_ts_ls_VFVGTAA.nc",
            unit="%",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=800,
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
                v.id if (v := variables.get("PRCPTOT")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="pr_seasonal_absolute_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="EC-EARTH_RACMO22Eymbc/clipped/pr_EC-EARTH_RACMO22E_{scenario}_{year_period}_ts_ls_VFVGTAA.nc",
            unit="%",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=800,
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
                v.id if (v := variables.get("PRCPTOT")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="pr_annual_absolute_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="EC-EARTH_RACMO22Eymbc/clipped/pr_EC-EARTH_RACMO22E_{scenario}_ts_ls_VFVGTAA.nc",
            unit="%",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=3200,
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
                v.id if (v := variables.get("PRCPTOT")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="pr_seasonal_absolute_model_ec_earth_rca4",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="EC-EARTH_RCA4ymbc/clipped/pr_EC-EARTH_RCA4_{scenario}_{year_period}_ts_ls_VFVGTAA.nc",
            unit="%",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=800,
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
                v.id if (v := variables.get("PRCPTOT")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="pr_annual_absolute_model_ec_earth_rca4",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="EC-EARTH_RCA4ymbc/clipped/pr_EC-EARTH_RCA4_{scenario}_ts_ls_VFVGTAA.nc",
            unit="%",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=3200,
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
                v.id if (v := variables.get("PRCPTOT")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="pr_seasonal_absolute_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eymbc/clipped/pr_HadGEM2-ES_RACMO22E_{scenario}_{year_period}_ts_ls_VFVGTAA.nc",
            unit="%",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=800,
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
                v.id if (v := variables.get("PRCPTOT")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="pr_annual_absolute_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eymbc/clipped/pr_HadGEM2-ES_RACMO22E_{scenario}_ts_ls_VFVGTAA.nc",
            unit="%",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=3200,
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
                v.id if (v := variables.get("PRCPTOT")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="pr_seasonal_absolute_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ymbc/clipped/pr_MPI-ESM-LR_REMO2009_{scenario}_{year_period}_ts_ls_VFVGTAA.nc",
            unit="%",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=800,
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
                v.id if (v := variables.get("PRCPTOT")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="pr_annual_absolute_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ymbc/clipped/pr_MPI-ESM-LR_REMO2009_{scenario}_ts_ls_VFVGTAA.nc",
            unit="%",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=3200,
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
                v.id if (v := variables.get("PRCPTOT")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="pr_seasonal_absolute_model_ensemble_upper_uncertainty",
            netcdf_main_dataset_name="pr_stdup",
            thredds_url_pattern="ensymbc/std/clipped/pr_stdup_{scenario}_{year_period}_ts19762100_ls_VFVGTAA.nc",
            unit="mm",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=800,
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
            name="pr_seasonal_absolute_model_ensemble_lower_uncertainty",
            netcdf_main_dataset_name="pr_stddown",
            thredds_url_pattern="ensymbc/std/clipped/pr_stddown_{scenario}_{year_period}_ts19762100_ls_VFVGTAA.nc",
            unit="mm",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=800,
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
            name="pr_annual_absolute_model_ensemble_upper_uncertainty",
            netcdf_main_dataset_name="pr_stdup",
            thredds_url_pattern="ensymbc/std/clipped/pr_stdup_{scenario}_ts19762100_ls_VFVGTAA.nc",
            unit="mm",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=3200,
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
            name="pr_annual_absolute_model_ensemble_lower_uncertainty",
            netcdf_main_dataset_name="pr_stddown",
            thredds_url_pattern="ensymbc/std/clipped/pr_stddown_{scenario}_ts19762100_ls_VFVGTAA.nc",
            unit="mm",
            palette="default/seq-BuYl-inv",
            color_scale_min=0,
            color_scale_max=3200,
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
            name="pr_30yr_anomaly_seasonal_agree_model_ensemble",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="ensembletwbc/std/clipped/pr_avgagree_percentage_{time_window}_{scenario}_{year_period}_VFVGTAA.nc",
            unit="%",
            palette="uncert-stippled/div-BrBG",
            color_scale_min=-40,
            color_scale_max=40,
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
            name="pr_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="taspr5rcm/clipped/pr_EC-EARTH_CCLM4-8-17_{scenario}_seas_{time_window}_percentage_{year_period}_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBG",
            color_scale_min=-40,
            color_scale_max=40,
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
            name="pr_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="taspr5rcm/clipped/pr_EC-EARTH_RACMO22E_{scenario}_seas_{time_window}_percentage_{year_period}_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBG",
            color_scale_min=-40,
            color_scale_max=40,
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
            name="pr_30yr_anomaly_seasonal_model_ec_earth_rca4",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="taspr5rcm/clipped/pr_EC-EARTH_RCA4_{scenario}_seas_{time_window}_percentage_{year_period}_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBG",
            color_scale_min=-40,
            color_scale_max=40,
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
            name="pr_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="taspr5rcm/clipped/pr_HadGEM2-ES_RACMO22E_{scenario}_seas_{time_window}_percentage_{year_period}_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBG",
            color_scale_min=-40,
            color_scale_max=40,
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
            name="pr_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="taspr5rcm/clipped/pr_MPI-ESM-LR_REMO2009_{scenario}_seas_{time_window}_percentage_{year_period}_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBG",
            color_scale_min=-40,
            color_scale_max=40,
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
        "pr_seasonal_anomaly_model_ensemble": [
            "pr_seasonal_anomaly_model_ec_earth_cclm4_8_17",
            "pr_seasonal_anomaly_model_ec_earth_racmo22e",
            "pr_seasonal_anomaly_model_ec_earth_rca4",
            "pr_seasonal_anomaly_model_hadgem2_es_racmo22e",
            "pr_seasonal_anomaly_model_mpi_esm_lr_remo2009",
        ],
        "pr_seasonal_anomaly_model_ec_earth_cclm4_8_17": [
            "pr_seasonal_anomaly_model_ensemble",
            "pr_seasonal_anomaly_model_ec_earth_racmo22e",
            "pr_seasonal_anomaly_model_ec_earth_rca4",
            "pr_seasonal_anomaly_model_hadgem2_es_racmo22e",
            "pr_seasonal_anomaly_model_mpi_esm_lr_remo2009",
        ],
        "pr_seasonal_anomaly_model_ec_earth_racmo22e": [
            "pr_seasonal_anomaly_model_ensemble",
            "pr_seasonal_anomaly_model_ec_earth_cclm4_8_17",
            "pr_seasonal_anomaly_model_ec_earth_rca4",
            "pr_seasonal_anomaly_model_hadgem2_es_racmo22e",
            "pr_seasonal_anomaly_model_mpi_esm_lr_remo2009",
        ],
        "pr_seasonal_anomaly_model_ec_earth_rca4": [
            "pr_seasonal_anomaly_model_ensemble",
            "pr_seasonal_anomaly_model_ec_earth_cclm4_8_17",
            "pr_seasonal_anomaly_model_ec_earth_racmo22e",
            "pr_seasonal_anomaly_model_hadgem2_es_racmo22e",
            "pr_seasonal_anomaly_model_mpi_esm_lr_remo2009",
        ],
        "pr_seasonal_anomaly_model_hadgem2_es_racmo22e": [
            "pr_seasonal_anomaly_model_ensemble",
            "pr_seasonal_anomaly_model_ec_earth_cclm4_8_17",
            "pr_seasonal_anomaly_model_ec_earth_racmo22e",
            "pr_seasonal_anomaly_model_ec_earth_rca4",
            "pr_seasonal_anomaly_model_mpi_esm_lr_remo2009",
        ],
        "pr_seasonal_anomaly_model_mpi_esm_lr_remo2009": [
            "pr_seasonal_anomaly_model_ensemble",
            "pr_seasonal_anomaly_model_ec_earth_cclm4_8_17",
            "pr_seasonal_anomaly_model_ec_earth_racmo22e",
            "pr_seasonal_anomaly_model_ec_earth_rca4",
            "pr_seasonal_anomaly_model_hadgem2_es_racmo22e",
        ],
        "pr_seasonal_absolute_model_ensemble": [
            "pr_seasonal_absolute_model_ec_earth_cclm4_8_17",
            "pr_seasonal_absolute_model_ec_earth_racmo22e",
            "pr_seasonal_absolute_model_ec_earth_rca4",
            "pr_seasonal_absolute_model_hadgem2_es_racmo22e",
            "pr_seasonal_absolute_model_mpi_esm_lr_remo2009",
        ],
        "pr_seasonal_absolute_model_ec_earth_cclm4_8_17": [
            "pr_seasonal_absolute_model_ensemble",
            "pr_seasonal_absolute_model_ec_earth_racmo22e",
            "pr_seasonal_absolute_model_ec_earth_rca4",
            "pr_seasonal_absolute_model_hadgem2_es_racmo22e",
            "pr_seasonal_absolute_model_mpi_esm_lr_remo2009",
        ],
        "pr_seasonal_absolute_model_ec_earth_racmo22e": [
            "pr_seasonal_absolute_model_ensemble",
            "pr_seasonal_absolute_model_ec_earth_cclm4_8_17",
            "pr_seasonal_absolute_model_ec_earth_rca4",
            "pr_seasonal_absolute_model_hadgem2_es_racmo22e",
            "pr_seasonal_absolute_model_mpi_esm_lr_remo2009",
        ],
        "pr_seasonal_absolute_model_ec_earth_rca4": [
            "pr_seasonal_absolute_model_ensemble",
            "pr_seasonal_absolute_model_ec_earth_cclm4_8_17",
            "pr_seasonal_absolute_model_ec_earth_racmo22e",
            "pr_seasonal_absolute_model_hadgem2_es_racmo22e",
            "pr_seasonal_absolute_model_mpi_esm_lr_remo2009",
        ],
        "pr_seasonal_absolute_model_hadgem2_es_racmo22e": [
            "pr_seasonal_absolute_model_ensemble",
            "pr_seasonal_absolute_model_ec_earth_cclm4_8_17",
            "pr_seasonal_absolute_model_ec_earth_racmo22e",
            "pr_seasonal_absolute_model_ec_earth_rca4",
            "pr_seasonal_absolute_model_mpi_esm_lr_remo2009",
        ],
        "pr_seasonal_absolute_model_mpi_esm_lr_remo2009": [
            "pr_seasonal_absolute_model_ensemble",
            "pr_seasonal_absolute_model_ec_earth_cclm4_8_17",
            "pr_seasonal_absolute_model_ec_earth_racmo22e",
            "pr_seasonal_absolute_model_ec_earth_rca4",
            "pr_seasonal_absolute_model_hadgem2_es_racmo22e",
        ],
        "pr_annual_absolute_model_ensemble": [
            "pr_annual_absolute_model_ec_earth_cclm4_8_17",
            "pr_annual_absolute_model_ec_earth_racmo22e",
            "pr_annual_absolute_model_ec_earth_rca4",
            "pr_annual_absolute_model_hadgem2_es_racmo22e",
            "pr_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "pr_annual_absolute_model_ec_earth_cclm4_8_17": [
            "pr_annual_absolute_model_ensemble",
            "pr_annual_absolute_model_ec_earth_racmo22e",
            "pr_annual_absolute_model_ec_earth_rca4",
            "pr_annual_absolute_model_hadgem2_es_racmo22e",
            "pr_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "pr_annual_absolute_model_ec_earth_racmo22e": [
            "pr_annual_absolute_model_ensemble",
            "pr_annual_absolute_model_ec_earth_cclm4_8_17",
            "pr_annual_absolute_model_ec_earth_rca4",
            "pr_annual_absolute_model_hadgem2_es_racmo22e",
            "pr_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "pr_annual_absolute_model_ec_earth_rca4": [
            "pr_annual_absolute_model_ensemble",
            "pr_annual_absolute_model_ec_earth_cclm4_8_17",
            "pr_annual_absolute_model_ec_earth_racmo22e",
            "pr_annual_absolute_model_hadgem2_es_racmo22e",
            "pr_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "pr_annual_absolute_model_hadgem2_es_racmo22e": [
            "pr_annual_absolute_model_ensemble",
            "pr_annual_absolute_model_ec_earth_cclm4_8_17",
            "pr_annual_absolute_model_ec_earth_racmo22e",
            "pr_annual_absolute_model_ec_earth_rca4",
            "pr_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "pr_annual_absolute_model_mpi_esm_lr_remo2009": [
            "pr_annual_absolute_model_ensemble",
            "pr_annual_absolute_model_ec_earth_cclm4_8_17",
            "pr_annual_absolute_model_ec_earth_racmo22e",
            "pr_annual_absolute_model_ec_earth_rca4",
            "pr_annual_absolute_model_hadgem2_es_racmo22e",
        ],
        "pr_30yr_anomaly_seasonal_agree_model_ensemble": [
            "pr_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            "pr_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            "pr_30yr_anomaly_seasonal_model_ec_earth_rca4",
            "pr_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
            "pr_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
        ],
        "pr_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17": [
            "pr_30yr_anomaly_seasonal_agree_model_ensemble",
            "pr_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            "pr_30yr_anomaly_seasonal_model_ec_earth_rca4",
            "pr_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
            "pr_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
        ],
        "pr_30yr_anomaly_seasonal_model_ec_earth_racmo22e": [
            "pr_30yr_anomaly_seasonal_agree_model_ensemble",
            "pr_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            "pr_30yr_anomaly_seasonal_model_ec_earth_rca4",
            "pr_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
            "pr_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
        ],
        "pr_30yr_anomaly_seasonal_model_ec_earth_rca4": [
            "pr_30yr_anomaly_seasonal_agree_model_ensemble",
            "pr_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            "pr_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            "pr_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
            "pr_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
        ],
        "pr_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e": [
            "pr_30yr_anomaly_seasonal_agree_model_ensemble",
            "pr_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            "pr_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            "pr_30yr_anomaly_seasonal_model_ec_earth_rca4",
            "pr_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009",
        ],
        "pr_30yr_anomaly_seasonal_model_mpi_esm_lr_remo2009": [
            "pr_30yr_anomaly_seasonal_agree_model_ensemble",
            "pr_30yr_anomaly_seasonal_model_ec_earth_cclm4_8_17",
            "pr_30yr_anomaly_seasonal_model_ec_earth_racmo22e",
            "pr_30yr_anomaly_seasonal_model_ec_earth_rca4",
            "pr_30yr_anomaly_seasonal_model_hadgem2_es_racmo22e",
        ],
    }


def get_uncertainty_map() -> dict[str, tuple[str, str]]:
    return {
        "pr_seasonal_anomaly_model_ensemble": (
            "pr_seasonal_anomaly_model_ensemble_upper_uncertainty",
            "pr_seasonal_anomaly_model_ensemble_lower_uncertainty",
        ),
        "pr_seasonal_absolute_model_ensemble": (
            "pr_seasonal_absolute_model_ensemble_upper_uncertainty",
            "pr_seasonal_absolute_model_ensemble_lower_uncertainty",
        ),
        "pr_annual_absolute_model_ensemble": (
            "pr_annual_absolute_model_ensemble_upper_uncertainty",
            "pr_annual_absolute_model_ensemble_lower_uncertainty",
        ),
    }
