import geojson_pydantic
import pydantic
from fastapi import Request

from .....schemas import (
    fields,
    municipalities,
)
from .base import ArpavFeatureCollection


class MunicipalityFeatureCollectionItem(geojson_pydantic.Feature):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    type: str = "Feature"
    id: pydantic.UUID4
    geometry: fields.WkbElement

    @classmethod
    def from_db_instance(
        cls,
        instance: municipalities.Municipality,
        request: Request,
    ) -> "MunicipalityFeatureCollectionItem":
        return cls(
            id=instance.id,
            geometry=instance.geom,
            properties={
                **instance.model_dump(
                    exclude={
                        "id",
                        "geom",
                    }
                ),
            },
        )


class MunicipalityFeatureCollection(ArpavFeatureCollection):
    path_operation_name = "list_municipalities"
    list_item_type = MunicipalityFeatureCollectionItem
