import typer

import sqlmodel
from rich import print
from sqlalchemy.exc import IntegrityError

from .. import database
from ..schemas import observations

from ..schemas.coverages import (
    ConfigurationParameterCreate,
    ConfigurationParameterValueCreateEmbeddedInConfigurationParameter,
)

from .coverage_configurations.cdd import generate_cdd_configurations
from .coverage_configurations.fd import generate_fd_configurations
from .coverage_configurations.pr import generate_pr_configurations
from .coverage_configurations.r95ptot import generate_r95ptot_configurations
from .coverage_configurations.snwdays import generate_snwdays_configurations
from .coverage_configurations.su30 import generate_su30_configurations
from .coverage_configurations.tas import generate_tas_configurations
from .coverage_configurations.tasmax import generate_tasmax_configurations
from .coverage_configurations.tasmin import generate_tasmin_configurations
from .coverage_configurations.tr import generate_tr_configurations

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
    coverage_configurations = []
    coverage_configurations.extend(generate_cdd_configurations(conf_param_values))
    coverage_configurations.extend(
        generate_fd_configurations(conf_param_values, variables)
    )
    coverage_configurations.extend(
        generate_pr_configurations(conf_param_values, variables)
    )
    coverage_configurations.extend(generate_r95ptot_configurations(conf_param_values))
    coverage_configurations.extend(generate_snwdays_configurations(conf_param_values))
    coverage_configurations.extend(
        generate_su30_configurations(conf_param_values, variables)
    )
    coverage_configurations.extend(
        generate_tas_configurations(conf_param_values, variables)
    )
    coverage_configurations.extend(
        generate_tasmax_configurations(conf_param_values, variables)
    )
    coverage_configurations.extend(
        generate_tasmin_configurations(conf_param_values, variables)
    )
    coverage_configurations.extend(
        generate_tr_configurations(conf_param_values, variables)
    )

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
