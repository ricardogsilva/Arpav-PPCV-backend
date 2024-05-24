# station
# seasonal measurement
# monthly measurement
# yearly measurement

import functools
import logging
from typing import (
    Any,
    Optional,
    Sequence,
    Union,
)

import anyio
import geojson_pydantic
import shapely.io
import starlette_admin
from starlette.requests import Request
from starlette_admin.contrib.sqlmodel import ModelView

from .... import database as db
from ....schemas import observations
from .. import fields
from .. import schemas as read_schemas

logger = logging.getLogger(__name__)


class VariableView(ModelView):
    identity = "variables"
    name = "Variable"
    label = "Variables"
    icon = "fa fa-blog"
    pk_attr = "id"

    exclude_fields_from_list = ("id",)
    exclude_fields_from_detail = ("id",)

    fields = (
        fields.UuidField("id"),
        starlette_admin.StringField("name", required=True),
        starlette_admin.StringField("description", required=True),
        starlette_admin.StringField("unit"),
    )

    @staticmethod
    def _serialize_instance(
            instance: observations.Variable) -> read_schemas.VariableRead:
        return read_schemas.VariableRead(**instance.model_dump())

    async def get_pk_value(self, request: Request, obj: Any) -> str:
        # note: we need to cast the value, which is a uuid.UUID, to a string
        # because starlette_admin just assumes that the value of a model's
        # pk attribute is always JSON serializable so it doesn't bother with
        # calling the respective field's `serialize_value()` method
        result = await super().get_pk_value(request, obj)
        return str(result)

    async def create(
            self, request: Request, data: dict[str, Any]
    ) -> Optional[read_schemas.VariableRead]:
        try:
            data = await self._arrange_data(request, data)
            await self.validate(request, data)
            var_create = observations.VariableCreate(**data)
            db_variable = await anyio.to_thread.run_sync(
                db.create_variable,
                request.state.session,
                var_create,
            )
            return self._serialize_instance(db_variable)
        except Exception as e:
            return self.handle_exception(e)

    async def edit(
            self, request: Request, pk: Any, data: dict[str, Any]
    ) -> Optional[read_schemas.VariableRead]:
        try:
            data = await self._arrange_data(request, data, True)
            await self.validate(request, data)
            var_update = observations.VariableUpdate(**data)
            db_var = await anyio.to_thread.run_sync(
                db.get_variable, request.state.session, pk
            )
            db_var = await anyio.to_thread.run_sync(
                db.update_variable, request.state.session, db_var, var_update)
            return self._serialize_instance(db_var)
        except Exception as e:
            logger.exception("something went wrong")
            self.handle_exception(e)

    async def find_by_pk(
            self, request: Request, pk: Any
    ) -> read_schemas.VariableRead:
        db_var = await anyio.to_thread.run_sync(
            db.get_variable, request.state.session, pk)
        return self._serialize_instance(db_var)

    async def find_all(
            self,
            request: Request,
            skip: int = 0,
            limit: int = 100,
            where: Union[dict[str, Any], str, None] = None,
            order_by: Optional[list[str]] = None,
    ) -> Sequence[read_schemas.VariableRead]:
        list_variables = functools.partial(
            db.list_variables,
            limit=limit,
            offset=skip,
            include_total=False,
        )
        db_vars, _ = await anyio.to_thread.run_sync(
            list_variables, request.state.session)
        return [self._serialize_instance(db_var) for db_var in db_vars]


class StationView(ModelView):
    identity = "stations"
    name = "Station"
    label = "Stations"
    icon = "fa fa-blog"
    pk_attr = "id"

    exclude_fields_from_list = ("id",)
    exclude_fields_from_detail = ("id",)

    fields = (
        fields.UuidField("id"),
        starlette_admin.StringField("name", required=True),
        starlette_admin.StringField("code", required=True),
        starlette_admin.StringField("type", required=True),
        starlette_admin.FloatField("longitude", required=True),
        starlette_admin.FloatField("latitude", required=True),
        starlette_admin.DateField("active_since"),
        starlette_admin.DateField("active_until"),
        starlette_admin.FloatField("altitude_m"),
    )

    @staticmethod
    def _serialize_instance(
            instance: observations.Station) -> read_schemas.StationRead:
        geom = shapely.io.from_wkb(instance.geom.data)
        return read_schemas.StationRead(
            **instance.model_dump(exclude={"geom"}),
            longitude=geom.x,
            latitude=geom.y,
        )

    async def get_pk_value(self, request: Request, obj: Any) -> str:
        # note: we need to cast the value, which is a uuid.UUID, to a string
        # because starlette_admin just assumes that the value of a model's
        # pk attribute is always JSON serializable so it doesn't bother with
        # calling the respective field's `serialize_value()` method
        result = await super().get_pk_value(request, obj)
        return str(result)

    async def create(
            self, request: Request, data: dict[str, Any]
    ) -> Optional[read_schemas.StationRead]:
        try:
            data = await self._arrange_data(request, data)
            await self.validate(request, data)
            geojson_geom = geojson_pydantic.Point(
                type="Point",
                coordinates=(data.pop("longitude"), data.pop("latitude"))
            )
            station_create = observations.StationCreate(
                type_=data.pop("type"),
                geom=geojson_geom,
                **data,
            )
            db_station = await anyio.to_thread.run_sync(
                db.create_station,
                request.state.session,
                station_create,
            )
            return self._serialize_instance(db_station)
        except Exception as e:
            return self.handle_exception(e)

    async def edit(
            self, request: Request, pk: Any, data: dict[str, Any]
    ) -> Optional[read_schemas.StationRead]:
        try:
            data = await self._arrange_data(request, data, True)
            await self.validate(request, data)
            lon = data.pop("longitude", None)
            lat = data.pop("latitude", None)
            kwargs = {}
            if all((lon, lat)):
                kwargs["geom"] = geojson_pydantic.Point(
                    type="Point",
                    coordinates=(lon, lat)
                )
            if (type_ := data.pop("type", None)) is not None:
                kwargs["type_"] = type_
            station_update = observations.StationUpdate(
                **data,
                **kwargs
            )
            db_station = await anyio.to_thread.run_sync(
                db.get_station, request.state.session, pk
            )
            db_station = await anyio.to_thread.run_sync(
                db.update_station, request.state.session, db_station, station_update)
            return self._serialize_instance(db_station)
        except Exception as e:
            logger.exception("something went wrong")
            self.handle_exception(e)

    async def find_by_pk(
            self, request: Request, pk: Any
    ) -> read_schemas.StationRead:
        db_station = await anyio.to_thread.run_sync(
            db.get_station, request.state.session, pk)
        return self._serialize_instance(db_station)

    async def find_all(
            self,
            request: Request,
            skip: int = 0,
            limit: int = 100,
            where: Union[dict[str, Any], str, None] = None,
            order_by: Optional[list[str]] = None,
    ) -> Sequence[read_schemas.StationRead]:
        list_stations = functools.partial(
            db.list_stations,
            limit=limit,
            offset=skip,
            include_total=False,
        )
        db_stations, _ = await anyio.to_thread.run_sync(
            list_stations, request.state.session)
        return [self._serialize_instance(db_station) for db_station in db_stations]
