import datetime as dt
from typing import Optional

import geojson_pydantic
import pydantic
import sqlmodel

from ..schemas import models as app_models


class StationRead(app_models.StationBase):
    ...


class StationCreate(sqlmodel.SQLModel):
    geom: geojson_pydantic.Point
    code: str


class StationUpdate(sqlmodel.SQLModel):
    geom: Optional[geojson_pydantic.Point] = None
    code: Optional[str] = None


class VariableRead(app_models.VariableBase):
    ...


class VariableCreate(sqlmodel.SQLModel):
    name: str
    unit: str


class VariableUpdate(sqlmodel.SQLModel):
    name: Optional[str] = None
    unit: Optional[str] = None


class MonthlyMeasurementRead(app_models.MonthlyMeasurementBase):
    station_id: pydantic.UUID4
    variable_id: pydantic.UUID4


class MonthlyMeasurementCreate(sqlmodel.SQLModel):
    station_id: pydantic.UUID4
    variable_id: pydantic.UUID4
    value: float
    date: dt.date


class MonthlyMeasurementUpdate(sqlmodel.SQLModel):
    value: Optional[float] = None
    date: Optional[dt.date] = None
