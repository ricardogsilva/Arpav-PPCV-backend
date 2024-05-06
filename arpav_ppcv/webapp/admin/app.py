import logging

from starlette.middleware import Middleware
from starlette_admin.contrib.sqlmodel import Admin
from starlette_admin.views import Link

from ...import (
    config,
    database,
)
from ...schemas import coverages
from . import views
from .middlewares import SqlModelDbSessionMiddleware

logger = logging.getLogger(__name__)


def create_admin(settings: config.ArpavPpcvSettings) -> Admin:
    engine = database.get_engine(settings)
    admin = Admin(
        engine,
        debug=settings.debug,
        templates_dir=str(settings.templates_dir / 'admin'),
        middlewares=[
            Middleware(SqlModelDbSessionMiddleware, engine=engine)
        ]
    )
    admin.add_view(
        views.ConfigurationParameterView(coverages.ConfigurationParameter))
    admin.add_view(
        views.CoverageConfigurationView(coverages.CoverageConfiguration))
    admin.add_view(
        Link(
            "V2 API docs",
            icon="fa fa-link",
            url=f"{settings.public_url}{settings.v2_api_mount_prefix}/docs",
            target="blank_"
        )
    )
    return admin
