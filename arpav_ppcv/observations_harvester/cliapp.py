import httpx
import sqlmodel
import typer
from rich import print
from typing import (
    Annotated,
    Literal,
)

from .. import database
from . import operations

app = typer.Typer()


@app.command()
def refresh_stations(ctx: typer.Context) -> None:
    client = httpx.Client()
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        created = operations.refresh_stations(client, session)
        print(f"Created {len(created)} stations:")
        print("\n".join(s.code for s in created))


@app.command()
def refresh_monthly_measurements(
        ctx: typer.Context,
        station: Annotated[
            str,
            typer.Option(
                help=(
                        "Code of the station to process. If not provided, all "
                        "stations are processed."
                )
            )
        ] = None,
        variable: Annotated[
            str,
            typer.Option(
                help=(
                        "Name of the variable to process. If not provided, all "
                        "variables are processed."
                )
            )
        ] = None,
) -> None:
    client = httpx.Client()
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        created = _refresh_measurements(
            session,
            client,
            variable,
            station,
            "monthly"
        )
        print(f"Created {len(created)} monthly measurements:")
        print(
            "\n".join(
                f"{m.station.code}-{m.variable.name}-{m.year}"
                for m in created
            )
        )


@app.command()
def refresh_seasonal_measurements(
        ctx: typer.Context,
        station: Annotated[
            str,
            typer.Option(
                help=(
                        "Code of the station to process. If not provided, all "
                        "stations are processed."
                )
            )
        ] = None,
        variable: Annotated[
            str,
            typer.Option(
                help=(
                        "Name of the variable to process. If not provided, all "
                        "variables are processed."
                )
            )
        ] = None,
) -> None:
    client = httpx.Client()
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        created = _refresh_measurements(
            session,
            client,
            variable,
            station,
            "seasonal"
        )
        print(f"Created {len(created)} seasonal measurements:")
        print(
            "\n".join(
                f"{m.station.code}-{m.variable.name}-{m.year}"
                for m in created
            )
        )


@app.command()
def refresh_yearly_measurements(
        ctx: typer.Context,
        station: Annotated[
            str,
            typer.Option(
                help=(
                        "Code of the station to process. If not provided, all "
                        "stations are processed."
                )
            )
        ] = None,
        variable: Annotated[
            str,
            typer.Option(
                help=(
                        "Name of the variable to process. If not provided, all "
                        "variables are processed."
                )
            )
        ] = None,
) -> None:
    client = httpx.Client()
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        created = _refresh_measurements(
            session,
            client,
            variable,
            station,
            "yearly"
        )
        print(f"Created {len(created)} yearly measurements:")
        print(
            "\n".join(
                f"{m.station.code}-{m.variable.name}-{m.year}"
                for m in created
            )
        )


def _refresh_measurements(
        db_session: sqlmodel.Session,
        client: httpx.Client,
        variable_name: str | None,
        station_code: str | None,
        measurement_type: Literal["monthly", "seasonal", "yearly"],
) -> list:
    if station_code is not None:
        db_station = database.get_station_by_code(db_session, station_code)
        if db_station is not None:
            station_id = db_station.id
        else:
            raise SystemExit("Invalid station code")
    else:
        station_id = None
    if variable_name is not None:
        db_variable = database.get_variable_by_name(db_session, variable_name)
        if db_variable is not None:
            variable_id = db_variable.id
        else:
            raise SystemExit("Invalid variable name")
    else:
        variable_id = None

    handler = {
        "monthly": operations.refresh_monthly_measurements,
        "seasonal": operations.refresh_seasonal_measurements,
        "yearly": operations.refresh_yearly_measurements
    }[measurement_type]

    return handler(
        client,
        db_session,
        station_id=station_id,
        variable_id=variable_id,
    )
