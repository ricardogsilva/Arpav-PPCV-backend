import datetime as dt
from typing import Optional

import geojson_pydantic
import pydantic
import sqlmodel

from ..schemas import models as app_models


class StationRead(app_models.StationBase):
    ...


class StationCreate(app_models.StationCreate):
    ...


class StationUpdate(app_models.StationUpdate):
    ...


class VariableRead(app_models.VariableBase):
    ...


class VariableCreate(app_models.VariableCreate):
    ...


class VariableUpdate(app_models.VariableUpdate):
    ...


class MonthlyMeasurementRead(app_models.MonthlyMeasurementBase):
    station_id: pydantic.UUID4
    variable_id: pydantic.UUID4


class MonthlyMeasurementCreate(app_models.MonthlyMeasurementCreate):
    ...


class MonthlyMeasurementUpdate(app_models.MonthlyMeasurementUpdate):
    ...
