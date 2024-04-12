import datetime as dt
import json
import uuid
from typing import (
    Annotated,
    Optional,
)

import geojson_pydantic
import geoalchemy2
import pydantic
import sqlalchemy
import shapely.io
import sqlmodel
from pydantic.functional_serializers import PlainSerializer


def serialize_wkbelement(wkbelement: geoalchemy2.WKBElement):
    geom = shapely.io.from_wkb(bytes(wkbelement.data))
    return json.loads(shapely.io.to_geojson(geom))


WkbElement = Annotated[
    geoalchemy2.WKBElement,
    PlainSerializer(serialize_wkbelement, return_type=dict, when_used="json")
]


class StationBase(sqlmodel.SQLModel):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    id: pydantic.UUID4 = sqlmodel.Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    geom: WkbElement = sqlmodel.Field(
        sa_column=sqlalchemy.Column(
            geoalchemy2.Geometry(
                srid=4326,
                geometry_type="POINT",
                spatial_index=True,
            )
        )
    )
    code: str = sqlmodel.Field(unique=True)


class Station(StationBase, table=True):

    monthly_measurements: list["MonthlyMeasurement"] = sqlmodel.Relationship(
        back_populates="station")


class StationCreate(sqlmodel.SQLModel):
    geom: geojson_pydantic.Point
    code: str


class StationUpdate(sqlmodel.SQLModel):
    geom: Optional[geojson_pydantic.Point] = None
    code: Optional[str] = None


class VariableBase(sqlmodel.SQLModel):
    id: pydantic.UUID4 = sqlmodel.Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    name: str = sqlmodel.Field(unique=True)
    unit: str


class Variable(VariableBase, table=True):

    monthly_measurements: list["MonthlyMeasurement"] = sqlmodel.Relationship(
        back_populates="variable"
    )


class VariableCreate(sqlmodel.SQLModel):
    name: str
    unit: str


class VariableUpdate(sqlmodel.SQLModel):
    name: Optional[str] = None
    unit: Optional[str] = None


class MonthlyMeasurementBase(sqlmodel.SQLModel):
    value: float
    date: dt.date


class MonthlyMeasurement(MonthlyMeasurementBase, table=True):
    id: pydantic.UUID4 = sqlmodel.Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    station_id: pydantic.UUID4 = sqlmodel.Field(
        foreign_key="station.id"
    )
    variable_id: pydantic.UUID4 = sqlmodel.Field(
        foreign_key="variable.id"
    )
    station: Station = sqlmodel.Relationship(
        back_populates="monthly_measurements",
        sa_relationship_kwargs={
            # retrieve the related resource immediately, by means of a SQL JOIN - this
            # is instead of the default lazy behavior of only retrieving related
            # records when they are accessed by the ORM
            "lazy": "joined",
        }
    )
    variable: Variable = sqlmodel.Relationship(
        back_populates="monthly_measurements",
        sa_relationship_kwargs={
            # retrieve the related resource immediately, by means of a SQL JOIN - this
            # is instead of the default lazy behavior of only retrieving related
            # records when they are accessed by the ORM
            "lazy": "joined",
        }
    )


class MonthlyMeasurementCreate(sqlmodel.SQLModel):
    station_id: pydantic.UUID4
    variable_id: pydantic.UUID4
    value: float
    date: dt.date


class MonthlyMeasurementUpdate(sqlmodel.SQLModel):
    value: Optional[float] = None
    date: Optional[dt.date] = None
