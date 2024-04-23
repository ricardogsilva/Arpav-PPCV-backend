import logging
import pydantic
from fastapi import Request

from ....schemas import models as app_models
from .base import WebResourceList

logger = logging.getLogger(__name__)


class StationReadListItem(app_models.StationBase):
    url: pydantic.AnyHttpUrl

    @classmethod
    def from_db_instance(
            cls,
            instance: app_models.Station,
            request: Request,
    ) -> "StationReadListItem":
        url = request.url_for("get_station", **{"station_id": instance.id})
        return cls(
            **instance.model_dump(),
            url=str(url),
        )


class VariableReadListItem(app_models.VariableBase):
    url: pydantic.AnyHttpUrl

    @classmethod
    def from_db_instance(
            cls,
            instance: app_models.Variable,
            request: Request,
    ) -> "VariableReadListItem":
        return cls(
            **instance.model_dump(),
            url=str(request.url_for("get_variable", variable_id=instance.id))
        )


class MonthlyMeasurementReadListItem(app_models.MonthlyMeasurementBase):
    url: pydantic.AnyHttpUrl
    variable_name: str
    station_code: str

    @classmethod
    def from_db_instance(
            cls,
            instance: app_models.MonthlyMeasurement,
            request: Request,
    ) -> "MonthlyMeasurementReadListItem":
        return cls(
            **instance.model_dump(),
            variable_name=instance.variable.name,
            station_code=instance.station.code,
            url=str(
                request.url_for(
                    "get_monthly_measurement", monthly_measurement_id=instance.id)
            )
        )


class StationList(WebResourceList):
    items: list[StationReadListItem]
    list_item_type = StationReadListItem
    path_operation_name = "list_stations"


class VariableList(WebResourceList):
    items: list[VariableReadListItem]
    list_item_type = VariableReadListItem
    path_operation_name = "list_variables"


class MonthlyMeasurementList(WebResourceList):
    items: list[MonthlyMeasurementReadListItem]
    list_item_type = MonthlyMeasurementReadListItem
    path_operation_name = "list_monthly_measurements"
