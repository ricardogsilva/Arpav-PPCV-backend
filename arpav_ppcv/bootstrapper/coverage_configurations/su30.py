"""
- [x] su30_annual_absolute_model_ensemble
- [x] su30_annual_absolute_model_ensemble_upper_uncertainty
- [x] su30_annual_absolute_model_ensemble_lower_uncertainty
- [x] su30_annual_absolute_model_ec_earth_cclm4_8_17
- [x] su30_annual_absolute_model_ec_earth_racmo22e
- [x] su30_annual_absolute_model_ec_earth_rca4
- [x] su30_annual_absolute_model_hadgem2_es_racmo22e
- [x] su30_annual_absolute_model_mpi_esm_lr_remo2009

- [x] 30year anomaly
  - [x] su30_30yr_anomaly_annual_agree_model_ensemble
  - [x] su30_30yr_anomaly_annual_model_ec_earth_cclm4_8_17
  - [x] su30_30yr_anomaly_annual_model_ec_earth_racmo22e
  - [x] su30_30yr_anomaly_annual_model_ec_earth_rca4
  - [x] su30_30yr_anomaly_annual_model_hadgem2_es_racmo22e
  - [x] su30_30yr_anomaly_annual_model_mpi_esm_lr_remo2009
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
            name="su30_annual_absolute_model_ensemble",
            netcdf_main_dataset_name="su30",
            thredds_url_pattern="ensymbc/clipped/ecasu_30_avg_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
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
            observation_variable_id=(
                v.id if (v := variables.get("SU30")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="su30_annual_absolute_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="su30",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ymbc/clipped/ecasu_30_EC-EARTH_CCLM4-8-17_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
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
            observation_variable_id=(
                v.id if (v := variables.get("SU30")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="su30_annual_absolute_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="su30",
            thredds_url_pattern="EC-EARTH_RACMO22Eymbc/clipped/ecasu_30_EC-EARTH_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
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
            observation_variable_id=(
                v.id if (v := variables.get("SU30")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="su30_annual_absolute_model_ec_earth_rca4",
            netcdf_main_dataset_name="su30",
            thredds_url_pattern="EC-EARTH_RCA4ymbc/clipped/ecasu_30_EC-EARTH_RCA4_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
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
            observation_variable_id=(
                v.id if (v := variables.get("SU30")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="su30_annual_absolute_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="su30",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eymbc/clipped/ecasu_30_HadGEM2-ES_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
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
            observation_variable_id=(
                v.id if (v := variables.get("SU30")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="su30_annual_absolute_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="su30",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ymbc/clipped/ecasu_30_MPI-ESM-LR_REMO2009_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
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
            observation_variable_id=(
                v.id if (v := variables.get("SU30")) is not None else None
            ),
            observation_variable_aggregation_type=ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="su30_annual_absolute_model_ensemble_upper_uncertainty",
            netcdf_main_dataset_name="su30_stdup",
            thredds_url_pattern="ensymbc/std/clipped/ecasu_30_stdup_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
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
            name="su30_annual_absolute_model_ensemble_lower_uncertainty",
            netcdf_main_dataset_name="su30_stddown",
            thredds_url_pattern="ensymbc/std/clipped/ecasu_30_stddown_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
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
            name="su30_30yr_anomaly_annual_agree_model_ensemble",
            netcdf_main_dataset_name="su30",
            thredds_url_pattern="ensembletwbc/std/clipped/ecasuan_30_avgagree_{time_window}_{scenario}_ls_VFVG.nc",
            unit="gg",
            palette="uncert-stippled/seq-YlOrRd",
            color_scale_min=-5,
            color_scale_max=75,
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
            name="su30_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="su30",
            thredds_url_pattern="indici5rcm/clipped/ecasuan_30_EC-EARTH_CCLM4-8-17_{scenario}_{time_window}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
            color_scale_min=-5,
            color_scale_max=75,
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
            name="su30_30yr_anomaly_annual_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="su30",
            thredds_url_pattern="indici5rcm/clipped/ecasuan_30_EC-EARTH_RACMO22E_{scenario}_{time_window}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
            color_scale_min=-5,
            color_scale_max=75,
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
            name="su30_30yr_anomaly_annual_model_ec_earth_rca4",
            netcdf_main_dataset_name="su30",
            thredds_url_pattern="indici5rcm/clipped/ecasuan_30_EC-EARTH_RCA4_{scenario}_{time_window}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
            color_scale_min=-5,
            color_scale_max=75,
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
            name="su30_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="su30",
            thredds_url_pattern="indici5rcm/clipped/ecasuan_30_HadGEM2-ES_RACMO22E_{scenario}_{time_window}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
            color_scale_min=-5,
            color_scale_max=75,
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
            name="su30_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="su30",
            thredds_url_pattern="indici5rcm/clipped/ecasuan_30_MPI-ESM-LR_REMO2009_{scenario}_{time_window}_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
            color_scale_min=-5,
            color_scale_max=75,
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


def get_related_map() -> dict[str, list[str]]:
    return {
        "su30_annual_absolute_model_ensemble": [
            "su30_annual_absolute_model_ec_earth_cclm4_8_17",
            "su30_annual_absolute_model_ec_earth_racmo22e",
            "su30_annual_absolute_model_ec_earth_rca4",
            "su30_annual_absolute_model_hadgem2_es_racmo22e",
            "su30_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "su30_annual_absolute_model_ec_earth_cclm4_8_17": [
            "su30_annual_absolute_model_ensemble",
            "su30_annual_absolute_model_ec_earth_racmo22e",
            "su30_annual_absolute_model_ec_earth_rca4",
            "su30_annual_absolute_model_hadgem2_es_racmo22e",
            "su30_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "su30_annual_absolute_model_ec_earth_racmo22e": [
            "su30_annual_absolute_model_ensemble",
            "su30_annual_absolute_model_ec_earth_cclm4_8_17",
            "su30_annual_absolute_model_ec_earth_rca4",
            "su30_annual_absolute_model_hadgem2_es_racmo22e",
            "su30_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "su30_annual_absolute_model_ec_earth_rca4": [
            "su30_annual_absolute_model_ensemble",
            "su30_annual_absolute_model_ec_earth_cclm4_8_17",
            "su30_annual_absolute_model_ec_earth_racmo22e",
            "su30_annual_absolute_model_hadgem2_es_racmo22e",
            "su30_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "su30_annual_absolute_model_hadgem2_es_racmo22e": [
            "su30_annual_absolute_model_ensemble",
            "su30_annual_absolute_model_ec_earth_cclm4_8_17",
            "su30_annual_absolute_model_ec_earth_racmo22e",
            "su30_annual_absolute_model_ec_earth_rca4",
            "su30_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "su30_annual_absolute_model_mpi_esm_lr_remo2009": [
            "su30_annual_absolute_model_ensemble",
            "su30_annual_absolute_model_ec_earth_cclm4_8_17",
            "su30_annual_absolute_model_ec_earth_racmo22e",
            "su30_annual_absolute_model_ec_earth_rca4",
            "su30_annual_absolute_model_hadgem2_es_racmo22e",
        ],
        "su30_30yr_anomaly_annual_agree_model_ensemble": [
            "su30_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            "su30_30yr_anomaly_annual_model_ec_earth_racmo22e",
            "su30_30yr_anomaly_annual_model_ec_earth_rca4",
            "su30_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            "su30_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
        ],
        "su30_30yr_anomaly_annual_model_ec_earth_cclm4_8_17": [
            "su30_30yr_anomaly_annual_agree_model_ensemble",
            "su30_30yr_anomaly_annual_model_ec_earth_racmo22e",
            "su30_30yr_anomaly_annual_model_ec_earth_rca4",
            "su30_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            "su30_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
        ],
        "su30_30yr_anomaly_annual_model_ec_earth_racmo22e": [
            "su30_30yr_anomaly_annual_agree_model_ensemble",
            "su30_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            "su30_30yr_anomaly_annual_model_ec_earth_rca4",
            "su30_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            "su30_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
        ],
        "su30_30yr_anomaly_annual_model_ec_earth_rca4": [
            "su30_30yr_anomaly_annual_agree_model_ensemble",
            "su30_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            "su30_30yr_anomaly_annual_model_ec_earth_racmo22e",
            "su30_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            "su30_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
        ],
        "su30_30yr_anomaly_annual_model_hadgem2_es_racmo22e": [
            "su30_30yr_anomaly_annual_agree_model_ensemble",
            "su30_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            "su30_30yr_anomaly_annual_model_ec_earth_racmo22e",
            "su30_30yr_anomaly_annual_model_ec_earth_rca4",
            "su30_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
        ],
        "su30_30yr_anomaly_annual_model_mpi_esm_lr_remo2009": [
            "su30_30yr_anomaly_annual_agree_model_ensemble",
            "su30_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            "su30_30yr_anomaly_annual_model_ec_earth_racmo22e",
            "su30_30yr_anomaly_annual_model_ec_earth_rca4",
            "su30_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
        ],
    }


def get_uncertainty_map() -> dict[str, tuple[str, str]]:
    return {
        "su30_annual_absolute_model_ensemble": (
            "su30_annual_absolute_model_ensemble_upper_uncertainty",
            "su30_annual_absolute_model_ensemble_lower_uncertainty",
        ),
    }
