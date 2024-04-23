import fastapi
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

from .. import config
from .v2.app import create_app as create_v2_app
from .v1.app import create_app as create_v1_app
from .legacy.app import create_django_app
from .routers import router


def create_app_from_settings(settings: config.ArpavPpcvSettings) -> fastapi.FastAPI:
    v2_app = create_v2_app(settings)
    v2_docs_url = "".join(
        (settings.public_url, settings.v2_mount_prefix, v2_app.docs_url))
    v1_app = create_v1_app(settings)
    v1_docs_url = "".join(
        (settings.public_url, settings.v1_mount_prefix, v1_app.docs_url))
    django_app = create_django_app(settings)
    app = fastapi.FastAPI(
        debug=settings.debug,
        title="ARPAV PPCV backend",
        description=(
            f"### Developer API for ARPAV-PPCV backend\n"
            f"This is the root of the ARPAV-PPCV application - please head over "
            f"to either:\n"
            f"- <{v2_docs_url}> for info on version 2 of the API\n"
            f"- <{v1_docs_url}> for info on version 1 of the API\n"
            f"- <{''.join((settings.public_url, settings.django_app.mount_prefix))}> "
            f"for accessing the older django-rest-framework API - "
            f"There is no docs URL for this unfortunately\n"
        ),
        contact={
            "name": settings.contact.name,
            "url": settings.contact.url,
            "email": settings.contact.email
        },
    )
    app.include_router(router)
    app.mount(settings.v1_mount_prefix, v1_app)
    app.mount(settings.v2_mount_prefix, v2_app)
    app.mount(settings.django_app.mount_prefix, WSGIMiddleware(django_app))
    settings.django_app.static_root.mkdir(parents=True, exist_ok=True)
    app.mount(
        settings.django_app.static_mount_prefix,
        StaticFiles(directory=settings.django_app.static_root),
        name="django_static"
    )
    return app


def create_app() -> fastapi.FastAPI:
    settings = config.get_settings()
    return create_app_from_settings(settings)
