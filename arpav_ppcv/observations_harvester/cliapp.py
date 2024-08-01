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
def refresh_stations(
    ctx: typer.Context,
    variable: Annotated[
        str,
        typer.Option(
            help=(
                "Name of the variable to process. If not provided, all "
                "variables are processed."
            )
        ),
    ] = None,
    month: Annotated[
        int,
        typer.Option(
            help=(
                "Only refresh stations that have monthly measurements for "
                "the input month."
            )
        ),
    ] = None,
    season: Annotated[
        int,
        typer.Option(
            help=(
                "Only refresh stations that have seasonal measurements for "
                "the input season."
            )
        ),
    ] = None,
    year: Annotated[
        bool, typer.Option(help=("Only refresh stations that have yearly measurements"))
    ] = False,
) -> None:
    client = httpx.AsyncClient(timeout=30)
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        if variable is not None:
            db_variable = database.get_variable_by_name(session, variable)
            if db_variable is not None:
                variable_filter = [db_variable]
            else:
                raise SystemExit("Invalid variable name")
        else:
            variable_filter = database.collect_all_variables(session)
        created = operations.refresh_stations(
            client,
            session,
            variable_filter,
            fetch_stations_with_months=[month] if month is not None else None,
            fetch_stations_with_seasons=[season] if season is not None else None,
            fetch_stations_with_yearly_measurements=year,
        )
        print(f"Created {len(created)} stations:")
        print("\n".join(s.code for s in created))


@app.command()
def refresh_monthly_measurements(
    ctx: typer.Context,
    station: Annotated[
        list[str],
        typer.Option(
            default_factory=list,
            help=(
                "Code of the station to process. If not provided, all "
                "stations are processed."
            ),
        ),
    ],
    variable: Annotated[
        str,
        typer.Option(
            help=(
                "Name of the variable to process. If not provided, all "
                "variables are processed."
            )
        ),
    ] = None,
) -> None:
    client = httpx.Client()
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        for station_code in station:
            print(f"Processing station: {station_code!r}...")
            created = _refresh_measurements(
                session, client, variable, station_code, "monthly"
            )
            print(f"Created {len(created)} monthly measurements:")
            print(
                "\n".join(
                    f"{m.station.code}-{m.variable.name}-{m.date.strftime('%Y-%m-%d')}"
                    for m in created
                )
            )


@app.command()
def refresh_seasonal_measurements(
    ctx: typer.Context,
    station: Annotated[
        list[str],
        typer.Option(
            default_factory=list,
            help=(
                "Code of the station to process. If not provided, all "
                "stations are processed."
            ),
        ),
    ],
    variable: Annotated[
        str,
        typer.Option(
            help=(
                "Name of the variable to process. If not provided, all "
                "variables are processed."
            )
        ),
    ] = None,
) -> None:
    client = httpx.Client()
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        if len(station) > 0:
            for station_code in station:
                print(f"Processing station {station_code!r}...")
                created = _refresh_measurements(
                    session, client, variable, station_code, "seasonal"
                )
        else:
            created = _refresh_measurements(session, client, variable, None, "seasonal")
        print(f"Created {len(created)} seasonal measurements:")
        print(
            "\n".join(f"{m.station.code}-{m.variable.name}-{m.year}" for m in created)
        )


@app.command()
def refresh_yearly_measurements(
    ctx: typer.Context,
    station: Annotated[
        list[str],
        typer.Option(
            default_factory=list,
            help=(
                "Code of the station to process. If not provided, all "
                "stations are processed."
            ),
        ),
    ],
    variable: Annotated[
        str,
        typer.Option(
            help=(
                "Name of the variable to process. If not provided, all "
                "variables are processed."
            )
        ),
    ] = None,
) -> None:
    client = httpx.Client()
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        if len(station) > 0:
            for station_code in station:
                print(f"Processing station {station_code!r}...")
                created = _refresh_measurements(
                    session, client, variable, station_code, "yearly"
                )
        else:
            created = _refresh_measurements(session, client, variable, None, "yearly")
        print(f"Created {len(created)} yearly measurements:")
        print(
            "\n".join(f"{m.station.code}-{m.variable.name}-{m.year}" for m in created)
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
        "yearly": operations.refresh_yearly_measurements,
    }[measurement_type]

    return handler(
        client,
        db_session,
        station_id=station_id,
        variable_id=variable_id,
    )
