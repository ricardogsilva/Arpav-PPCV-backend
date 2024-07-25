import random
import re

import httpx
import pytest_httpx

from arpav_ppcv.schemas import coverages
from arpav_ppcv import database

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
    httpx_mock: pytest_httpx.HTTPXMock,
    test_client_v2_app: httpx.Client,
    arpav_db_session,
    sample_tas_csv_data: str,
):
    db_cov_conf = coverages.CoverageConfiguration(
        name="fake_tas",
        netcdf_main_dataset_name="tas",
        thredds_url_pattern="fake",
        palette="fake",
    )
    arpav_db_session.add(db_cov_conf)
    arpav_db_session.commit()
    arpav_db_session.refresh(db_cov_conf)

    httpx_mock.add_response(
        url=re.compile(r".*ncss/grid.*"),
        method="get",
        text=sample_tas_csv_data,
    )
    identifiers = database.generate_coverage_identifiers(db_cov_conf)
    cov_id = random.choice(identifiers)
    series_response = test_client_v2_app.get(
        test_client_v2_app.app.url_path_for(
            "get_time_series", coverage_identifier=cov_id
        ),
        params={
            "coords": "POINT(11.5469 44.9524)",
            "include_observation_data": False,
            "coverage_data_smoothing": ["NO_SMOOTHING"],
        },
        headers={"accept": "application/json"},
    )
    print(series_response.content)
    assert series_response.status_code == 200
