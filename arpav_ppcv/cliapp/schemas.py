import pydantic

from ..schemas import observations


class StationRead(observations.StationBase):
    ...


class StationCreate(observations.StationCreate):
    ...


class StationUpdate(observations.StationUpdate):
    ...


class VariableRead(observations.VariableBase):
    ...


class VariableCreate(observations.VariableCreate):
    ...


class VariableUpdate(observations.VariableUpdate):
    ...


class MonthlyMeasurementRead(observations.MonthlyMeasurementBase):
    station_id: pydantic.UUID4
    variable_id: pydantic.UUID4


class MonthlyMeasurementCreate(observations.MonthlyMeasurementCreate):
    ...


class MonthlyMeasurementUpdate(observations.MonthlyMeasurementUpdate):
    ...
