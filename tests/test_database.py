import pytest

from arpav_ppcv import database


@pytest.mark.parametrize(
    "limit, offset, include_total",
    [
        pytest.param(10, 0, False),
        pytest.param(10, 0, True),
        pytest.param(20, 20, True),
    ],
)
def test_list_stations(
        arpav_db_session,
        sample_stations,
        limit,
        offset,
        include_total
):
    ordered_stations = sorted(sample_stations, key=lambda station: station.code)
    expected_codes = [s.code for s in ordered_stations][offset:offset+limit]
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
        arpav_db_session,
        sample_variables,
        limit,
        offset,
        include_total
):
    ordered_variables = sorted(sample_variables, key=lambda variable: variable.name)
    expected_names = [v.name for v in ordered_variables][offset:offset+limit]
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
        arpav_db_session,
        sample_monthly_measurements,
        limit,
        offset,
        include_total
):
    ordered_measurements = sorted(
        sample_monthly_measurements, key=lambda m: m.date)
    expected_dates = [m.date for m in ordered_measurements][offset:offset+limit]
    db_measurements, total = database.list_monthly_measurements(
        arpav_db_session, limit=limit, offset=offset, include_total=include_total
    )
    if include_total:
        assert total == len(sample_monthly_measurements)
    else:
        assert total is None
    for index, db_measurement in enumerate(db_measurements):
        assert db_measurement.date == expected_dates[index]
