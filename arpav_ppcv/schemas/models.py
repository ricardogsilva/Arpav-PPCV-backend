import uuid

import geoalchemy2
import geojson_pydantic
import pydantic
import sqlalchemy
import sqlmodel


class Station(sqlmodel.SQLModel, table=True):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    id: pydantic.UUID4 = sqlmodel.Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    geom: geoalchemy2.WKBElement = sqlmodel.Field(
        sa_column=sqlalchemy.Column(
            geoalchemy2.Geometry(
                srid=4326,
                geometry_type="POLYGON",
                spatial_index=True,
            )
        )
    )
    code: str = sqlmodel.Field(unique=True)
    monthly_measurements: list["MonthlyMeasurement"] = sqlmodel.Relationship(
        back_populates="station")


class StationCreate(sqlmodel.SQLModel):
    geom: geojson_pydantic.Point
    code: str


class Variable(sqlmodel.SQLModel, table=True):
    id: pydantic.UUID4 = sqlmodel.Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    name: str
    unit: str

    monthly_measurements: list["MonthlyMeasurement"] = sqlmodel.Relationship(
        back_populates="variable"
    )


class MonthlyMeasurement(sqlmodel.SQLModel, table=True):
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
