from ...schemas.coverages import (
    CoverageConfigurationCreate,
    ConfigurationParameterPossibleValueCreate,
)

_DISPLAY_NAME_ENGLISH = "Cooling degree days"
_DISPLAY_NAME_ITALIAN = "Gradi giorno di raffrescamento"
_DESCRIPTION_ENGLISH = (
    "Sum of the average daily temperature minus 21°C if the average daily temperature "
    "is greater than 24°C"
)
_DESCRIPTION_ITALIAN = (
    "Somma della temperatura media giornaliera meno 21°C se la temperatura media "
    "giornaliera è maggiore di 24°C"
)


def generate_configurations(
    conf_param_values,
) -> list[CoverageConfigurationCreate]:
    return [
        CoverageConfigurationCreate(
            name="cdds_annual_absolute_model_ensemble",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdds",
            wms_main_layer_name="cdds",
            thredds_url_pattern="ensymbc/clipped_noppcne/cdds_21oc24oc_avg_ts19762100_{scenario}_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=1000,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdds")
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
                        ("year_period", "year")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="cdds_annual_absolute_model_ec_earth_cclm4_8_17",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdds",
            wms_main_layer_name="cdds",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ymbc/clipped_noppcne/cdds_21oc24oc_EC-EARTH_CCLM4-8-17_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=1000,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdds")
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
                        ("climatological_model", "ec_earth_cclm_4_8_17")
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
                        ("year_period", "year")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="cdds_annual_absolute_model_ec_earth_racmo22e",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdds",
            wms_main_layer_name="cdds",
            thredds_url_pattern="EC-EARTH_RACMO22Eymbc/clipped_noppcne/cdds_21oc24oc_EC-EARTH_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=1000,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdds")
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
                        ("climatological_model", "ec_earth_racmo22e")
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
                        ("year_period", "year")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="cdds_annual_absolute_model_ec_earth_rca4",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdds",
            wms_main_layer_name="cdds",
            thredds_url_pattern="EC-EARTH_RCA4ymbc/clipped_noppcne/cdds_21oc24oc_EC-EARTH_RCA4_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=1000,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdds")
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
                        ("climatological_model", "ec_earth_rca4")
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
                        ("year_period", "year")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="cdds_annual_absolute_model_hadgem2_es_racmo22e",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdds",
            wms_main_layer_name="cdds",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eymbc/clipped_noppcne/cdds_21oc24oc_HadGEM2-ES_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=1000,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdds")
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
                        ("climatological_model", "hadgem2_racmo22e")
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
                        ("year_period", "year")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="cdds_annual_absolute_model_mpi_esm_lr_remo2009",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdds",
            wms_main_layer_name="cdds",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ymbc/clipped_noppcne/cdds_21oc24oc_MPI-ESM-LR_REMO2009_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=1000,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdds")
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
                        ("climatological_model", "mpi_esm_lr_remo2009")
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
                        ("year_period", "year")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="cdds_annual_absolute_model_ensemble_upper_uncertainty",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdds_stdup",
            wms_main_layer_name="cdds_stdup",
            thredds_url_pattern="ensymbc/std/clipped/cdds_21oc24oc_stdup_ts19762100_{scenario}_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=1000,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdds")
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
                        ("climatological_model", "model_ensemble")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("uncertainty_type", "upper_bound")
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
                        ("year_period", "year")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="cdds_annual_absolute_model_ensemble_lower_uncertainty",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdds_stddown",
            wms_main_layer_name="cdds_stddown",
            thredds_url_pattern="ensymbc/std/clipped/cdds_21oc24oc_stddown_ts19762100_{scenario}_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=1000,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdds")
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
                        ("climatological_model", "model_ensemble")
                    ].id
                ),
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("uncertainty_type", "lower_bound")
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
                        ("year_period", "year")
                    ].id
                ),
            ],
        ),
        # ---
        CoverageConfigurationCreate(
            name="cdds_30yr_anomaly_annual_agree_model_ensemble",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdds",
            wms_main_layer_name="cdds-uncertainty_group",
            wms_secondary_layer_name="cdds",
            thredds_url_pattern="ensembletwbc/std/clipped/cdds_an_21oc24oc_avgagree_{time_window}_{scenario}_ls_VFVG.nc",
            unit="ºC",
            palette="uncert-stippled/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=1000,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdds")
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
                        ("year_period", "year")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="cdds_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdds",
            wms_main_layer_name="cdds",
            thredds_url_pattern="indici5rcm/clipped_noppcne/cdds_an_21oc24oc_EC-EARTH_CCLM4-8-17_{scenario}_{time_window}_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=1000,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdds")
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
                        ("year_period", "year")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="cdds_30yr_anomaly_annual_model_ec_earth_racmo22e",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdds",
            wms_main_layer_name="cdds",
            thredds_url_pattern="indici5rcm/clipped_noppcne/cdds_an_21oc24oc_EC-EARTH_RACMO22E_{scenario}_{time_window}_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=1000,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdds")
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
                        ("year_period", "year")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="cdds_30yr_anomaly_annual_model_ec_earth_rca4",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdds",
            wms_main_layer_name="cdds",
            thredds_url_pattern="indici5rcm/clipped_noppcne/cdds_an_21oc24oc_EC-EARTH_RCA4_{scenario}_{time_window}_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=1000,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdds")
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
                        ("year_period", "year")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="cdds_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdds",
            wms_main_layer_name="cdds",
            thredds_url_pattern="indici5rcm/clipped_noppcne/cdds_an_21oc24oc_HadGEM2-ES_RACMO22E_{scenario}_{time_window}_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=1000,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdds")
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
                        ("year_period", "year")
                    ].id
                ),
            ],
        ),
        CoverageConfigurationCreate(
            name="cdds_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
            display_name_english=_DISPLAY_NAME_ENGLISH,
            display_name_italian=_DISPLAY_NAME_ITALIAN,
            description_english=_DESCRIPTION_ENGLISH,
            description_italian=_DESCRIPTION_ITALIAN,
            netcdf_main_dataset_name="cdds",
            wms_main_layer_name="cdds",
            thredds_url_pattern="indici5rcm/clipped_noppcne/cdds_an_21oc24oc_MPI-ESM-LR_REMO2009_{scenario}_{time_window}_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=1000,
            possible_values=[
                ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[
                        ("climatological_variable", "cdds")
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
                        ("year_period", "year")
                    ].id
                ),
            ],
        ),
    ]


