"""Database utilities."""

from typing import (
    Optional,
    Sequence,
)

import shapely.geometry
import shapely.io
import sqlalchemy.exc
import sqlmodel
from geoalchemy2.shape import from_shape

from . import config
from .schemas import models


def get_engine(settings: config.ArpavPpcvSettings):
    return sqlmodel.create_engine(
        settings.db_dsn.unicode_string(),
        echo=True if settings.debug else False
    )


def create_station(
        session: sqlmodel.Session,
        station_create: models.StationCreate
) -> models.Station:
    """Create a new station."""
    geom = shapely.io.from_geojson(station_create.geom.model_dump_json())
    wkbelement = from_shape(geom)
    db_station = models.Station(
        geom=wkbelement,
        code=station_create.code
    )
    session.add(db_station)
    try:
        session.commit()
    except sqlalchemy.exc.DBAPIError:
        raise
    else:
        session.refresh(db_station)
        return db_station


def list_stations(
        session: sqlmodel.Session,
        *,
        limit: int = 20,
        offset: int = 0,
        include_total: bool = False,
) -> tuple[Sequence[models.Station], Optional[int]]:
    """List existing stations."""
    statement = sqlmodel.select(models.Station)
    stations = session.exec(statement.offset(offset).limit(limit)).all()
    num_stations = (
        _get_total_num_records(session, statement) if include_total else None)
    return stations, num_stations


def collect_all_stations(
        session: sqlmodel.Session,
) -> Sequence[models.Station]:
    _, num_total = list_stations(session, limit=1, include_total=True)
    result, _ = list_stations(session, limit=num_total, include_total=False)
    return result


def _get_total_num_records(session: sqlmodel.Session, statement):
    return session.exec(
        sqlmodel.select(sqlmodel.func.count()).select_from(statement)
    ).first()
