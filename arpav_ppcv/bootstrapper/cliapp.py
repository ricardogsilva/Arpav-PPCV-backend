import json
from pathlib import Path

import geojson_pydantic
import sqlmodel
import typer
from rich import print
from sqlalchemy.exc import IntegrityError

from .. import database
from ..schemas import (
    municipalities,
    observations,
)

from ..schemas.coverages import (
    ConfigurationParameterCreate,
    ConfigurationParameterValueCreateEmbeddedInConfigurationParameter,
    ConfigurationParameterPossibleValueUpdate,
    CoverageConfigurationUpdate,
)

from .coverage_configurations import (
    cdd,
    fd,
    pr,
    r95ptot,
    snwdays,
    su30,
    tas,
    tasmax,
    tasmin,
    tr,
)

app = typer.Typer()


@app.command("municipalities")
def bootstrap_municipalities(ctx: typer.Context) -> None:
    """Bootstrap Italian municipalities."""
    data_directory = Path(__file__).parents[2] / "data"
    municipalities_dataset = data_directory / "limits_IT_municipalities.geojson"
    to_create = []
    with municipalities_dataset.open() as fh:
        municipalities_geojson = json.load(fh)
        for idx, feature in enumerate(municipalities_geojson["features"]):
            print(
                f"parsing feature ({idx+1}/{len(municipalities_geojson['features'])})..."
            )
            props = feature["properties"]
            mun_create = municipalities.MunicipalityCreate(
                geom=geojson_pydantic.MultiPolygon(
                    type="MultiPolygon", coordinates=feature["geometry"]["coordinates"]
                ),
                name=props["name"],
                province_name=props["prov_name"],
                region_name=props["reg_name"],
            )
            to_create.append(mun_create)
    print(f"About to save {len(to_create)} municipalities...")
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        database.create_many_municipalities(session, to_create)
    print("Done!")


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
    coverage_configurations.extend(cdd.generate_configurations(conf_param_values))
    coverage_configurations.extend(
        fd.generate_configurations(conf_param_values, variables)
    )
    coverage_configurations.extend(
        pr.generate_configurations(conf_param_values, variables)
    )
    coverage_configurations.extend(r95ptot.generate_configurations(conf_param_values))
    coverage_configurations.extend(snwdays.generate_configurations(conf_param_values))
    coverage_configurations.extend(
        su30.generate_configurations(conf_param_values, variables)
    )
    coverage_configurations.extend(
        tas.generate_configurations(conf_param_values, variables)
    )
    coverage_configurations.extend(
        tasmax.generate_configurations(conf_param_values, variables)
    )
    coverage_configurations.extend(
        tasmin.generate_configurations(conf_param_values, variables)
    )
    coverage_configurations.extend(
        tr.generate_configurations(conf_param_values, variables)
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

    print("Creating related coverage relationships...")
    all_cov_confs = {
        cc.name: cc for cc in database.collect_all_coverage_configurations(session)
    }

    to_update = {}
    for name, related_names in {
        **cdd.get_related_map(),
        **fd.get_related_map(),
        **pr.get_related_map(),
        **r95ptot.get_related_map(),
        **snwdays.get_related_map(),
        **su30.get_related_map(),
        **tas.get_related_map(),
        **tasmax.get_related_map(),
        **tasmin.get_related_map(),
        **tr.get_related_map(),
    }.items():
        to_update[name] = {
            "related": related_names,
        }

    for name, uncertainties in {
        **cdd.get_uncertainty_map(),
        **fd.get_uncertainty_map(),
        **pr.get_uncertainty_map(),
        **r95ptot.get_uncertainty_map(),
        **snwdays.get_uncertainty_map(),
        **su30.get_uncertainty_map(),
        **tas.get_uncertainty_map(),
        **tasmax.get_uncertainty_map(),
        **tasmin.get_uncertainty_map(),
        **tr.get_uncertainty_map(),
    }.items():
        info = to_update.setdefault(name, {})
        info["uncertainties"] = uncertainties

    for name, info in to_update.items():
        main_cov_conf = all_cov_confs[name]
        secondaries = info.get("related")
        uncertainties = info.get("uncertainties")
        update_kwargs = {}
        if secondaries is not None:
            secondary_cov_confs = [
                cc for name, cc in all_cov_confs.items() if name in secondaries
            ]
            update_kwargs["secondary_coverage_configurations_ids"] = [
                cc.id for cc in secondary_cov_confs
            ]
        if uncertainties is not None:
            lower_uncert_id = [
                cc.id for name, cc in all_cov_confs.items() if name == uncertainties[0]
            ][0]
            upper_uncert_id = [
                cc.id for name, cc in all_cov_confs.items() if name == uncertainties[1]
            ][0]
            update_kwargs.update(
                uncertainty_lower_bounds_coverage_configuration_id=lower_uncert_id,
                uncertainty_upper_bounds_coverage_configuration_id=upper_uncert_id,
            )
        cov_update = CoverageConfigurationUpdate(
            **main_cov_conf.model_dump(
                exclude={
                    "uncertainty_lower_bounds_coverage_configuration_id",
                    "uncertainty_upper_bounds_coverage_configuration_id",
                    "secondary_coverage_configurations_ids",
                    "possible_values",
                }
            ),
            **update_kwargs,
            possible_values=[
                ConfigurationParameterPossibleValueUpdate(
                    configuration_parameter_value_id=pv.configuration_parameter_value_id
                )
                for pv in main_cov_conf.possible_values
            ],
        )
        database.update_coverage_configuration(
            session,
            main_cov_conf,
            cov_update,
        )
