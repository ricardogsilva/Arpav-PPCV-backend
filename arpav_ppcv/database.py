"""Database utilities."""

import logging
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
from .schemas import (
    coverages,
    models,
)

logger = logging.getLogger(__name__)


def get_engine(
        settings: config.ArpavPpcvSettings,
        use_test_db: Optional[bool] = False
):
    db_dsn = settings.test_db_dsn if use_test_db else settings.db_dsn
    return sqlmodel.create_engine(
        db_dsn.unicode_string(),
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
    statement = sqlmodel.select(models.Variable).order_by(models.Variable.name)
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


def create_many_stations(
        session: sqlmodel.Session,
        stations_to_create: Sequence[models.StationCreate],
) -> list[models.Station]:
    """Create several stations."""
    db_records = []
    for station_create in stations_to_create:
        geom = shapely.io.from_geojson(station_create.geom.model_dump_json())
        wkbelement = from_shape(geom)
        db_station = models.Station(
            code=station_create.code,
            geom=wkbelement,
            altitude_m=station_create.altitude_m,
            name=station_create.name,
            type_=station_create.type_,
        )
        db_records.append(db_station)
        session.add(db_station)
    try:
        session.commit()
    except sqlalchemy.exc.DBAPIError:
        raise
    else:
        for db_record in db_records:
            session.refresh(db_record)
        return db_records


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
    statement = sqlmodel.select(models.Station).order_by(models.Station.code)
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


def create_many_monthly_measurements(
        session: sqlmodel.Session,
        monthly_measurements_to_create: Sequence[models.MonthlyMeasurementCreate],
) -> list[models.MonthlyMeasurement]:
    """Create several monthly measurements."""
    db_records = []
    for monthly_measurement_create in monthly_measurements_to_create:
        db_monthly_measurement = models.MonthlyMeasurement(
            station_id=monthly_measurement_create.station_id,
            variable_id=monthly_measurement_create.variable_id,
            value=monthly_measurement_create.value,
            date=monthly_measurement_create.date,
        )
        db_records.append(db_monthly_measurement)
        session.add(db_monthly_measurement)
    try:
        session.commit()
    except sqlalchemy.exc.DBAPIError:
        raise
    else:
        for db_record in db_records:
            session.refresh(db_record)
        return db_records


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
        station_id_filter: Optional[uuid.UUID] = None,
        variable_id_filter: Optional[uuid.UUID] = None,
        month_filter: Optional[int] = None,
        include_total: bool = False,
) -> tuple[Sequence[models.MonthlyMeasurement], Optional[int]]:
    """List existing monthly measurements."""
    statement = sqlmodel.select(models.MonthlyMeasurement).order_by(
        models.MonthlyMeasurement.date)
    if station_id_filter is not None:
        statement = statement.where(
            models.MonthlyMeasurement.station_id == station_id_filter)
    if variable_id_filter is not None:
        statement = statement.where(
            models.MonthlyMeasurement.variable_id == variable_id_filter)
    if month_filter is not None:
        statement = statement.where(
            sqlmodel.func.extract(
                "MONTH", models.MonthlyMeasurement.date) == month_filter)
    items = session.exec(statement.offset(offset).limit(limit)).all()
    num_items = (
        _get_total_num_records(session, statement) if include_total else None)
    return items, num_items


def collect_all_monthly_measurements(
        session: sqlmodel.Session,
        *,
        station_id_filter: Optional[uuid.UUID] = None,
        variable_id_filter: Optional[uuid.UUID] = None,
        month_filter: Optional[int] = None,
) -> Sequence[models.MonthlyMeasurement]:
    _, num_total = list_monthly_measurements(
        session,
        limit=1,
        station_id_filter=station_id_filter,
        variable_id_filter=variable_id_filter,
        month_filter=month_filter,
        include_total=True
    )
    result, _ = list_monthly_measurements(
        session,
        limit=num_total,
        station_id_filter=station_id_filter,
        variable_id_filter=variable_id_filter,
        month_filter=month_filter,
        include_total=False
    )
    return result


def get_configuration_parameter_value(
        session: sqlmodel.Session,
        configuration_parameter_value_id: uuid.UUID
) -> Optional[coverages.ConfigurationParameterValue]:
    return session.get(
        coverages.ConfigurationParameterValue, configuration_parameter_value_id)


