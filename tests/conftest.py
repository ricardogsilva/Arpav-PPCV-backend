import pytest
from fastapi.testclient import TestClient

from arpav_ppcv import config
from arpav_ppcv.webapp.app import create_app_from_settings


@pytest.fixture
def settings() -> config.ArpavPpcvSettings:
    settings = config.ArpavPpcvSettings()
    yield settings


@pytest.fixture
def app(settings):
    app = create_app_from_settings(settings)
    yield app


@pytest.fixture
def test_client(app) -> TestClient:
    yield TestClient(app)
