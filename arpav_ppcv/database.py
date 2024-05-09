"""Database utilities."""

import itertools
import logging
import re
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
    observations,
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
        variable_create: observations.VariableCreate
) -> observations.Variable:
    """Create a new variable."""
    db_variable = observations.Variable(**variable_create.model_dump())
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
        variables_to_create: Sequence[observations.VariableCreate],
) -> list[observations.Variable]:
    """Create several variables."""
    db_records = []
    for variable_create in variables_to_create:
        db_variable = observations.Variable(**variable_create.model_dump())
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
        session: sqlmodel.Session, variable_id: uuid.UUID
) -> Optional[observations.Variable]:
    return session.get(observations.Variable, variable_id)


def get_variable_by_name(
        session: sqlmodel.Session,
        variable_name: str
) -> Optional[observations.Variable]:
    """Get a variable by its name.

    Since a variable name is unique, it can be used to uniquely identify a variable.
    """
    return session.exec(
        sqlmodel.select(observations.Variable)
        .where(observations.Variable.name == variable_name)
    ).first()


def update_variable(
        session: sqlmodel.Session,
        db_variable: observations.Variable,
        variable_update: observations.VariableUpdate
) -> observations.Variable:
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
) -> tuple[Sequence[observations.Variable], Optional[int]]:
    """List existing variables."""
    statement = (
        sqlmodel.select(observations.Variable)
        .order_by(observations.Variable.name)
    )
    items = session.exec(statement.offset(offset).limit(limit)).all()
    num_items = (
        _get_total_num_records(session, statement) if include_total else None)
    return items, num_items


def collect_all_variables(
        session: sqlmodel.Session,
) -> Sequence[observations.Variable]:
    _, num_total = list_variables(session, limit=1, include_total=True)
    result, _ = list_variables(session, limit=num_total, include_total=False)
    return result


def create_station(
        session: sqlmodel.Session,
        station_create: observations.StationCreate
) -> observations.Station:
    """Create a new station."""
    geom = shapely.io.from_geojson(station_create.geom.model_dump_json())
    wkbelement = from_shape(geom)
    db_station = observations.Station(
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
        stations_to_create: Sequence[observations.StationCreate],
) -> list[observations.Station]:
    """Create several stations."""
    db_records = []
    for station_create in stations_to_create:
        geom = shapely.io.from_geojson(station_create.geom.model_dump_json())
        wkbelement = from_shape(geom)
        db_station = observations.Station(
            **station_create.model_dump(exclude={"geom"}),
            geom=wkbelement,
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
        session: sqlmodel.Session,
        station_id: uuid.UUID
) -> Optional[observations.Station]:
    return session.get(observations.Station, station_id)


def get_station_by_code(
        session: sqlmodel.Session,
        station_code: str
) -> Optional[observations.Station]:
    """Get a station by its code.

    Since a station code is unique, it can be used to uniquely identify a station.
    """
    return session.exec(
        sqlmodel.select(observations.Station)
        .where(observations.Station.code == station_code)
    ).first()


def update_station(
        session: sqlmodel.Session,
        db_station: observations.Station,
        station_update: observations.StationUpdate
) -> observations.Station:
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
) -> tuple[Sequence[observations.Station], Optional[int]]:
    """List existing stations."""
    statement = (
        sqlmodel.select(observations.Station)
        .order_by(observations.Station.code)
    )
    items = session.exec(statement.offset(offset).limit(limit)).all()
    num_items = (
        _get_total_num_records(session, statement) if include_total else None)
    return items, num_items


def collect_all_stations(
        session: sqlmodel.Session,
) -> Sequence[observations.Station]:
    _, num_total = list_stations(session, limit=1, include_total=True)
    result, _ = list_stations(session, limit=num_total, include_total=False)
    return result


