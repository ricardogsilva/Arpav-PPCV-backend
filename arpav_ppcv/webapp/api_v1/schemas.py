"""A reimplementation of the schemas used by the legacy django app, which
is based on django-rest-framework.
"""

import datetime as dt
from typing import (
    Generic,
    TypeVar,
)

import pydantic

ItemType = TypeVar("ItemType")


class BaseConfigParameterListItem(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes=True
    )

    id: str
    name: str
    description: str
    order_item: int


class VariableListItem(BaseConfigParameterListItem):
    ...


class ForecastModelListItem(BaseConfigParameterListItem):
    ...


class ScenarioListItem(BaseConfigParameterListItem):
    ...


class DataSeriesListItem(BaseConfigParameterListItem):
    ...


class YearPeriodListItem(BaseConfigParameterListItem):
    ...


class TimeWindowListItem(BaseConfigParameterListItem):
    ...


class ValueTypeListItem(BaseConfigParameterListItem):
    ...


class MapListItem(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes=True
    )

    variable_id: str
    forecast_model_id: str
    scenario_id: str
    data_series_id: str
    year_period_id: str
    time_window_id: str
    value_type_id: str
    time_start: dt.datetime
    time_end: dt.datetime
    time_interval: str
    csr: str
    layer_id: str
    path: str
    palette: str
    unit: str
    color_scale_min: int
    color_scale_max: int
    bbox: tuple[tuple[float, float], tuple[float, float]]
    elevation: int
    legend: dict[str, str]


class UserDownloadListItem(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes=True
    )

    reason: str | None = None
    place: str | None = None
    membership: str | None = None
    public: bool = False
    accept_disclaimer: bool = False
    date: dt.date | None = None
    parameters: str | None = None


class DatasetEmbeddedInTimeSeries(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes=True
    )

    lat: float
    lng: float
    dataset: str
    layer: str


class TimeSeriesCreate(pydantic.BaseModel):
    map_ids: list[str]
    latitude: float | None = None
    longitude: float | None = None


class TimeSeriesListItem(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes=True
    )

    dataset: DatasetEmbeddedInTimeSeries
    values: dict


class DatasetReadIn(pydantic.BaseModel):
    map_id: str
    time_start: dt.datetime
    time_end: dt.datetime
    north: float | None = None
    west: float | None = None
    east: float | None = None
    south: float | None = None


class CityLocation(pydantic.BaseModel):
    lng: float
    lat: float


class CityListItem(pydantic.BaseModel):
    id: int
    name: str
    latlng: CityLocation


class ItemList(pydantic.BaseModel, Generic[ItemType]):
    count: int
    next: str | None = None
    previous: str | None = None
    results: list[ItemType]
