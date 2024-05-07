import datetime as dt
import uuid
from typing import Optional

import geojson_pydantic
import geoalchemy2
import pydantic
import sqlalchemy
import sqlmodel

from . import fields


class StationBase(sqlmodel.SQLModel):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    id: pydantic.UUID4 = sqlmodel.Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    geom: fields.WkbElement = sqlmodel.Field(
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
    altitude_m: Optional[float] = sqlmodel.Field(default=None)
    name: str = ""
    type_: str = ""

    monthly_measurements: list["MonthlyMeasurement"] = sqlmodel.Relationship(
        back_populates="station",
        sa_relationship_kwargs={
            # ORM relationship config, which explicitly includes the
            # `delete` and `delete-orphan` options because we want the ORM
            # to try to delete monthly measurements when their related station
            # is deleted
            "cascade": "all, delete-orphan",
            # expect that the RDBMS handles cascading deletes
            "passive_deletes": True
        }
    )


class StationCreate(sqlmodel.SQLModel):
    code: str
    geom: geojson_pydantic.Point
    altitude_m: Optional[float] = None
    name: Optional[str] = ""
    type_: Optional[str] = ""


class StationUpdate(sqlmodel.SQLModel):
    code: Optional[str] = None
    geom: Optional[geojson_pydantic.Point] = None
    altitude_m: Optional[float] = None
    name: Optional[str] = None
    type_: Optional[str] = None


class VariableBase(sqlmodel.SQLModel):
    id: pydantic.UUID4 = sqlmodel.Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    name: str = sqlmodel.Field(unique=True)
    description: str
    unit: str = ""


class Variable(VariableBase, table=True):
    monthly_measurements: list["MonthlyMeasurement"] = sqlmodel.Relationship(
        back_populates="variable",
        sa_relationship_kwargs={
            # ORM relationship config, which explicitly includes the
            # `delete` and `delete-orphan` options because we want the ORM
            # to try to delete monthly measurements when their related variable
            # is deleted
            "cascade": "all, delete-orphan",
            # expect that the RDBMS handles cascading deletes
            "passive_deletes": True
        }
    )


class VariableCreate(sqlmodel.SQLModel):
    name: str
    description: str
    unit: Optional[str] = ""


class VariableUpdate(sqlmodel.SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None


class MonthlyMeasurementBase(sqlmodel.SQLModel):
    value: float
    date: dt.date


class MonthlyMeasurement(MonthlyMeasurementBase, table=True):
    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["station_id",],
            ["station.id",],
            onupdate="CASCADE",
            ondelete="CASCADE",  # i.e. delete a monthly measurement if its related station is deleted
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["variable_id", ],
            ["variable.id", ],
            onupdate="CASCADE",
            ondelete="CASCADE",  # i.e. delete a monthly measurement if its related station is deleted
        ),
    )
    id: pydantic.UUID4 = sqlmodel.Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    station_id: pydantic.UUID4
    variable_id: pydantic.UUID4

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
