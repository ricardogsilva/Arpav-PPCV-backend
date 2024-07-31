import fastapi
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from .. import config
from .api_v2.app import create_app as create_v2_app
from .admin.app import create_admin
from .routes import routes


def create_app_from_settings(settings: config.ArpavPpcvSettings) -> fastapi.FastAPI:
    app = Starlette(
        debug=settings.debug,
        routes=routes,
    )
    settings.static_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")
    admin = create_admin(settings)
    admin.mount_to(app, settings)
    v2_api = create_v2_app(settings)
    app.state.settings = settings
    app.state.templates = Jinja2Templates(str(settings.templates_dir))
    app.state.v2_api_docs_url = "".join(
        (settings.public_url, settings.v2_api_mount_prefix, v2_api.docs_url)
    )
    app.mount(settings.v2_api_mount_prefix, v2_api)
    return app


def create_app() -> fastapi.FastAPI:
    settings = config.get_settings()
    return create_app_from_settings(settings)
