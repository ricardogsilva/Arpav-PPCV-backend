import datetime as dt
import uuid
from typing import (
    Annotated,
    Optional,
)

import geojson_pydantic
import pydantic_core
import sqlmodel
import typer

from .. import database
from . import schemas

app = typer.Typer()


@app.command(name="list-stations")
def list_stations(ctx: typer.Context) -> None:
    """List stations."""
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        result = [
            schemas.StationRead(**s.model_dump())
            for s in database.collect_all_stations(session)
        ]
        print(pydantic_core.to_json(result).decode("utf-8"))


@app.command(
    name="create-station",
    context_settings={
        "ignore_unknown_options": True
    }
)
def create_station(
        ctx: typer.Context,
        code: str,
        longitude: Annotated[float, typer.Argument(min=-180, max=180)],
        latitude: Annotated[float, typer.Argument(min=-90, max=90)],
        altitude: Annotated[float, typer.Option(min=-50, max=10_000)] = None,
        name: Annotated[str, typer.Option(help="Station name")] = "",
        type: Annotated[str, typer.Option(help="Station type")] = "",
) -> None:
    station_create = schemas.StationCreate(
        geom=geojson_pydantic.Point(
            type="Point", coordinates=(longitude, latitude)
        ),
        code=code,
        altitude_m=altitude,
        name=name,
        type_=type.lower().replace(" ", "_")
    )
    """Create a new station."""
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        db_station = database.create_station(session, station_create)
        print(schemas.StationRead(**db_station.model_dump()).model_dump_json())


@app.command(name="delete-station")
def delete_station(
        ctx: typer.Context,
        station_id: uuid.UUID,
) -> None:
    """Delete a station."""
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        database.delete_station(session, station_id)


@app.command(name="list-variables")
def list_variables(ctx: typer.Context) -> None:
    """List variables."""
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        result = [
            schemas.VariableRead(**v.model_dump())
            for v in database.collect_all_variables(session)
        ]
        print(pydantic_core.to_json(result).decode("utf-8"))


@app.command(name="create-variable")
def create_variable(
        ctx: typer.Context,
        name: str,
        description: str,
        unit: Optional[str] = "",
) -> None:
    variable_create = schemas.VariableCreate(
        name=name,
        description=description,
        unit=unit
    )
    """Create a new variable."""
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        db_variable = database.create_variable(session, variable_create)
        print(schemas.VariableRead(**db_variable.model_dump()).model_dump_json())


@app.command(name="delete-variable")
def delete_variable(
        ctx: typer.Context,
        variable_id: uuid.UUID,
) -> None:
    """Delete a variable."""
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        database.delete_variable(session, variable_id)


@app.command(name="list-monthly-measurements")
def list_monthly_measurements(ctx: typer.Context) -> None:
    """List monthly measurements."""
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        result = [
            schemas.MonthlyMeasurementRead(**v.model_dump())
            for v in database.collect_all_monthly_measurements(session)
        ]
        print(pydantic_core.to_json(result).decode("utf-8"))


@app.command(
    name="create-monthly-measurement",
    context_settings={
        "ignore_unknown_options": True
    }
)
def create_monthly_measurement(
        ctx: typer.Context,
        station_code: str,
        variable: str,
        date: dt.datetime,
        value: float,
) -> None:
    """Create a new variable."""
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        db_station = database.get_station_by_code(session, station_code)
        db_variable = database.get_variable_by_name(session, variable)
        if db_station is None:
            raise SystemExit("Invalid station code")
        elif db_variable is None:
            raise SystemExit("invalid variable")
        else:
            db_monthly_measurement = database.create_monthly_measurement(
                session,
                schemas.MonthlyMeasurementCreate(
                    station_id=db_station.id,
                    variable_id=db_variable.id,
                    date=dt.date(date.year, date.month, 1),
                    value=value
                )
            )
        print(
            schemas.MonthlyMeasurementRead(
                **db_monthly_measurement.model_dump()
            ).model_dump_json()
        )


@app.command(name="delete-monthly-measurement")
def delete_monthly_measurement(
        ctx: typer.Context,
        monthly_measurement_id: uuid.UUID,
) -> None:
    """Delete a monthly measurement."""
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        database.delete_monthly_measurement(session, monthly_measurement_id)