def get_related_map() -> dict[str, list[str]]:
    return {
        "cdds_annual_absolute_model_ensemble": [
            "cdds_annual_absolute_model_ec_earth_cclm4_8_17",
            "cdds_annual_absolute_model_ec_earth_racmo22e",
            "cdds_annual_absolute_model_ec_earth_rca4",
            "cdds_annual_absolute_model_hadgem2_es_racmo22e",
            "cdds_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "cdds_annual_absolute_model_ec_earth_cclm4_8_17": [
            "cdds_annual_absolute_model_ensemble",
            "cdds_annual_absolute_model_ec_earth_racmo22e",
            "cdds_annual_absolute_model_ec_earth_rca4",
            "cdds_annual_absolute_model_hadgem2_es_racmo22e",
            "cdds_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "cdds_annual_absolute_model_ec_earth_racmo22e": [
            "cdds_annual_absolute_model_ensemble",
            "cdds_annual_absolute_model_ec_earth_cclm4_8_17",
            "cdds_annual_absolute_model_ec_earth_rca4",
            "cdds_annual_absolute_model_hadgem2_es_racmo22e",
            "cdds_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "cdds_annual_absolute_model_ec_earth_rca4": [
            "cdds_annual_absolute_model_ensemble",
            "cdds_annual_absolute_model_ec_earth_cclm4_8_17",
            "cdds_annual_absolute_model_ec_earth_racmo22e",
            "cdds_annual_absolute_model_hadgem2_es_racmo22e",
            "cdds_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "cdds_annual_absolute_model_hadgem2_es_racmo22e": [
            "cdds_annual_absolute_model_ensemble",
            "cdds_annual_absolute_model_ec_earth_cclm4_8_17",
            "cdds_annual_absolute_model_ec_earth_racmo22e",
            "cdds_annual_absolute_model_ec_earth_rca4",
            "cdds_annual_absolute_model_mpi_esm_lr_remo2009",
        ],
        "cdds_annual_absolute_model_mpi_esm_lr_remo2009": [
            "cdds_annual_absolute_model_ensemble",
            "cdds_annual_absolute_model_ec_earth_cclm4_8_17",
            "cdds_annual_absolute_model_ec_earth_racmo22e",
            "cdds_annual_absolute_model_ec_earth_rca4",
            "cdds_annual_absolute_model_hadgem2_es_racmo22e",
        ],
        "cdds_30yr_anomaly_annual_agree_model_ensemble": [
            "cdds_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            "cdds_30yr_anomaly_annual_model_ec_earth_racmo22e",
            "cdds_30yr_anomaly_annual_model_ec_earth_rca4",
            "cdds_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            "cdds_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
        ],
        "cdds_30yr_anomaly_annual_model_ec_earth_cclm4_8_17": [
            "cdds_30yr_anomaly_annual_agree_model_ensemble",
            "cdds_30yr_anomaly_annual_model_ec_earth_racmo22e",
            "cdds_30yr_anomaly_annual_model_ec_earth_rca4",
            "cdds_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            "cdds_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
        ],
        "cdds_30yr_anomaly_annual_model_ec_earth_racmo22e": [
            "cdds_30yr_anomaly_annual_agree_model_ensemble",
            "cdds_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            "cdds_30yr_anomaly_annual_model_ec_earth_rca4",
            "cdds_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            "cdds_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
        ],
        "cdds_30yr_anomaly_annual_model_ec_earth_rca4": [
            "cdds_30yr_anomaly_annual_agree_model_ensemble",
            "cdds_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            "cdds_30yr_anomaly_annual_model_ec_earth_racmo22e",
            "cdds_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
            "cdds_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
        ],
        "cdds_30yr_anomaly_annual_model_hadgem2_es_racmo22e": [
            "cdds_30yr_anomaly_annual_agree_model_ensemble",
            "cdds_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            "cdds_30yr_anomaly_annual_model_ec_earth_racmo22e",
            "cdds_30yr_anomaly_annual_model_ec_earth_rca4",
            "cdds_30yr_anomaly_annual_model_mpi_esm_lr_remo2009",
        ],
        "cdds_30yr_anomaly_annual_model_mpi_esm_lr_remo2009": [
            "cdds_30yr_anomaly_annual_agree_model_ensemble",
            "cdds_30yr_anomaly_annual_model_ec_earth_cclm4_8_17",
            "cdds_30yr_anomaly_annual_model_ec_earth_racmo22e",
            "cdds_30yr_anomaly_annual_model_ec_earth_rca4",
            "cdds_30yr_anomaly_annual_model_hadgem2_es_racmo22e",
        ],
    }


def get_uncertainty_map() -> dict[str, tuple[str, str]]:
    return {
        "cdds_annual_absolute_model_ensemble": (
            "cdds_annual_absolute_model_ensemble_upper_uncertainty",
            "cdds_annual_absolute_model_ensemble_lower_uncertainty",
        ),
    }