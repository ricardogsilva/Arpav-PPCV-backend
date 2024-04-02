import pytest
from django.conf import settings as django_settings
from fastapi.testclient import TestClient

from arpav_ppcv import config
from arpav_ppcv.webapp.app import create_app_from_settings
from arpav_ppcv.webapp.legacy.django_settings import get_custom_django_settings


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
    settings = config.ArpavPpcvSettings()
    yield settings


@pytest.fixture
def app(settings):
    app = create_app_from_settings(settings)
    yield app


@pytest.fixture
def test_client(app) -> TestClient:
    yield TestClient(app)
