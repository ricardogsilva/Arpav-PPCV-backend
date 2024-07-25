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


@pytest.fixture()
def sample_coverage_configurations(
    arpav_db_session, sample_configuration_parameters
) -> list[coverages.CoverageConfiguration]:
    db_cov_confs = []
    for i in range(10):
        params_to_use = random.sample(sample_configuration_parameters, k=2)
        param_values_to_use = []
        for param in params_to_use:
            possible_value = coverages.ConfigurationParameterPossibleValue(
                configuration_parameter_value=random.choice(param.allowed_values)
            )
            param_values_to_use.append(possible_value)
        db_cov_confs.append(
            coverages.CoverageConfiguration(
                name=f"coverage_configuration{i}",
                netcdf_main_dataset_name="some-dataset-name",
                thredds_url_pattern=(
                    f"the_thredds-param_"
                    f"{{"
                    f"{random.choice(param_values_to_use).configuration_parameter_value.configuration_parameter.name}"
                    f"}}"
                ),
                palette="fake",
                possible_values=param_values_to_use,
            )
        )
    for db_cov_conf in db_cov_confs:
        arpav_db_session.add(db_cov_conf)
    arpav_db_session.commit()
    for db_cov_conf in db_cov_confs:
        arpav_db_session.refresh(db_cov_conf)
    return db_cov_confs


@pytest.fixture()
def sample_tas_csv_data():
    return """
    time,station,latitude[unit="degrees_north"],longitude[unit="degrees_east"],tas[unit="degC"]
    1976-02-15T12:00:00Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,2.640222
    1977-02-14T17:57:04.390Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,4.131799
    1978-02-14T23:54:08.780Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,2.9139953
    1979-02-15T05:51:13.171Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.9587035
    1980-02-15T11:48:17.561Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.5937133
    1981-02-14T17:45:21.951Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.7524657
    1982-02-14T23:42:26.341Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.8758483
    1983-02-15T05:39:30.732Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.5044188
    1984-02-15T11:36:35.122Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,2.284906
    1985-02-14T17:33:39.512Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,4.2877746
    1986-02-14T23:30:43.902Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.3630004
    1987-02-15T05:27:48.293Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,2.611383
    1988-02-15T11:24:52.683Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.5216613
    1989-02-14T17:21:57.073Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.7202392
    1990-02-14T23:19:01.463Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,4.1510253
    1991-02-15T05:16:05.854Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.5604796
    1992-02-15T11:13:10.244Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,2.830011
    1993-02-14T17:10:14.634Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.3071227
    1994-02-14T23:07:19.024Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,4.4500365
    1995-02-15T05:04:23.415Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,4.8746276
    1996-02-15T11:01:27.805Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,4.0703063
    1997-02-14T16:58:32.195Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,4.0519347
    1998-02-14T22:55:36.585Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.9186034
    1999-02-15T04:52:40.976Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,4.3369384
    2000-02-15T10:49:45.366Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,4.413568
    2001-02-14T16:46:49.756Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.7551513
    2002-02-14T22:43:54.146Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.6977477
    2003-02-15T04:40:58.537Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,4.3922668
    2004-02-15T10:38:02.927Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,4.298364
    2005-02-14T16:35:07.317Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.7203918
    2006-02-14T22:32:11.707Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,5.3815246
    2007-02-15T04:29:16.098Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.568109
    2008-02-15T10:26:20.488Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,4.08172
    2009-02-14T16:23:24.878Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,4.7300353
    2010-02-14T22:20:29.268Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,4.7169127
    2011-02-15T04:17:33.659Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.357843
    2012-02-15T10:14:38.049Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,2.469293
    2013-02-14T16:11:42.439Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.4914489
    2014-02-14T22:08:46.829Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,4.1174865
    2015-02-15T04:05:51.220Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,4.338098
    2016-02-15T10:02:55.610Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,5.111444
    2017-02-14T16:00:00Z,GridPointRequestedAt[44.952N_11.547E],44.953,11.547,3.911859
    """.strip()


def _override_get_settings():
    standard_settings = config.get_settings()
    return standard_settings


def _override_get_db_engine(settings=Depends(dependencies.get_settings)):
    yield database.get_engine(settings, use_test_db=True)


def _override_get_db_session(engine=Depends(dependencies.get_db_engine)):
    with sqlmodel.Session(autocommit=False, autoflush=False, bind=engine) as session:
        yield session