def get_configuration_parameter(
        session: sqlmodel.Session,
        configuration_parameter_id: uuid.UUID
) -> Optional[coverages.ConfigurationParameter]:
    return session.get(coverages.ConfigurationParameter, configuration_parameter_id)


def get_configuration_parameter_by_name(
        session: sqlmodel.Session,
        configuration_parameter_name: str
) -> Optional[coverages.ConfigurationParameter]:
    """Get a configuration parameter by its name.

    Since a configuration parameter's name is unique, it can be used to uniquely
    identify it.
    """
    return session.exec(
        sqlmodel.select(coverages.ConfigurationParameter)
        .where(coverages.ConfigurationParameter.name == configuration_parameter_name)
    ).first()


def list_configuration_parameters(
        session: sqlmodel.Session,
        *,
        limit: int = 20,
        offset: int = 0,
        include_total: bool = False,
) -> tuple[Sequence[coverages.ConfigurationParameter], Optional[int]]:
    """List existing configuration parameters."""
    statement = sqlmodel.select(coverages.ConfigurationParameter).order_by(
        coverages.ConfigurationParameter.name)
    items = session.exec(statement.offset(offset).limit(limit)).all()
    num_items = (
        _get_total_num_records(session, statement) if include_total else None)
    return items, num_items


def collect_all_configuration_parameters(
        session: sqlmodel.Session,
) -> Sequence[coverages.ConfigurationParameter]:
    _, num_total = list_configuration_parameters(session, limit=1, include_total=True)
    result, _ = list_configuration_parameters(
        session, limit=num_total, include_total=False)
    return result


def create_configuration_parameter(
        session: sqlmodel.Session,
        configuration_parameter_create: coverages.ConfigurationParameterCreate
) -> coverages.ConfigurationParameter:
    logger.debug(f"inside database.create_configuration_parameter - {locals()=}")
    to_refresh = []
    db_configuration_parameter = coverages.ConfigurationParameter(
        name=configuration_parameter_create.name,
        description=configuration_parameter_create.description
    )
    to_refresh.append(db_configuration_parameter)
    for allowed in configuration_parameter_create.allowed_values:
        db_conf_param_value = coverages.ConfigurationParameterValue(
            name=allowed.name,
            description=allowed.description,
        )
        db_configuration_parameter.allowed_values.append(db_conf_param_value)
        to_refresh.append(db_conf_param_value)
    session.add(db_configuration_parameter)
    session.commit()
    for item in to_refresh:
        session.refresh(item)
    return db_configuration_parameter


def update_configuration_parameter(
        session: sqlmodel.Session,
        db_configuration_parameter: coverages.ConfigurationParameter,
        configuration_parameter_update: coverages.ConfigurationParameterUpdate
) -> coverages.ConfigurationParameter:
    """Update a configuration parameter."""
    to_refresh = []
    # account for allowed values being: added/modified/deleted
    for existing_allowed_value in db_configuration_parameter.allowed_values:
        has_been_requested_to_remove = (
                existing_allowed_value.id not in
                [i.id for i in configuration_parameter_update.allowed_values]
        )
        if has_been_requested_to_remove:
            session.delete(existing_allowed_value)
    for av in configuration_parameter_update.allowed_values:
        if av.id is None:
            # this is a new allowed value, need to create it
            db_allowed_value = coverages.ConfigurationParameterValue(
                name=av.name,
                description=av.description,
            )
            db_configuration_parameter.allowed_values.append(db_allowed_value)
        else:
            # this is an existing allowed value, lets update
            db_allowed_value = get_configuration_parameter_value(session, av.id)
            for prop, value in av.model_dump(exclude_none=True, exclude_unset=True).items():
                setattr(db_allowed_value, prop, value)
        session.add(db_allowed_value)
        to_refresh.append(db_allowed_value)
    data_ = configuration_parameter_update.model_dump(
        exclude={"allowed_values"}, exclude_unset=True, exclude_none=True)
    for key, value in data_.items():
        setattr(db_configuration_parameter, key, value)
    session.add(db_configuration_parameter)
    to_refresh.append(db_configuration_parameter)
    session.commit()
    for item in to_refresh:
        session.refresh(item)
    return db_configuration_parameter


def _get_total_num_records(session: sqlmodel.Session, statement):
    return session.exec(
        sqlmodel.select(sqlmodel.func.count()).select_from(statement)
    ).first()
