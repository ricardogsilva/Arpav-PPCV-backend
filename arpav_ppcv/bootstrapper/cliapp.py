import typer

import sqlmodel
from rich import print
from sqlalchemy.exc import IntegrityError

from .. import database
from ..schemas import (
    base,
    observations,
)
from ..schemas.coverages import (
    ConfigurationParameterCreate,
    ConfigurationParameterValueCreateEmbeddedInConfigurationParameter,
    CoverageConfigurationCreate,
    ConfigurationParameterPossibleValueCreate,
)

app = typer.Typer()


@app.command("observation-variables")
def bootstrap_observation_variables(
    ctx: typer.Context,
):
    """Create initial observation variables."""
    variables = [
        observations.VariableCreate(
            name="TDd", description="Mean temperature", unit="ºC"
        ),
        observations.VariableCreate(
            name="TXd", description="Max temperature", unit="ºC"
        ),
        observations.VariableCreate(
            name="TNd", description="Min temperature", unit="ºC"
        ),
        observations.VariableCreate(
            name="PRCPTOT", description="Total precipitation", unit="mm"
        ),
        observations.VariableCreate(
            name="TR", description="Tropical nights", unit="mm"
        ),
        observations.VariableCreate(name="SU30", description="Hot days", unit="mm"),
        observations.VariableCreate(name="FD", description="Cold days", unit="mm"),
    ]
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        for var_create in variables:
            try:
                db_variable = database.create_variable(session, var_create)
                print(f"Created observation variable {db_variable.name!r}")
            except IntegrityError as err:
                print(
                    f"Could not create observation "
                    f"variable {var_create.name!r}: {err}"
                )
                session.rollback()
    print("Done!")


@app.command("coverage-configuration-parameters")
def bootstrap_coverage_configuration_parameters(
    ctx: typer.Context,
):
    """Create initial coverage configuration parameters."""
    params = [
        ConfigurationParameterCreate(
            name="scenario",
            description=(
                "Represents the path fragment related to forecast model scenario"
            ),
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="rcp26", description="Represents the RCP2.6 scenario"
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="rcp45", description="Represents the RCP4.5 scenario"
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="rcp85", description="Represents the RCP8.5 scenario"
                ),
            ],
        ),
        ConfigurationParameterCreate(
            name="time_window",
            description=(
                "Represents the path fragment related to forecast model time window for the anomalies"
            ),
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="tw1",
                    description=(
                        "Represents the first anomaly time window, which spans the "
                        "period 2021-2050, with regard to the 1976-2005 period"
                    ),
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="tw2",
                    description=(
                        "Represents the second anomaly time window, which spans the "
                        "period 2071-2100, with regard to the 1976-2005 period"
                    ),
                ),
            ],
        ),
        ConfigurationParameterCreate(
            name="year_period",
            description=(
                "Represents the yearly temporal aggregation period in file paths"
            ),
            allowed_values=[
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="DJF",
                    description="Represents the winter season (December, January, February)",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="MAM",
                    description="Represents the spring season (March, April, May)",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="JJA",
                    description="Represents the summer season (June, July, August)",
                ),
                ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="SON",
                    description="Represents the autumn season (September, October, November)",
                ),
            ],
        ),
    ]
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        for param_create in params:
            try:
                db_param = database.create_configuration_parameter(
                    session, param_create
                )
                print(f"Created configuration parameter {db_param.name!r}")
            except IntegrityError as err:
                print(
                    f"Could not create configuration parameter "
                    f"{param_create.name!r}: {err}"
                )
                session.rollback()
    print("Done!")


