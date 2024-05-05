import logging

from starlette.middleware import Middleware
from starlette_admin.contrib.sqlmodel import Admin

from ....import (
    config,
    database,
)
from ....schemas import coverages
from . import views
from .middlewares import SqlModelDbSessionMiddleware

logger = logging.getLogger(__name__)


def create_admin(settings: config.ArpavPpcvSettings) -> Admin:
    engine = database.get_engine(settings)
    admin = Admin(
        engine,
        debug=settings.debug,
        middlewares=[
            Middleware(SqlModelDbSessionMiddleware, engine=engine)
        ]
    )
    admin.add_view(
        views.ConfigurationParameterView(
            coverages.ConfigurationParameter,
        )
    )
    return admin
