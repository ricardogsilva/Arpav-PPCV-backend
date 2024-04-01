from django.conf import settings as django_settings
from django.core.wsgi import get_wsgi_application as get_django_wsgi_application
from django.core.handlers.wsgi import WSGIHandler

from ... import config
from .django_settings import get_custom_django_settings


def create_django_app(settings: config.ArpavPpcvSettings) -> WSGIHandler:
    custom_django_settings = get_custom_django_settings(settings)
    django_settings.configure(**custom_django_settings)
    # no need to call django.setup() here because get_django_wsgi_application
    # already takes care of that
    return get_django_wsgi_application()