def create_monthly_measurement(
        session: sqlmodel.Session,
        monthly_measurement_create: observations.MonthlyMeasurementCreate
) -> observations.MonthlyMeasurement:
    """Create a new monthly measurement."""
    db_monthly_measurement = observations.MonthlyMeasurement(
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
        monthly_measurements_to_create: Sequence[observations.MonthlyMeasurementCreate],
) -> list[observations.MonthlyMeasurement]:
    """Create several monthly measurements."""
    db_records = []
    for monthly_measurement_create in monthly_measurements_to_create:
        db_monthly_measurement = observations.MonthlyMeasurement(
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
) -> Optional[observations.MonthlyMeasurement]:
    return session.get(observations.MonthlyMeasurement, monthly_measurement_id)


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
) -> tuple[Sequence[observations.MonthlyMeasurement], Optional[int]]:
    """List existing monthly measurements."""
    statement = sqlmodel.select(observations.MonthlyMeasurement).order_by(
        observations.MonthlyMeasurement.date)
    if station_id_filter is not None:
        statement = statement.where(
            observations.MonthlyMeasurement.station_id == station_id_filter)
    if variable_id_filter is not None:
        statement = statement.where(
            observations.MonthlyMeasurement.variable_id == variable_id_filter)
    if month_filter is not None:
        statement = statement.where(
            sqlmodel.func.extract(
                "MONTH", observations.MonthlyMeasurement.date) == month_filter)
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
) -> Sequence[observations.MonthlyMeasurement]:
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


def create_seasonal_measurement(
        session: sqlmodel.Session,
        measurement_create: observations.SeasonalMeasurementCreate
) -> observations.SeasonalMeasurement:
    """Create a new seasonal measurement."""
    db_measurement = observations.SeasonalMeasurement(
        **measurement_create.model_dump())
    session.add(db_measurement)
    try:
        session.commit()
    except sqlalchemy.exc.DBAPIError:
        raise
    else:
        session.refresh(db_measurement)
        return db_measurement


def create_many_seasonal_measurements(
        session: sqlmodel.Session,
        measurements_to_create: Sequence[observations.SeasonalMeasurementCreate],
) -> list[observations.SeasonalMeasurement]:
    """Create several seasonal measurements."""
    db_records = []
    for measurement_create in measurements_to_create:
        db_measurement = observations.SeasonalMeasurement(
            **measurement_create.model_dump())
        db_records.append(db_measurement)
        session.add(db_measurement)
    try:
        session.commit()
    except sqlalchemy.exc.DBAPIError:
        raise
    else:
        for db_record in db_records:
            session.refresh(db_record)
        return db_records


def get_seasonal_measurement(
        session: sqlmodel.Session,
        measurement_id: uuid.UUID
) -> Optional[observations.SeasonalMeasurement]:
    return session.get(observations.SeasonalMeasurement, measurement_id)


def delete_seasonal_measurement(
        session: sqlmodel.Session, measurement_id: uuid.UUID) -> None:
    """Delete a seasonal measurement."""
    db_measurement = get_seasonal_measurement(session, measurement_id)
    if db_measurement is not None:
        session.delete(db_measurement)
        session.commit()
    else:
        raise RuntimeError("Seasonal measurement not found")


def list_seasonal_measurements(
        session: sqlmodel.Session,
        *,
        limit: int = 20,
        offset: int = 0,
        station_id_filter: Optional[uuid.UUID] = None,
        variable_id_filter: Optional[uuid.UUID] = None,
        season_filter: Optional[observations.Season] = None,
        include_total: bool = False,
) -> tuple[Sequence[observations.SeasonalMeasurement], Optional[int]]:
    """List existing seasonal measurements."""
    statement = sqlmodel.select(observations.SeasonalMeasurement).order_by(
        observations.SeasonalMeasurement.year)
    if station_id_filter is not None:
        statement = statement.where(
            observations.SeasonalMeasurement.station_id == station_id_filter)
    if variable_id_filter is not None:
        statement = statement.where(
            observations.SeasonalMeasurement.variable_id == variable_id_filter)
    if season_filter is not None:
        statement = statement.where(
            observations.SeasonalMeasurement.season == season_filter)
    items = session.exec(statement.offset(offset).limit(limit)).all()
    num_items = (
        _get_total_num_records(session, statement) if include_total else None)
    return items, num_items


