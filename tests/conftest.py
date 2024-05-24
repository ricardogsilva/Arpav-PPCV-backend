import datetime as dt
import random

import geojson_pydantic
import pytest
import shapely.io
import shapely.geometry
import sqlmodel
import typer
from django.conf import settings as django_settings
from fastapi import Depends
from fastapi.testclient import TestClient
from geoalchemy2.shape import from_shape
from typer.testing import CliRunner

from arpav_ppcv import (
    config,
    database,
    main,
)
from arpav_ppcv.schemas import (
    coverages,
    observations,
)
from arpav_ppcv.webapp import dependencies
from arpav_ppcv.webapp.app import create_app_from_settings
from arpav_ppcv.webapp.legacy.django_settings import get_custom_django_settings
from arpav_ppcv.webapp.api_v2.app import create_app as create_v2_app


@pytest.hookimpl
def pytest_configure():
    """Custom configuration of pytest.

    This custom configuration is here so that we may initialize django with the custom
    settings-retrieval mechanism that is being used in the project.
    """
    settings = config.ArpavPpcvSettings()
    custom_django_settings = get_custom_django_settings(settings)
    django_settings.configure(**custom_django_settings)


@pytest.fixture
def settings() -> config.ArpavPpcvSettings:
    settings = _override_get_settings()
    yield settings


@pytest.fixture
def app(settings):
    yield create_app_from_settings(settings)


@pytest.fixture
def v2_app(settings):
    app = create_v2_app(settings)
    app.dependency_overrides[dependencies.get_db_session] = _override_get_db_session
    app.dependency_overrides[dependencies.get_db_engine] = _override_get_db_engine
    app.dependency_overrides[dependencies.get_settings] = _override_get_settings
    yield app


@pytest.fixture()
def arpav_db(settings):
    """Provides a clean DB."""
    engine = next(_override_get_db_engine(settings))
    sqlmodel.SQLModel.metadata.create_all(engine)
    yield
    sqlmodel.SQLModel.metadata.drop_all(engine)
    # tables_to_truncate = list(sqlmodel.SQLModel.metadata.tables.keys())
    # tables_fragment = ', '.join(f'"{t}"' for t in tables_to_truncate)
    # with engine.connect() as connection:
    #     connection.execute(text(f"TRUNCATE {tables_fragment}"))


@pytest.fixture()
def arpav_db_session(arpav_db, settings):
    engine = next(_override_get_db_engine(settings))
    with sqlmodel.Session(autocommit=False, autoflush=False, bind=engine) as session:
        yield session


@pytest.fixture()
def test_client(app) -> TestClient:
    yield TestClient(app)


@pytest.fixture()
def test_client_v2_app(v2_app) -> TestClient:
    """This fixture exists in order to ensure app overrides work.

    See https://github.com/tiangolo/fastapi/issues/3651#issuecomment-892138488
    """
    yield TestClient(v2_app)


@pytest.fixture()
def cli_runner():
    runner = CliRunner(mix_stderr=False)
    yield runner


@pytest.fixture()
def cli_app(settings, arpav_db):
    # replaces the default callback with another one, with different settings
    @main.app.callback()
    def _override_main_app_callback(ctx: typer.Context):
        cli_config = ctx.obj or {}
        cli_config["settings"] = settings
        engine = next(_override_get_db_engine(settings))
        # engine = database.get_engine(settings, use_test_db=True)
        cli_config["engine"] = engine
        ctx.obj = cli_config

    yield main.app


@pytest.fixture()
def sample_stations(arpav_db_session) -> list[observations.Station]:
    db_stations = []
    for i in range(50):
        db_stations.append(
            observations.Station(
                code=f"teststation{i}",
                geom=from_shape(
                    shapely.io.from_geojson(
                        geojson_pydantic.Point(
                            type="Point", coordinates=(i, 2 * i)
                        ).model_dump_json()
                    )
                ),
                altitude_m=2,
                name=f"teststation{i}name",
                type_="sometype",
            )
        )
    for db_station in db_stations:
        arpav_db_session.add(db_station)
    arpav_db_session.commit()
    for db_station in db_stations:
        arpav_db_session.refresh(db_station)
    return db_stations


@pytest.fixture()
def sample_variables(arpav_db_session) -> list[observations.Variable]:
    db_variables = []
    for i in range(20):
        db_variables.append(
            observations.Variable(
                name=f"testvariable{i}",
                description=f"Description for test variable {i}",
            )
        )
    for db_variable in db_variables:
        arpav_db_session.add(db_variable)
    arpav_db_session.commit()
    for db_station in db_variables:
        arpav_db_session.refresh(db_station)
    return db_variables


@pytest.fixture()
def sample_monthly_measurements(
    arpav_db_session, sample_variables, sample_stations
) -> list[observations.MonthlyMeasurement]:
    db_monthly_measurements = []
    unique_measurement_instances = set()
    while len(unique_measurement_instances) < 200:
        sampled_date = dt.date(random.randrange(1920, 2020), random.randrange(1, 13), 1)
        sampled_station_id = random.choice(sample_stations).id
        sampled_variable_id = random.choice(sample_variables).id
        unique_measurement_instances.add(
            (sampled_date, sampled_station_id, sampled_variable_id)
        )

    for date_, station_id, variable_id in unique_measurement_instances:
        db_monthly_measurements.append(
            observations.MonthlyMeasurement(
                value=random.random() * 20 - 10,
                date=date_,
                station_id=station_id,
                variable_id=variable_id,
            )
        )
    for db_monthly_measurement in db_monthly_measurements:
        arpav_db_session.add(db_monthly_measurement)
    arpav_db_session.commit()
    for db_station in db_monthly_measurements:
        arpav_db_session.refresh(db_station)
    return db_monthly_measurements


@pytest.fixture()
def sample_configuration_parameters(arpav_db_session):
    db_conf_params = []
    for i in range(5):
        allowed_values = []
        for j in range(4):
            allowed_values.append(
                coverages.ConfigurationParameterValue(
                    name=f"fake_parameter_value{j}",
                    description=f"Description for fake param value {j}",
                )
            )
        db_conf_params.append(
            coverages.ConfigurationParameter(
                name=f"fake_parameter_{i}",
                description=f"Description for fake param {i}",
                allowed_values=allowed_values,
            )
        )
    for db_conf_param in db_conf_params:
        arpav_db_session.add(db_conf_param)
    arpav_db_session.commit()
    for db_conf_param in db_conf_params:
        arpav_db_session.refresh(db_conf_param)
    return db_conf_params


def _override_get_settings():
    standard_settings = config.get_settings()
    return standard_settings


def _override_get_db_engine(settings=Depends(dependencies.get_settings)):
    yield database.get_engine(settings, use_test_db=True)


def _override_get_db_session(engine=Depends(dependencies.get_db_engine)):
    with sqlmodel.Session(autocommit=False, autoflush=False, bind=engine) as session:
        yield session
