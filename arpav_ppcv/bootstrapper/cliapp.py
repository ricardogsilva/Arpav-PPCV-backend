import typer

import sqlmodel
from rich import print
from sqlalchemy.exc import IntegrityError

from .. import database
from ..schemas import (
    base,
    coverages,
    observations,
)

app = typer.Typer()


@app.command("observation-variables")
def bootstrap_observation_variables(
        ctx: typer.Context,
):
    """Create initial observation variables."""
    variables = [
        observations.VariableCreate(
            name="TDd",
            description="Mean temperature",
            unit="ºC"
        ),
        observations.VariableCreate(
            name="TXd",
            description="Max temperature",
            unit="ºC"
        ),
        observations.VariableCreate(
            name="TNd",
            description="Min temperature",
            unit="ºC"
        ),
        observations.VariableCreate(
            name="PRCPTOT",
            description="Total precipitation",
            unit="mm"
        ),
        observations.VariableCreate(
            name="TR",
            description="Tropical nights",
            unit="mm"
        ),
        observations.VariableCreate(
            name="SU30",
            description="Hot days",
            unit="mm"
        ),
        observations.VariableCreate(
            name="FD",
            description="Cold days",
            unit="mm"
        ),
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
        coverages.ConfigurationParameterCreate(
            name="scenario",
            description=(
                "Represents the path fragment related to forecast model scenario"
            ),
            allowed_values=[
                coverages.ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="rcp26",
                    description="Represents the RCP2.6 scenario"
                ),
                coverages.ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="rcp45",
                    description="Represents the RCP4.5 scenario"
                ),
                coverages.ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="rcp85",
                    description="Represents the RCP8.5 scenario"
                ),
            ]
        ),
        coverages.ConfigurationParameterCreate(
            name="time_window",
            description=(
                "Represents the path fragment related to forecast model time window"
            ),
            allowed_values=[
                coverages.ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="tw1",
                    description="Represents the first time window, which spans the period 2021-2050"
                ),
                coverages.ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="tw2",
                    description="Represents the second time window, which spans the period 2071-2100"
                ),
            ]
        ),
        coverages.ConfigurationParameterCreate(
            name="year_period",
            description=(
                "Represents the yearly temporal aggregation period in file paths"
            ),
            allowed_values=[
                coverages.ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="DJF",
                    description="Represents the winter season (December, January, February)"
                ),
                coverages.ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="MAM",
                    description="Represents the spring season (March, April, May)"
                ),
                coverages.ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="JJA",
                    description="Represents the summer season (June, July, August)"
                ),
                coverages.ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                    name="SON",
                    description="Represents the autumn season (September, October, November)"
                ),
            ]
        ),
    ]
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        for param_create in params:
            try:
                db_param = database.create_configuration_parameter(
                    session, param_create)
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
        all_conf_param_values = database.collect_all_configuration_parameter_values(session)
        variables = {v.name: v for v in all_vars}
        conf_param_values = {(pv.configuration_parameter.name, pv.name): pv for pv in all_conf_param_values}
    coverage_configurations = [
        coverages.CoverageConfigurationCreate(
            name="tas_absolute",
            netcdf_main_dataset_name="tas",
            thredds_url_pattern="ensymbc/tas_avg_{scenario}_{year_period}_ts19762100_ls.nc",
            unit="ºC",
            palette="default/seq-YlOrRd",
            color_scale_min=-3.0,
            color_scale_max=32.0,
            possible_values=[
                coverages.ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[("scenario", "rcp26")].id
                ),
                coverages.ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[("scenario", "rcp45")].id
                ),
                coverages.ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[("scenario", "rcp85")].id
                ),
                coverages.ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[("year_period", "DJF")].id
                ),
                coverages.ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[("year_period", "MAM")].id
                ),
                coverages.ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[("year_period", "JJA")].id
                ),
                coverages.ConfigurationParameterPossibleValueCreate(
                    configuration_parameter_value_id=conf_param_values[("year_period", "SON")].id
                ),
            ],
            observation_variable_id=v.id if (v := variables.get("TDd")) is not None else None,
            observation_variable_aggregation_type=base.ObservationAggregationType.SEASONAL
        ),
    ]
    for cov_conf_create in coverage_configurations:
        try:
            db_cov_conf = database.create_coverage_configuration(
                session, cov_conf_create)
            print(f"Created coverage configuration {db_cov_conf.name!r}")
        except IntegrityError as err:
            print(
                f"Could not create coverage configuration "
                f"{cov_conf_create.name!r}: {err}"
            )
            session.rollback()
