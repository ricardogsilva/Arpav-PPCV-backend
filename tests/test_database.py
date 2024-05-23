import pytest
import random

from arpav_ppcv import database
from arpav_ppcv.schemas import coverages


@pytest.mark.parametrize(
    "limit, offset, include_total",
    [
        pytest.param(10, 0, False),
        pytest.param(10, 0, True),
        pytest.param(20, 20, True),
    ],
)
def test_list_stations(arpav_db_session, sample_stations, limit, offset, include_total):
    ordered_stations = sorted(sample_stations, key=lambda station: station.code)
    expected_codes = [s.code for s in ordered_stations][offset : offset + limit]
    db_stations, total = database.list_stations(
        arpav_db_session, limit=limit, offset=offset, include_total=include_total
    )
    if include_total:
        assert total == len(sample_stations)
    else:
        assert total is None
    for index, db_station in enumerate(db_stations):
        assert db_station.code == expected_codes[index]


@pytest.mark.parametrize(
    "limit, offset, include_total",
    [
        pytest.param(10, 0, False),
        pytest.param(10, 0, True),
        pytest.param(5, 2, True),
    ],
)
def test_list_variables(
    arpav_db_session, sample_variables, limit, offset, include_total
):
    ordered_variables = sorted(sample_variables, key=lambda variable: variable.name)
    expected_names = [v.name for v in ordered_variables][offset : offset + limit]
    db_variables, total = database.list_variables(
        arpav_db_session, limit=limit, offset=offset, include_total=include_total
    )
    if include_total:
        assert total == len(sample_variables)
    else:
        assert total is None
    for index, db_variable in enumerate(db_variables):
        assert db_variable.name == expected_names[index]


@pytest.mark.parametrize(
    "limit, offset, include_total",
    [
        pytest.param(20, 0, False),
        pytest.param(20, 0, True),
        pytest.param(20, 20, True),
    ],
)
def test_list_monthly_measurements(
    arpav_db_session, sample_monthly_measurements, limit, offset, include_total
):
    ordered_measurements = sorted(sample_monthly_measurements, key=lambda m: m.date)
    expected_dates = [m.date for m in ordered_measurements][offset : offset + limit]
    db_measurements, total = database.list_monthly_measurements(
        arpav_db_session, limit=limit, offset=offset, include_total=include_total
    )
    if include_total:
        assert total == len(sample_monthly_measurements)
    else:
        assert total is None
    for index, db_measurement in enumerate(db_measurements):
        assert db_measurement.date == expected_dates[index]


@pytest.mark.parametrize("name, thredds_url_pattern", [
    pytest.param("fake_cov_conf1", "fake-thredds-pattern1"),
    pytest.param("fake_cov_conf2", " fake-thredds-pattern2 ", id="spaces in thredds url pattern edges"),
    # pytest.param("fake_cov_conf2", " fake-thredds-pattern2 ", id="invalid_name"),
])
def test_create_coverage_configuration_simple(
        arpav_db_session,
        name,
        thredds_url_pattern
):
    cov_conf_create = coverages.CoverageConfigurationCreate(
        name=name,
        netcdf_main_dataset_name="fake_ds",
        thredds_url_pattern=thredds_url_pattern,
        unit="fake_unit",
        palette="fake_palette",
        color_scale_min=0.0,
        color_scale_max=1.0,
        possible_values=[],
    )
    created = database.create_coverage_configuration(arpav_db_session, cov_conf_create)
    assert created.id is not None
    assert created.name == cov_conf_create.name
    assert created.thredds_url_pattern == cov_conf_create.thredds_url_pattern.strip()


def test_create_coverage_configuration_with_possible_values(
        arpav_db_session, sample_configuration_parameters):
    used_params = random.sample(sample_configuration_parameters, k=3)
    possible_values = []
    for used_param in used_params:
        possible_values.extend(
            random.sample(used_param.allowed_values, k=2)
        )
    print(f"possible_values: {[(type(pv), pv.model_dump()) for pv in possible_values]}")
    cov_conf_create = coverages.CoverageConfigurationCreate(
        name="fake_name",
        netcdf_main_dataset_name="fake_ds",
        thredds_url_pattern="fake_thredds_pattern",
        unit="fake_unit",
        palette="fake_palette",
        color_scale_min=0.0,
        color_scale_max=1.0,
        possible_values=[
            coverages.ConfigurationParameterPossibleValueCreate(
                configuration_parameter_value_id=p.id
            )
            for p in possible_values
        ],
    )
    created = database.create_coverage_configuration(arpav_db_session, cov_conf_create)
    assert created.id is not None
    for possible_value in possible_values:
        assert possible_value.id in [
            pv.configuration_parameter_value_id for pv in created.possible_values]


def test_create_coverage_configuration_value_uses_new_possible_values(
        arpav_db_session, sample_configuration_parameters
):
    used_param = sample_configuration_parameters[0]
    possible_value = used_param.allowed_values[0]
    cov_conf_create1 = coverages.CoverageConfigurationCreate(
        name="fake_name1",
        netcdf_main_dataset_name="fake_ds1",
        thredds_url_pattern="fake_thredds_pattern1",
        unit="fake_unit",
        palette="fake_palette",
        color_scale_min=0.0,
        color_scale_max=1.0,
        possible_values=[
            coverages.ConfigurationParameterPossibleValueCreate(
                configuration_parameter_value_id=possible_value.id)
        ],

    )
    created1 = database.create_coverage_configuration(
        arpav_db_session, cov_conf_create1)
    cov_conf_create2 = coverages.CoverageConfigurationCreate(
        name="fake_name2",
        netcdf_main_dataset_name="fake_ds2",
        thredds_url_pattern="fake_thredds_pattern2",
        unit="fake_unit",
        palette="fake_palette",
        color_scale_min=0.0,
        color_scale_max=1.0,
        possible_values=[
            coverages.ConfigurationParameterPossibleValueCreate(
                configuration_parameter_value_id=possible_value.id)
        ],

    )
    created2 = database.create_coverage_configuration(
        arpav_db_session, cov_conf_create2)
    assert created2.id is not None
    assert created2.possible_values[0] == possible_value
    assert created1.id is not None
    assert created1.possible_values[0] == possible_value