@app.command("coverage-configurations")
def bootstrap_coverage_configurations(
    ctx: typer.Context,
):
    """Create initial coverage configurations."""
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        all_vars = database.collect_all_variables(session)
        all_conf_param_values = database.collect_all_configuration_parameter_values(
            session
        )
        variables = {v.name: v for v in all_vars}
        conf_param_values = {
            (pv.configuration_parameter.name, pv.name): pv
            for pv in all_conf_param_values
        }
    coverage_configurations = [
        CoverageConfigurationCreate(
            name="tas_seasonal_anomaly_model_ensemble",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="ens5ym/clipped/tas_anom_pp_ts_{scenario}_{year_period}_VFVGTAA.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
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
            name="tas_seasonal_anomaly_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ym/clipped/tas_EC-EARTH_CCLM4-8-17_{scenario}_{year_period}_anomaly_pp_VFVGTAA.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
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
            name="tas_seasonal_anomaly_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="EC-EARTH_RACMO22Eym/tas_EC-EARTH_RACMO22E_{scenario}_{year_period}_anomaly_pp_VFVGTAA.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
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
            name="tas_seasonal_anomaly_model_ec_earth_rca4",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="EC-EARTH_RCA4ym/tas_EC-EARTH_RCA4_{scenario}_{year_period}_anomaly_pp_VFVGTAA.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
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
            name="tas_seasonal_anomaly_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eym/tas_HadGEM2-ES_RACMO22E_{scenario}_{year_period}_anomaly_pp_VFVGTAA.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
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
            name="tas_seasonal_anomaly_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ym/tas_MPI-ESM-LR_REMO2009_{scenario}_{year_period}_anomaly_pp_VFVGTAA.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=6,
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
            name="pr_seasonal_anomaly_model_ensemble",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="ens5ym/clipped/pr_anom_pp_ts_{scenario}_{year_period}_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBg",
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
            palette="default/div-BrBg",
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
            thredds_url_pattern="EC-EARTH_RACMO22Eym/pr_EC-EARTH_RACMO22E_{scenario}_{year_period}_anomaly_pp_percentage_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBg",
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
            thredds_url_pattern="EC-EARTH_RCA4ym/pr_EC-EARTH_RCA4_{scenario}_{year_period}_anomaly_pp_percentage_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBg",
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
            thredds_url_pattern="HadGEM2-ES_RACMO22Eym/pr_HadGEM2-ES_RACMO22E_{scenario}_{year_period}_anomaly_pp_percentage_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBg",
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
            thredds_url_pattern="MPI-ESM-LR_REMO2009ym/pr_MPI-ESM-LR_REMO2009_{scenario}_{year_period}_anomaly_pp_percentage_VFVGTAA.nc",
            unit="%",
            palette="default/div-BrBg",
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
            name="tas_seasonal_anomaly_model_ensemble_upper_uncertainty",
            netcdf_main_dataset_name="tas_stdup",
            thredds_url_pattern="ens5ym/std/clipped/tas_anom_stdup_pp_ts_{scenario}_{year_period}_VFVGTAA.nc",
            unit="ºC",
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
            name="tas_seasonal_anomaly_model_ensemble_lower_uncertainty",
            netcdf_main_dataset_name="tas_stddown",
            thredds_url_pattern="ens5ym/std/clipped/tas_anom_stddown_pp_ts_{scenario}_{year_period}_VFVGTAA.nc",
            unit="ºC",
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
            name="tas_seasonal_absolute_model_ensemble",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="ensymbc/std/clipped/tas_avg_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TDd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tas_annual_absolute_model_ensemble",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="ensymbc/clipped/tas_avg_{scenario}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TDd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmax_seasonal_absolute_model_ensemble",
            netcdf_main_dataset_name="tasmax",
            thredds_url_pattern="ensymbc/std/clipped/tasmax_avg_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmin_seasonal_absolute_model_ensemble",
            netcdf_main_dataset_name="tasmin",
            thredds_url_pattern="ensymbc/std/clipped/tasmin_avg_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TNd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmin_annual_absolute_model_ensemble",
            netcdf_main_dataset_name="tasmin",
            thredds_url_pattern="ensymbc/clipped/tasmin_avg_{scenario}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TNd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="pr_seasonal_absolute_model_ensemble",
            netcdf_main_dataset_name="pr",
            thredds_url_pattern="ensymbc/std/clipped/pr_avg_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="fd_annual_absolute_model_ensemble",
            netcdf_main_dataset_name="fd",
            thredds_url_pattern="ensymbc/std/clipped/ecafd_0_avg_{scenario}_ts19762100_ls_VFVG.nc",
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="su30_annual_absolute_model_ensemble",
            netcdf_main_dataset_name="su30",
            thredds_url_pattern="ensymbc/std/clipped/ecasu_30_avg_{scenario}_ts19762100_ls_VFVG.nc",
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tr_annual_absolute_model_ensemble",
            netcdf_main_dataset_name="tr",
            thredds_url_pattern="ensymbc/std/clipped/ecatr_20_avg_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=120,
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
                v.id if (v := variables.get("TR")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
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
            name="tas_seasonal_absolute_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ymbc/clipped/tas_EC-EARTH_CCLM4-8-17_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TDd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tas_annual_absolute_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ymbc/clipped/tas_EC-EARTH_CCLM4-8-17_{scenario}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TDd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmin_seasonal_absolute_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="tasmin",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ymbc/clipped/tasmin_EC-EARTH_CCLM4-8-17_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TNd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmin_annual_absolute_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="tasmin",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ymbc/clipped/tasmin_EC-EARTH_CCLM4-8-17_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-13,
            color_scale_max=27,
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
                v.id if (v := variables.get("TNd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tr_annual_absolute_model_ec_earth_cclm4_8_17",
            netcdf_main_dataset_name="tr",
            thredds_url_pattern="EC-EARTH_CCLM4-8-17ymbc/clipped/ecatr_20_EC-EARTH_CCLM4-8-17_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=120,
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
                v.id if (v := variables.get("TR")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            name="tas_seasonal_absolute_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="EC-EARTH_RACMO22Eymbc/clipped/tas_EC-EARTH_RACMO22E_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TDd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tas_annual_absolute_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="EC-EARTH_RACMO22Eymbc/clipped/tas_EC-EARTH_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TDd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmin_seasonal_absolute_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="tasmin",
            thredds_url_pattern="EC-EARTH_RACMO22Eymbc/clipped/tasmin_EC-EARTH_RACMO22E_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TNd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmin_annual_absolute_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="tasmin",
            thredds_url_pattern="EC-EARTH_RACMO22Eymbc/clipped/tasmin_EC-EARTH_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-13,
            color_scale_max=27,
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
                v.id if (v := variables.get("TNd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tr_annual_absolute_model_ec_earth_racmo22e",
            netcdf_main_dataset_name="tr",
            thredds_url_pattern="EC-EARTH_RACMO22Eymbc/clipped/ecatr_20_EC-EARTH_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=120,
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
                v.id if (v := variables.get("TR")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            name="tas_seasonal_absolute_model_ec_earth_rca4",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="EC-EARTH_RCA4ymbc/clipped/tas_EC-EARTH_RCA4_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TDd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tas_annual_absolute_model_ec_earth_rca4",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="EC-EARTH_RCA4ymbc/clipped/tas_EC-EARTH_RCA4_{scenario}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TDd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmin_seasonal_absolute_model_ec_earth_rca4",
            netcdf_main_dataset_name="tasmin",
            thredds_url_pattern="EC-EARTH_RCA4ymbc/clipped/tasmin_EC-EARTH_RCA4_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TNd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmin_annual_absolute_model_ec_earth_rca4",
            netcdf_main_dataset_name="tasmin",
            thredds_url_pattern="EC-EARTH_RCA4ymbc/clipped/tasmin_EC-EARTH_RCA4_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-13,
            color_scale_max=27,
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
                v.id if (v := variables.get("TNd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tr_annual_absolute_model_ec_earth_rca4",
            netcdf_main_dataset_name="tr",
            thredds_url_pattern="EC-EARTH_RCA4ymbc/clipped/ecatr_20_EC-EARTH_RCA4_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=120,
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
                v.id if (v := variables.get("TR")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            name="tas_seasonal_absolute_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eymbc/clipped/tas_HadGEM2-ES_RACMO22E_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TDd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tas_annual_absolute_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eymbc/clipped/tas_HadGEM2-ES_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TDd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmin_seasonal_absolute_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="tasmin",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eymbc/clipped/tasmin_HadGEM2-ES_RACMO22E_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TNd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmin_annual_absolute_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="tasmin",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eymbc/clipped/tasmin_HadGEM2-ES_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-13,
            color_scale_max=27,
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
                v.id if (v := variables.get("TNd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tr_annual_absolute_model_hadgem2_es_racmo22e",
            netcdf_main_dataset_name="tr",
            thredds_url_pattern="HadGEM2-ES_RACMO22Eymbc/clipped/ecatr_20_HadGEM2-ES_RACMO22E_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=120,
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
                v.id if (v := variables.get("TR")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            name="tas_seasonal_absolute_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ymbc/clipped/tas_MPI-ESM-LR_REMO2009_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TDd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tas_annual_absolute_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ymbc/clipped/tas_MPI-ESM-LR_REMO2009_{scenario}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TDd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
        ),
        CoverageConfigurationCreate(
            name="tasmin_seasonal_absolute_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="tasmin",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ymbc/clipped/tasmin_MPI-ESM-LR_REMO2009_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
                v.id if (v := variables.get("TNd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tasmin_annual_absolute_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="tasmin",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ymbc/clipped/tasmin_MPI-ESM-LR_REMO2009_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-13,
            color_scale_max=27,
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
                v.id if (v := variables.get("TNd")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.YEARLY,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
        ),
        CoverageConfigurationCreate(
            name="tr_annual_absolute_model_mpi_esm_lr_remo2009",
            netcdf_main_dataset_name="tr",
            thredds_url_pattern="MPI-ESM-LR_REMO2009ymbc/clipped/ecatr_20_MPI-ESM-LR_REMO2009_{scenario}_ts19762100_ls_VFVG.nc",
            unit="gg",
            palette="default/seq-YlOrRd",
            color_scale_min=0,
            color_scale_max=120,
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
                v.id if (v := variables.get("TR")) is not None else None
            ),
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL,
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
            name="tas_seasonal_absolute_model_ensemble_upper_uncertainty",
            netcdf_main_dataset_name="tas_stdup",
            thredds_url_pattern="ensymbc/std/clipped/tas_stdup_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
        ),
        CoverageConfigurationCreate(
            name="tas_seasonal_absolute_model_ensemble_lower_uncertainty",
            netcdf_main_dataset_name="tas_stddown",
            thredds_url_pattern="ensymbc/std/clipped/tas_stddown_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
        ),
        CoverageConfigurationCreate(
            name="tas_annual_absolute_model_ensemble_upper_uncertainty",
            netcdf_main_dataset_name="tas_stdup",
            thredds_url_pattern="ensymbc/std/clipped/tas_stdup_{scenario}_ts19762100_ls_VFVG.nc",
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
        ),
        CoverageConfigurationCreate(
            name="tas_annual_absolute_model_ensemble_lower_uncertainty",
            netcdf_main_dataset_name="tas_stddown",
            thredds_url_pattern="ensymbc/std/clipped/tas_stddown_{scenario}_ts19762100_ls_VFVG.nc",
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
            name="tasmin_seasonal_absolute_model_ensemble_upper_uncertainty",
            netcdf_main_dataset_name="tasmin_stdup",
            thredds_url_pattern="ensymbc/std/clipped/tasmin_stdup_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-13,
            color_scale_max=27,
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
            name="tasmin_seasonal_absolute_model_ensemble_lower_uncertainty",
            netcdf_main_dataset_name="tasmin_stddown",
            thredds_url_pattern="ensymbc/std/clipped/tasmin_stddown_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-13,
            color_scale_max=27,
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
            name="tasmin_annual_absolute_model_ensemble_upper_uncertainty",
            netcdf_main_dataset_name="tasmin_stdup",
            thredds_url_pattern="ensymbc/std/clipped/tasmin_stdup_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-13,
            color_scale_max=27,
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
            name="tasmin_annual_absolute_model_ensemble_lower_uncertainty",
            netcdf_main_dataset_name="tasmin_stddown",
            thredds_url_pattern="ensymbc/std/clipped/tasmin_stddown_{scenario}_ts19762100_ls_VFVG.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-13,
            color_scale_max=27,
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
            thredds_url_pattern="ensymbc/std/clipped/ecafd_0_stddown_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
            thredds_url_pattern="ensymbc/std/clipped/ecasu_30_stddown_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
            name="tr_annual_absolute_model_ensemble_upper_uncertainty",
            netcdf_main_dataset_name="tr_stdup",
            thredds_url_pattern="ensymbc/std/clipped/ecatr_20_stdup_{scenario}_ts19762100_ls_VFVG.nc",
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
            name="tr_annual_absolute_model_ensemble_lower_uncertainty",
            netcdf_main_dataset_name="tr_stddown",
            thredds_url_pattern="ensymbc/std/clipped/ecatr_20_stddown_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
            thredds_url_pattern="ensymbc/std/clipped/ecatr_20_stddown_{scenario}_{year_period}_ts19762100_ls_VFVG.nc",
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
    ]
    for cov_conf_create in coverage_configurations:
        try:
            db_cov_conf = database.create_coverage_configuration(
                session, cov_conf_create
            )
            print(f"Created coverage configuration {db_cov_conf.name!r}")
        except IntegrityError as err:
            print(
                f"Could not create coverage configuration "
                f"{cov_conf_create.name!r}: {err}"
            )
            session.rollback()
