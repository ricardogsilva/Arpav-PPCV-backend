import datetime as dt

import pytest
from pandas.core.dtypes.common import (
    is_datetime64_ns_dtype,
    is_float_dtype,
)

from arpav_ppcv import (
    database,
    operations,
)
from arpav_ppcv.schemas import coverages


@pytest.mark.parametrize(
    "temporal_range, expected",
    [
        pytest.param("../..", (None, None)),
        pytest.param(
            "1982-12-10T01:01:00Z/..",
            (dt.datetime(1982, 12, 10, 1, 1, 0, tzinfo=dt.timezone.utc), None),
        ),
        pytest.param(
            "1982-12-10T01:01:00+01:00/..",
            (dt.datetime(1982, 12, 10, 0, 1, 0, tzinfo=dt.timezone.utc), None),
        ),
        pytest.param(
            "1982-12-10T01:01:00+02:00/..",
            (dt.datetime(1982, 12, 9, 23, 1, 0, tzinfo=dt.timezone.utc), None),
        ),
    ],
)
def test_parse_temporal_range(temporal_range, expected):
    result = operations._parse_temporal_range(temporal_range)
    assert result == expected


@pytest.mark.parametrize(
    [
        "time_start",
        "time_end",
        "expected_first_tas_value",
        "expected_last_tas_value",
        "expected_first_dt_value",
        "expected_last_dt_value",
    ],
    [
        pytest.param(
            None,
            None,
            2.640222,
            3.911859,
            "1976-02-15T12:00:00+00:00",
            "2017-02-14T16:00:00+00:00",
        ),
        pytest.param(
            dt.datetime(1980, 1, 1),
            None,
            3.5937133,
            3.911859,
            "1980-02-15T11:48:17.561000+00:00",
            "2017-02-14T16:00:00+00:00",
        ),
        pytest.param(
            None,
            dt.datetime(2000, 1, 1),
            2.640222,
            4.3369384,
            "1976-02-15T12:00:00+00:00",
            "1999-02-15T04:52:40.976000+00:00",
        ),
        pytest.param(
            dt.datetime(1980, 1, 1),
            dt.datetime(2000, 1, 1),
            3.5937133,
            4.3369384,
            "1980-02-15T11:48:17.561000+00:00",
            "1999-02-15T04:52:40.976000+00:00",
        ),
    ],
)
def test_parse_ncss_dataset(
    sample_tas_csv_data,
    time_start,
    time_end,
    expected_first_tas_value,
    expected_last_tas_value,
    expected_first_dt_value,
    expected_last_dt_value,
):
    result = operations._parse_ncss_dataset(
        raw_data=sample_tas_csv_data["tas"],
        source_main_ds_name="tas",
        time_start=time_start,
        time_end=time_end,
        target_main_ds_name="tas",
    )
    assert result.index.name == "time"
    assert is_datetime64_ns_dtype(result.index.dtype)
    assert is_float_dtype(result.tas)
    assert result.index[0].isoformat() == expected_first_dt_value
    assert result.index[-1].isoformat() == expected_last_dt_value
    assert result.tas[0] == pytest.approx(expected_first_tas_value)
    assert result.tas[-1] == pytest.approx(expected_last_tas_value)


@pytest.mark.parametrize(
    "cov_conf_name, cov_identifier, expected_lower_identifier, expected_upper_identifier",
    [
        pytest.param(
            "tas_seasonal_anomaly_model_ensemble",
            "tas_seasonal_anomaly_model_ensemble-annual-forecast-model_ensemble-tas-anomaly-rcp26-MAM",
            "tas_seasonal_anomaly_model_ensemble_lower_uncertainty-annual-forecast-model_ensemble-tas-anomaly-rcp26-lower_bound-MAM",
            "tas_seasonal_anomaly_model_ensemble_upper_uncertainty-annual-forecast-model_ensemble-tas-anomaly-rcp26-upper_bound-MAM",
        ),
        pytest.param(
            "tas_annual_absolute_model_ensemble",
            "tas_annual_absolute_model_ensemble-annual-forecast-model_ensemble-tas-absolute-rcp26-year",
            "tas_annual_absolute_model_ensemble_lower_uncertainty-annual-forecast-model_ensemble-tas-absolute-rcp26-lower_bound-year",
            "tas_annual_absolute_model_ensemble_upper_uncertainty-annual-forecast-model_ensemble-tas-absolute-rcp26-upper_bound-year",
        ),
    ],
)
def test_get_related_uncertainty_coverage_configurations(
    arpav_db_session,
    sample_real_coverage_configurations: list[coverages.CoverageConfiguration],  # noqa
    cov_conf_name,
    cov_identifier,
    expected_lower_identifier,
    expected_upper_identifier,
):
    cov_conf = database.get_coverage_configuration_by_name(
        arpav_db_session, cov_conf_name
    )
    lower_, upper_ = operations.get_related_uncertainty_coverage_configurations(
        arpav_db_session,
        coverage=coverages.CoverageInternal(
            configuration=cov_conf, identifier=cov_identifier
        ),
    )
    assert lower_.identifier == expected_lower_identifier
    assert upper_.identifier == expected_upper_identifier


@pytest.mark.parametrize(
    "cov_conf_name, cov_identifier, expected_related_coverage_identifiers",
    [
        pytest.param(
            "tas_seasonal_anomaly_model_ensemble",
            "tas_seasonal_anomaly_model_ensemble-annual-forecast-model_ensemble-tas-anomaly-rcp26-MAM",
            [
                "tas_seasonal_anomaly_model_ec_earth_cclm4_8_17-annual-forecast-ec_earth_cclm_4_8_17-tas-anomaly-rcp26-MAM",
                "tas_seasonal_anomaly_model_ec_earth_racmo22e-annual-forecast-ec_earth_racmo22e-tas-anomaly-rcp26-MAM",
                "tas_seasonal_anomaly_model_ec_earth_rca4-annual-forecast-ec_earth_rca4-tas-anomaly-rcp26-MAM",
                "tas_seasonal_anomaly_model_hadgem2_es_racmo22e-annual-forecast-hadgem2_racmo22e-tas-anomaly-rcp26-MAM",
                "tas_seasonal_anomaly_model_mpi_esm_lr_remo2009-annual-forecast-mpi_esm_lr_remo2009-tas-anomaly-rcp26-MAM",
            ],
        )
    ],
)
def test_get_related_coverage_configurations(
    arpav_db_session,
    sample_real_coverage_configurations: list[coverages.CoverageConfiguration],  # noqa
    cov_conf_name,
    cov_identifier,
    expected_related_coverage_identifiers,
):
    cov_conf = database.get_coverage_configuration_by_name(
        arpav_db_session, cov_conf_name
    )
    related = operations.get_related_coverages(
        coverage=coverages.CoverageInternal(
            configuration=cov_conf, identifier=cov_identifier
        )
    )
    related_cov_identifiers = [c.identifier for c in related]
    for expected_identifier in expected_related_coverage_identifiers:
        assert expected_identifier in related_cov_identifiers

    for found_identifier in related_cov_identifiers:
        assert found_identifier in expected_related_coverage_identifiers
