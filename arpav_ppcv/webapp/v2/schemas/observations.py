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
        print(f"{url=}")
        print(f"{__name__=}")
        logger.debug(f"{url=}")
        return cls(
            **instance.model_dump(),
            url=str(url),
        )


class VariableReadListItem(app_models.VariableBase):
    ...


class MonthlyMeasurementListItem(app_models.MonthlyMeasurementBase):
    ...


class StationList(WebResourceList):
    items: list[StationReadListItem]
    list_item_type = StationReadListItem
    path_operation_name = "list_stations"


class VariableList(WebResourceList):
    items: list[VariableReadListItem]


class MonthlyMeasurementList(WebResourceList):
    items: list[MonthlyMeasurementListItem]
