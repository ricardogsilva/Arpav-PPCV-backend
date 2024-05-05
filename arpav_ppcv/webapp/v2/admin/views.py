"""Views for the admin app.

The classes contained in this module are derived from
starlette_admin.contrib.sqlmodel.ModelView. This is done mostly for two reasons:

1. To be able to control database access and ensure we are using our handlers
   defined in `arpav_ppcv.database` - this is meant for achieving consistency
   throughout the code, as the API is also using the mentioned functions for
   interacting with the DB

2. To be able to present inline forms for editing related objects, as is the
   case with parameter configuration and its related values.

"""

import functools
import logging
from typing import Dict, Any, Union, Optional, List, Sequence

import anyio.to_thread
import starlette_admin
from starlette.requests import Request
from starlette_admin import RequestAction
from starlette_admin.contrib.sqlmodel import ModelView
from starlette_admin.fields import StringField

from .... import database
from ....schemas import coverages
from . import schemas as read_schemas


logger = logging.getLogger(__name__)


class UuidField(StringField):

    async def serialize_value(
        self, request: Request, value: Any, action: RequestAction
    ) -> Any:
        return str(value)


class ConfigurationParameterView(ModelView):
    identity = "configuration_parameters"
    name = "Configuration Parameter"
    label = "Configuration Parameters"
    icon = "fa fa-blog"
    pk_attr = "id"

    exclude_fields_from_list = (
        "id",
    )
    exclude_fields_from_detail = (
        "id",
    )

    fields = (
        UuidField("id"),
        starlette_admin.StringField("name"),
        starlette_admin.StringField("description"),
        starlette_admin.ListField(
            field=starlette_admin.CollectionField(
                "allowed_values",
                fields=(
                    UuidField(
                        "id",
                        read_only=True,
                        disabled=True,
                        exclude_from_list=True,
                        exclude_from_detail=True,
                        exclude_from_create=True,
                        exclude_from_edit=False,
                ),
                    starlette_admin.StringField("name"),
                    starlette_admin.StringField(
                        "description",
                        exclude_from_list=True,
                    ),
                )
            )
        )
    )

    async def get_pk_value(self, request: Request, obj: Any) -> Any:
        # note: we need to cast the value, which is a uuid.UUID, to a string
        # because starlette_admin just assumes that the value of a model's
        # pk attribute is always JSON serializable so it doesn't bother with
        # calling the respective field's `serialize_value()` method
        result = await super().get_pk_value(request, obj)
        return str(result)

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
            configuration_parameter_read = read_schemas.ConfigurationParameterRead(
                **db_configuration_parameter.model_dump()
            )
            logger.debug("About to leave the create instance")
            logger.debug(f"{configuration_parameter_read=}")
            return configuration_parameter_read
        except Exception as e:
            return self.handle_exception(e)

    async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
        logger.debug(f"inside edit - {locals()=}")
        try:
            data = await self._arrange_data(request, data, True)
            await self.validate(request, data)
            config_param_update = coverages.ConfigurationParameterUpdate(
                name=data.get("name"),
                description=data.get("description"),
                allowed_values=[
                    coverages.ConfigurationParameterValueUpdateEmbeddedInConfigurationParameterEdit(
                        id=av["id"],
                        name=av.get("name"),
                        description=av.get("description")
                    ) for av in data["allowed_values"]
                ]
            )
            db_configuration_parameter = await anyio.to_thread.run_sync(
                database.get_configuration_parameter,
                request.state.session,
                pk
            )
            db_configuration_parameter = await anyio.to_thread.run_sync(
                database.update_configuration_parameter,
                request.state.session,
                db_configuration_parameter,
                config_param_update
            )
            conf_param_read = read_schemas.ConfigurationParameterRead(
                **db_configuration_parameter.model_dump(),
                allowed_values=[
                    read_schemas.ConfigurationParameterValueRead(**av.model_dump())
                    for av in db_configuration_parameter.allowed_values
                ]
            )
            return conf_param_read
        except Exception as e:
            self.handle_exception(e)

    async def find_by_pk(
            self,
            request: Request,
            pk: Any
    ) -> read_schemas.ConfigurationParameterRead:
        db_conf_param = await anyio.to_thread.run_sync(
            database.get_configuration_parameter,
            request.state.session,
            pk
        )
        return read_schemas.ConfigurationParameterRead(
            **db_conf_param.model_dump(),
            allowed_values=[
                read_schemas.ConfigurationParameterValueRead(**av.model_dump())
                for av in db_conf_param.allowed_values
            ]
        )

    async def find_all(
            self,
            request: Request,
            skip: int = 0,
            limit: int = 100,
            where: Union[Dict[str, Any], str, None] = None,
            order_by: Optional[List[str]] = None,
    ) -> Sequence[read_schemas.ConfigurationParameterRead]:
        list_params = functools.partial(
            database.list_configuration_parameters,
            limit=limit,
            offset=skip,
            include_total=False
        )
        db_conf_params, _ = await anyio.to_thread.run_sync(
            list_params, request.state.session)
        result = []
        for db_conf_param in db_conf_params:
            result.append(
                read_schemas.ConfigurationParameterRead(
                    **db_conf_param.model_dump(),
                    allowed_values=[
                        read_schemas.ConfigurationParameterValueRead(**av.model_dump())
                        for av in db_conf_param.allowed_values
                    ]
                )
            )
        return result