import random
from unittest import mock

import httpx

from arpav_ppcv.schemas import coverages

random.seed(0)


def test_coverage_configurations_list(
    test_client_v2_app: httpx.Client,
    sample_coverage_configurations: list[coverages.CoverageConfiguration],
):
    list_response = test_client_v2_app.get(
        test_client_v2_app.app.url_path_for("list_coverage_configurations"),
        headers={"accept": "application/json"},
    )
    assert list_response.status_code == 200
    assert len(list_response.json()["items"]) == 10


def test_coverage_identifiers_list(
    test_client_v2_app: httpx.Client,
    sample_coverage_configurations: list[coverages.CoverageConfiguration],
):
    list_response = test_client_v2_app.get(
        test_client_v2_app.app.url_path_for("list_coverage_identifiers"),
        headers={"accept": "application/json"},
    )
    assert list_response.status_code == 200


def test_get_time_series(
    test_client_v2_app: httpx.Client,
    sample_coverage_configurations: list[coverages.CoverageConfiguration],
    sample_csv_data: str,
):
    cov_conf = random.choice(sample_coverage_configurations)
    with mock.patch("arpav_ppcv.operations.ncss") as mock_ncss_module:
        mock_query_dataset = mock.AsyncMock()
        mock_query_dataset.return_value = sample_csv_data
        mock_ncss_module.query_dataset.return_value = mock_query_dataset
        series_response = test_client_v2_app.get(
            test_client_v2_app.app.url_path_for(
                "get_time_series", coverage_identifier=str(cov_conf.id)
            ),
            params={
                "coords": "POINT(11.5469 44.9524)",
                "include_observation_data": False,
            },
            headers={"accept": "application/json"},
        )
        assert series_response.status_code == 200
