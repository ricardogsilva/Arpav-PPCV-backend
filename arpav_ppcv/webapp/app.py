import fastapi

from ..config import get_settings
from .routers import router


def create_app() -> fastapi.FastAPI:
    settings = get_settings()
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
    app.include_router(router)
    return app
