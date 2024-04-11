import fastapi

from ... import config
from .routers.thredds import router as thredds_router
from .routers.stations import router as stations_router


def create_app(settings: config.ArpavPpcvSettings) -> fastapi.FastAPI:
    app = fastapi.FastAPI(
        debug=settings.debug,
        title="ARPAV PPCV backend v2",
        description=(
            "### Developer API for ARPAV-PPCV backend v2\n"
            "This is the documentation for API v2, which is the new implementation "
            "of the system and is the recommended way to interact with it."
        ),
        contact={
            "name": settings.contact.name,
            "url": settings.contact.url,
            "email": settings.contact.email
        },
    )
    app.include_router(thredds_router, prefix="/api")
    app.include_router(stations_router, prefix="/api")
    return app