def collect_all_seasonal_measurements(
        session: sqlmodel.Session,
        *,
        station_id_filter: Optional[uuid.UUID] = None,
        variable_id_filter: Optional[uuid.UUID] = None,
        season_filter: Optional[observations.Season] = None,
) -> Sequence[observations.SeasonalMeasurement]:
    _, num_total = list_seasonal_measurements(
        session,
        limit=1,
        station_id_filter=station_id_filter,
        variable_id_filter=variable_id_filter,
        season_filter=season_filter,
        include_total=True
    )
    result, _ = list_seasonal_measurements(
        session,
        limit=num_total,
        station_id_filter=station_id_filter,
        variable_id_filter=variable_id_filter,
        season_filter=season_filter,
        include_total=False
    )
    return result


def create_yearly_measurement(
        session: sqlmodel.Session,
        measurement_create: observations.YearlyMeasurementCreate
) -> observations.YearlyMeasurement:
    """Create a new yearly measurement."""
    db_measurement = observations.YearlyMeasurement(
        **measurement_create.model_dump())
    session.add(db_measurement)
    try:
        session.commit()
    except sqlalchemy.exc.DBAPIError:
        raise
    else:
        session.refresh(db_measurement)
        return db_measurement


def create_many_yearly_measurements(
        session: sqlmodel.Session,
        measurements_to_create: Sequence[observations.YearlyMeasurementCreate],
) -> list[observations.YearlyMeasurement]:
    """Create several yearly measurements."""
    db_records = []
    for measurement_create in measurements_to_create:
        db_measurement = observations.YearlyMeasurement(
            **measurement_create.model_dump())
        db_records.append(db_measurement)
        session.add(db_measurement)
    try:
        session.commit()
    except sqlalchemy.exc.DBAPIError:
        raise
    else:
        for db_record in db_records:
            session.refresh(db_record)
        return db_records


def get_yearly_measurement(
        session: sqlmodel.Session,
        measurement_id: uuid.UUID
) -> Optional[observations.YearlyMeasurement]:
    return session.get(observations.YearlyMeasurement, measurement_id)


def delete_yearly_measurement(
        session: sqlmodel.Session, measurement_id: uuid.UUID) -> None:
    """Delete a yearly measurement."""
    db_measurement = get_yearly_measurement(session, measurement_id)
    if db_measurement is not None:
        session.delete(db_measurement)
        session.commit()
    else:
        raise RuntimeError("Yearly measurement not found")


def list_yearly_measurements(
        session: sqlmodel.Session,
        *,
        limit: int = 20,
        offset: int = 0,
        station_id_filter: Optional[uuid.UUID] = None,
        variable_id_filter: Optional[uuid.UUID] = None,
        include_total: bool = False,
) -> tuple[Sequence[observations.YearlyMeasurement], Optional[int]]:
    """List existing yearly measurements."""
    statement = sqlmodel.select(observations.YearlyMeasurement).order_by(
        observations.YearlyMeasurement.year)
    if station_id_filter is not None:
        statement = statement.where(
            observations.YearlyMeasurement.station_id == station_id_filter)
    if variable_id_filter is not None:
        statement = statement.where(
            observations.YearlyMeasurement.variable_id == variable_id_filter)
    items = session.exec(statement.offset(offset).limit(limit)).all()
    num_items = (
        _get_total_num_records(session, statement) if include_total else None)
    return items, num_items


