import httpx
import sqlmodel
import typer

from . import operations

app = typer.Typer()


@app.command()
def refresh_variables(ctx: typer.Context) -> None:
    client = httpx.Client()
    with sqlmodel.Session(ctx.obj["engine"]) as session:
        created, updated = operations.refresh_variables(client, session)
        print(f"Created {len(created)} variables:")
        print("\n".join(v.name for v in created))
        print(f"Updated {len(updated)} variables:")
        print("\n".join(v.name for v in updated))
