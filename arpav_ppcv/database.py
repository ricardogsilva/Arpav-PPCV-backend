"""Database utilities."""

import uuid
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
        echo=True if settings.verbose_db_logs else False
    )


def create_variable(
        session: sqlmodel.Session,
        variable_create: models.VariableCreate
) -> models.Variable:
    """Create a new variable."""
    db_variable = models.Variable(**variable_create.model_dump())
    session.add(db_variable)
    try:
        session.commit()
    except sqlalchemy.exc.DBAPIError:
        raise
    else:
        session.refresh(db_variable)
        return db_variable


def create_many_variables(
        session: sqlmodel.Session,
        variables_to_create: Sequence[models.VariableCreate],
) -> list[models.Variable]:
    """Create several variables."""
    db_records = []
    for variable_create in variables_to_create:
        db_variable = models.Variable(**variable_create.model_dump())
        db_records.append(db_variable)
        session.add(db_variable)
    try:
        session.commit()
    except sqlalchemy.exc.DBAPIError:
        raise
    else:
        for db_record in db_records:
            session.refresh(db_record)
        return db_records


def get_variable(
        session: sqlmodel.Session, variable_id: uuid.UUID) -> Optional[models.Variable]:
    return session.get(models.Variable, variable_id)


def get_variable_by_name(
        session: sqlmodel.Session, variable_name: str) -> Optional[models.Variable]:
    """Get a variable by its name.

    Since a variable name is unique, it can be used to uniquely identify a variable.
    """
    return session.exec(
        sqlmodel.select(models.Variable).where(models.Variable.name == variable_name)
    ).first()


def update_variable(
        session: sqlmodel.Session,
        db_variable: models.Variable,
        variable_update: models.VariableUpdate
) -> models.Variable:
    """Update a variable."""
    data_ = variable_update.model_dump(exclude_unset=True)
    for key, value in data_.items():
        setattr(db_variable, key, value)
    session.add(db_variable)
    session.commit()
    session.refresh(db_variable)
    return db_variable


def delete_variable(session: sqlmodel.Session, variable_id: uuid.UUID) -> None:
    """Delete a variable."""
    db_variable = get_variable(session, variable_id)
    if db_variable is not None:
        session.delete(db_variable)
        session.commit()
    else:
        raise RuntimeError("Variable not found")


def list_variables(
        session: sqlmodel.Session,
        *,
        limit: int = 20,
        offset: int = 0,
        include_total: bool = False,
) -> tuple[Sequence[models.Variable], Optional[int]]:
    """List existing variables."""
    statement = sqlmodel.select(models.Variable)
    items = session.exec(statement.offset(offset).limit(limit)).all()
    num_items = (
        _get_total_num_records(session, statement) if include_total else None)
    return items, num_items


def collect_all_variables(
        session: sqlmodel.Session,
) -> Sequence[models.Variable]:
    _, num_total = list_variables(session, limit=1, include_total=True)
    result, _ = list_variables(session, limit=num_total, include_total=False)
    return result


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


def get_station(
        session: sqlmodel.Session, station_id: uuid.UUID) -> Optional[models.Station]:
    return session.get(models.Station, station_id)


def get_station_by_code(
        session: sqlmodel.Session, station_code: str) -> Optional[models.Station]:
    """Get a station by its code.

    Since a station code is unique, it can be used to uniquely identify a station.
    """
    return session.exec(
        sqlmodel.select(models.Station).where(models.Station.code == station_code)
    ).first()


def update_station(
        session: sqlmodel.Session,
        db_station: models.Station,
        station_update: models.StationUpdate
) -> models.Station:
    """Update a station."""
    data_ = station_update.model_dump(exclude_unset=True)
    for key, value in data_.items():
        setattr(db_station, key, value)
    session.add(db_station)
    session.commit()
    session.refresh(db_station)
    return db_station


def delete_station(session: sqlmodel.Session, station_id: uuid.UUID) -> None:
    """Delete a station."""
    db_station = get_station(session, station_id)
    if db_station is not None:
        session.delete(db_station)
        session.commit()
    else:
        raise RuntimeError("Station not found")


def list_stations(
        session: sqlmodel.Session,
        *,
        limit: int = 20,
        offset: int = 0,
        include_total: bool = False,
) -> tuple[Sequence[models.Station], Optional[int]]:
    """List existing stations."""
    statement = sqlmodel.select(models.Station)
    items = session.exec(statement.offset(offset).limit(limit)).all()
    num_items = (
        _get_total_num_records(session, statement) if include_total else None)
    return items, num_items


def collect_all_stations(
        session: sqlmodel.Session,
) -> Sequence[models.Station]:
    _, num_total = list_stations(session, limit=1, include_total=True)
    result, _ = list_stations(session, limit=num_total, include_total=False)
    return result


def create_monthly_measurement(
        session: sqlmodel.Session,
        monthly_measurement_create: models.MonthlyMeasurementCreate
) -> models.MonthlyMeasurement:
    """Create a new monthly measurement."""
    db_monthly_measurement = models.MonthlyMeasurement(
        **monthly_measurement_create.model_dump())
    session.add(db_monthly_measurement)
    try:
        session.commit()
    except sqlalchemy.exc.DBAPIError:
        raise
    else:
        session.refresh(db_monthly_measurement)
        return db_monthly_measurement


def get_monthly_measurement(
        session: sqlmodel.Session,
        monthly_measurement_id: uuid.UUID
) -> Optional[models.MonthlyMeasurement]:
    return session.get(models.MonthlyMeasurement, monthly_measurement_id)


def delete_monthly_measurement(
        session: sqlmodel.Session, monthly_measurement_id: uuid.UUID) -> None:
    """Delete a monthly_measurement."""
    db_monthly_measurement = get_monthly_measurement(session, monthly_measurement_id)
    if db_monthly_measurement is not None:
        session.delete(db_monthly_measurement)
        session.commit()
    else:
        raise RuntimeError("Monthly measurement not found")


def list_monthly_measurements(
        session: sqlmodel.Session,
        *,
        limit: int = 20,
        offset: int = 0,
        include_total: bool = False,
) -> tuple[Sequence[models.MonthlyMeasurement], Optional[int]]:
    """List existing monthly measurements."""
    statement = sqlmodel.select(models.MonthlyMeasurement)
    items = session.exec(statement.offset(offset).limit(limit)).all()
    num_items = (
        _get_total_num_records(session, statement) if include_total else None)
    return items, num_items


def collect_all_monthly_measurements(
        session: sqlmodel.Session,
) -> Sequence[models.MonthlyMeasurement]:
    _, num_total = list_monthly_measurements(session, limit=1, include_total=True)
    result, _ = list_monthly_measurements(session, limit=num_total, include_total=False)
    return result


def _get_total_num_records(session: sqlmodel.Session, statement):
    return session.exec(
        sqlmodel.select(sqlmodel.func.count()).select_from(statement)
    ).first()
