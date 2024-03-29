import os

import fastapi
from django.core.wsgi import get_wsgi_application as get_django_wsgi_application
from django.core.handlers.wsgi import WSGIHandler
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

from .. import config
from .routers import router


def create_app() -> fastapi.FastAPI:
    settings = config.get_settings()
    app = fastapi.FastAPI(
        debug=settings.debug,
        title="ARPAV PPCV backend",
        description="""Developer API for ARPAV-PPCV backend""",
        contact={
            "name": settings.contact.name,
            "url": settings.contact.url,
            "email": settings.contact.email
        },
    )
    app.include_router(router, prefix="/api")
    django_app = get_django_app(settings)
    app.mount(settings.django_app.mount_prefix, WSGIMiddleware(django_app))
    settings.django_app.static_root.mkdir(parents=True, exist_ok=True)
    app.mount(
        settings.django_app.static_mount_prefix,
        StaticFiles(directory=settings.django_app.static_root),
        name="django_static"
    )
    return app


def get_django_app(settings: config.ArpavPpcvSettings) -> WSGIHandler:
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        settings.django_app.settings_module,
    )
    return get_django_wsgi_application()