def collect_all_yearly_measurements(
        session: sqlmodel.Session,
        *,
        station_id_filter: Optional[uuid.UUID] = None,
        variable_id_filter: Optional[uuid.UUID] = None,
) -> Sequence[observations.YearlyMeasurement]:
    _, num_total = list_yearly_measurements(
        session,
        limit=1,
        station_id_filter=station_id_filter,
        variable_id_filter=variable_id_filter,
        include_total=True
    )
    result, _ = list_yearly_measurements(
        session,
        limit=num_total,
        station_id_filter=station_id_filter,
        variable_id_filter=variable_id_filter,
        include_total=False
    )
    return result


def get_configuration_parameter_value(
        session: sqlmodel.Session,
        configuration_parameter_value_id: uuid.UUID
) -> Optional[coverages.ConfigurationParameterValue]:
    return session.get(
        coverages.ConfigurationParameterValue, configuration_parameter_value_id)


def list_configuration_parameter_values(
        session: sqlmodel.Session,
        *,
        limit: int = 20,
        offset: int = 0,
        include_total: bool = False,
) -> tuple[Sequence[coverages.ConfigurationParameterValue], Optional[int]]:
    """List existing configuration parameters."""
    statement = sqlmodel.select(coverages.ConfigurationParameterValue).order_by(
        coverages.ConfigurationParameterValue.name)
    items = session.exec(statement.offset(offset).limit(limit)).all()
    num_items = (
        _get_total_num_records(session, statement) if include_total else None)
    return items, num_items


def collect_all_configuration_parameter_values(
        session: sqlmodel.Session,
) -> Sequence[coverages.ConfigurationParameterValue]:
    _, num_total = list_configuration_parameter_values(
        session, limit=1, include_total=True)
    result, _ = list_configuration_parameter_values(
        session, limit=num_total, include_total=False)
    return result


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
            for prop, value in av.model_dump(
                    exclude={"id"},
                    exclude_none=True,
                    exclude_unset=True
            ).items():
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


def get_coverage_configuration(
        session: sqlmodel.Session,
        coverage_configuration_id: uuid.UUID
) -> Optional[coverages.CoverageConfiguration]:
    return session.get(coverages.CoverageConfiguration, coverage_configuration_id)


def get_coverage_configuration_by_name(
        session: sqlmodel.Session,
        coverage_configuration_name: str
) -> Optional[coverages.CoverageConfiguration]:
    """Get a coverage configuration by its name.

    Since a coverage configuration name is unique, it can be used to uniquely
    identify it.
    """
    return session.exec(
        sqlmodel.select(coverages.CoverageConfiguration)
        .where(coverages.CoverageConfiguration.name == coverage_configuration_name)
    ).first()


def list_coverage_configurations(
        session: sqlmodel.Session,
        *,
        limit: int = 20,
        offset: int = 0,
        include_total: bool = False,
) -> tuple[Sequence[coverages.CoverageConfiguration], Optional[int]]:
    """List existing coverage configurations."""
    statement = sqlmodel.select(coverages.CoverageConfiguration).order_by(
        coverages.CoverageConfiguration.name)
    items = session.exec(statement.offset(offset).limit(limit)).all()
    num_items = (
        _get_total_num_records(session, statement) if include_total else None)
    return items, num_items


def collect_all_coverage_configurations(
        session: sqlmodel.Session,
) -> Sequence[coverages.CoverageConfiguration]:
    _, num_total = list_coverage_configurations(session, limit=1, include_total=True)
    result, _ = list_coverage_configurations(
        session, limit=num_total, include_total=False)
    return result


