import logging

from django.conf import settings as django_settings
from django.core.wsgi import get_wsgi_application as get_django_wsgi_application
from django.core.handlers.wsgi import WSGIHandler

from ... import config
from .django_settings import get_custom_django_settings

logger = logging.getLogger(__name__)


def create_django_app(settings: config.ArpavPpcvSettings) -> WSGIHandler:
    custom_django_settings = get_custom_django_settings(settings)
    if not django_settings.configured:
        django_settings.configure(**custom_django_settings)
    else:
        logger.debug(
            "Skipping configuration of django settings, as they have been "
            "configured already"
        )
    # no need to call django.setup() here because get_django_wsgi_application
    # already takes care of that
    return get_django_wsgi_application()
