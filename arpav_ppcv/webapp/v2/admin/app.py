import functools
import logging
from typing import Dict, Any, Union, Optional, List, Sequence

import anyio.to_thread
import starlette_admin
from starlette.requests import Request
from starlette_admin.contrib.sqlmodel import (
    Admin,
    ModelView,
)

from ....import (
    config,
    database,
)
from ....schemas import coverages

logger = logging.getLogger(__name__)


class ConfigurationParameterView(ModelView):
    identity = "configuration_parameter_view"
    name = "Configuration Parameter"
    label = "Configuration Parameters"
    icon = "fa fa-blog"
    pk_attr = "id"

    fields = (
        starlette_admin.StringField("name"),
        starlette_admin.StringField("description"),
        starlette_admin.ListField(
            field=starlette_admin.CollectionField(
                "allowed_values",
                fields=(
                    starlette_admin.StringField("name"),
                    starlette_admin.StringField("description"),
                )
            )
        )
    )

    async def create(self, request: Request, data: Dict[str, Any]) -> Any:
        logger.debug(f"Inside create - {locals()=}")
        try:
            data = await self._arrange_data(request, data)
            await self.validate(request, data)
            config_param_create = coverages.ConfigurationParameterCreate(
                name=data["name"],
                description=data["description"],
                allowed_values=[
                    coverages.ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
                        name=av["name"],
                        description=av["description"]
                    ) for av in data["allowed_values"]
                ]
            )
            db_configuration_parameter = await anyio.to_thread.run_sync(
                database.create_configuration_parameter,
                request.state.session,
                config_param_create
            )
            configuration_parameter_read = coverages.ConfigurationParameterRead(
                **db_configuration_parameter.model_dump()
            )
            logger.debug("About to leave the create instance")
            logger.debug(f"{configuration_parameter_read=}")
            return configuration_parameter_read
        except Exception as e:
            return self.handle_exception(e)

    async def find_all(
        self,
        request: Request,
        skip: int = 0,
        limit: int = 100,
        where: Union[Dict[str, Any], str, None] = None,
        order_by: Optional[List[str]] = None,
    ) -> Sequence[Any]:
        list_params = functools.partial(
            database.list_configuration_parameters,
            limit=limit,
            offset=skip,
            include_total=False
        )
        items, _ = await anyio.to_thread.run_sync(
            list_params, request.state.session)
        return items


def create_admin(settings: config.ArpavPpcvSettings) -> Admin:
    admin = Admin(
        database.get_engine(settings),
        debug=settings.debug
    )
    # admin.add_view(ModelView(coverages.ConfigurationParameterValue))
    # admin.add_view(ModelView(coverages.ConfigurationParameter))
    admin.add_view(
        ConfigurationParameterView(
            coverages.ConfigurationParameter,
            identity="configuration_parameter_view"
        )
    )
    return admin