def create_coverage_configuration(
        session: sqlmodel.Session,
        coverage_configuration_create: coverages.CoverageConfigurationCreate
) -> coverages.CoverageConfiguration:
    logger.debug(f"inside database.create_coverage_configuration - {locals()=}")
    to_refresh = []
    db_coverage_configuration = coverages.CoverageConfiguration(
        name=coverage_configuration_create.name,
        thredds_url_pattern=coverage_configuration_create.thredds_url_pattern,
        unit=coverage_configuration_create.unit,
        palette=coverage_configuration_create.palette,
        color_scale_min=coverage_configuration_create.color_scale_min,
        color_scale_max=coverage_configuration_create.color_scale_max,
    )
    session.add(db_coverage_configuration)
    to_refresh.append(db_coverage_configuration)
    for possible in coverage_configuration_create.possible_values:
        db_conf_param_value = get_configuration_parameter_value(
            session, possible.configuration_parameter_value_id)
        possible_value = coverages.ConfigurationParameterPossibleValue(
            coverage_configuration=db_coverage_configuration,
            configuration_parameter_value=db_conf_param_value
        )
        session.add(possible_value)
        to_refresh.append(possible_value)
    session.commit()
    for item in to_refresh:
        session.refresh(item)
    return db_coverage_configuration


def update_coverage_configuration(
        session: sqlmodel.Session,
        db_coverage_configuration: coverages.CoverageConfiguration,
        coverage_configuration_update: coverages.CoverageConfigurationUpdate
) -> coverages.CoverageConfiguration:
    """Update a coverage configuration."""
    to_refresh = []
    # account for possible values being: added/deleted
    for existing_possible_value in db_coverage_configuration.possible_values:
        has_been_requested_to_remove = (
                existing_possible_value.configuration_parameter_value_id not in
                [
                    i.configuration_parameter_value_id
                    for i in coverage_configuration_update.possible_values
                ]
        )
        if has_been_requested_to_remove:
            session.delete(existing_possible_value)
    for pvc in coverage_configuration_update.possible_values:
        already_possible = (
                pvc.configuration_parameter_value_id
                in [
                    i.configuration_parameter_value_id
                    for i in db_coverage_configuration.possible_values
                ]
        )
        if not already_possible:
            db_possible_value = coverages.ConfigurationParameterPossibleValue(
                coverage_configuration=db_coverage_configuration,
                configuration_parameter_value_id=pvc.configuration_parameter_value_id
            )
            session.add(db_possible_value)
            to_refresh.append(db_possible_value)
    data_ = coverage_configuration_update.model_dump(
        exclude={"possible_values"}, exclude_unset=True, exclude_none=True)
    for key, value in data_.items():
        setattr(db_coverage_configuration, key, value)
    session.add(db_coverage_configuration)
    to_refresh.append(db_coverage_configuration)
    session.commit()
    for item in to_refresh:
        session.refresh(item)
    return db_coverage_configuration


def list_allowed_coverage_identifiers(
        session: sqlmodel.Session,
        *,
        coverage_configuration_id: uuid.UUID,
) -> list[str]:
    """Build list of legal coverage identifiers."""
    result = []
    db_cov_conf = get_coverage_configuration(session, coverage_configuration_id)
    if db_cov_conf is not None:
        pattern_parts = re.findall(
            r"\{(\w+)\}",
            db_cov_conf.coverage_id_pattern.partition("-")[-1])
        values_to_combine = []
        for part in pattern_parts:
            part_values = []
            for possible_value in db_cov_conf.possible_values:
                param_name_matches = (
                        possible_value.configuration_parameter_value.configuration_parameter.name == part
                )
                if param_name_matches:
                    part_values.append(possible_value.configuration_parameter_value.name)
            values_to_combine.append(part_values)
        # account for the possibility that there is an error in the
        # coverage_id_pattern, where some of the parts are not actually configured
        for index, container in enumerate(values_to_combine):
            if len(container) == 0:
                values_to_combine[index] = [pattern_parts[index]]
        for combination in itertools.product(*values_to_combine):
            dataset_id = "-".join((db_cov_conf.name, *combination))
            result.append(dataset_id)
    return result


def _get_total_num_records(session: sqlmodel.Session, statement):
    return session.exec(
        sqlmodel.select(sqlmodel.func.count()).select_from(statement)
    ).first()
