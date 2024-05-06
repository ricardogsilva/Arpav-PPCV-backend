import fastapi

from ... import config
from .routers import (
    forecastattributes,
    maps,
    ncss,
    places,
)


def create_app(settings: config.ArpavPpcvSettings) -> fastapi.FastAPI:
    app = fastapi.FastAPI(
        debug=settings.debug,
        title="ARPAV PPCV backend v1",
        description=(
            "### Developer API for ARPAV-PPCV backend v1\n"
            "This is the documentation for API v1, which is merely a reimplementation "
            "of the legacy API, but taking advantage of the automatic OpenAPI document "
            "generation."
        ),
        contact={
            "name": settings.contact.name,
            "url": settings.contact.url,
            "email": settings.contact.email
        },
    )
    app.include_router(forecastattributes.router, prefix="/api")
    app.include_router(maps.router, prefix="/api")
    app.include_router(ncss.router, prefix="/api")
    app.include_router(places.router, prefix="/api")
    return app
