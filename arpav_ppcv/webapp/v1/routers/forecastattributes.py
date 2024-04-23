from fastapi import APIRouter

from .. import schemas
from ..util import get_item_list

router = APIRouter()


@router.get(
    "/variables",
    response_model=schemas.ItemList[schemas.VariableListItem]
)
def get_variables():
    return get_item_list(
        "padoa.forecastattributes.models.Variable",
        schemas.VariableListItem
    )


@router.get(
    "/forecast-models",
    response_model=schemas.ItemList[schemas.ForecastModelListItem])
def get_forecast_models():
    return get_item_list(
        "padoa.forecastattributes.models.ForecastModel",
        schemas.ForecastModelListItem
    )


@router.get(
    "/scenarios",
    response_model=schemas.ItemList[schemas.ScenarioListItem])
def get_scenarios():
    return get_item_list(
        "padoa.forecastattributes.models.Scenario",
        schemas.ScenarioListItem
    )


@router.get(
    "/data-series",
    response_model=schemas.ItemList[schemas.DataSeriesListItem])
def get_data_series():
    return get_item_list(
        "padoa.forecastattributes.models.DataSeries",
        schemas.DataSeriesListItem
    )


@router.get(
    "/year-periods",
    response_model=schemas.ItemList[schemas.YearPeriodListItem])
def get_year_periods():
    return get_item_list(
        "padoa.forecastattributes.models.YearPeriod",
        schemas.YearPeriodListItem
    )


@router.get(
    "/time-windows",
    response_model=schemas.ItemList[schemas.TimeWindowListItem])
def get_time_windows():
    return get_item_list(
        "padoa.forecastattributes.models.TimeWindow",
        schemas.TimeWindowListItem
    )


@router.get(
    "/value-types",
    response_model=schemas.ItemList[schemas.ValueTypeListItem])
def get_time_windows():
    return get_item_list(
        "padoa.forecastattributes.models.ValueType",
        schemas.ValueTypeListItem
    )
