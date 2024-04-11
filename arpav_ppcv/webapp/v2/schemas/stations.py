import pydantic

from ....schemas import models as app_models
from .base import ResourceList


class StationReadListItem(app_models.StationBase):
    ...


class StationList(ResourceList):
    items: list[StationReadListItem]
