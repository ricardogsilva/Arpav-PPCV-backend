"""Command-line interface for the project."""

import logging
import os
import sys
from typing import (
    Annotated,
    Optional
)
from pathlib import Path

import anyio
import django
import httpx
import typer
from django.conf import settings as django_settings
from django.core import management

from .thredds import crawler
from .webapp.legacy.django_settings import get_custom_django_settings
from . import config

app = typer.Typer()
dev_app = typer.Typer()
app.add_typer(dev_app, name="dev")


@app.callback()
def base_callback(ctx: typer.Context) -> None:
    ctx_obj = ctx.ensure_object(dict)
    settings = config.get_settings()
    ctx_obj.update(
        {
            "settings": settings,
        }
    )
    logging.basicConfig(level=logging.DEBUG if settings.debug else logging.INFO)


@app.command()
def run_server(ctx: typer.Context):
    """Run the uvicorn server.

    Example (dev) invocation:

    ```
    bash -c 'set -o allexport; source sample_env.env; set +o allexport; poetry run arpav-ppcv.run-server'
    ```
    """
    # NOTE: we explicitly do not use uvicorn's programmatic running abilities here
    # because they do not work correctly when called outside an
    # `if __name__ == __main__` guard and when using its debug features.
    # For more detail check:
    #
    # https://github.com/encode/uvicorn/issues/1045
    #
    # This solution works well both in development (where we want to use reload)
    # and in production, as using os.execvp is actually similar to just running
    # the standard `uvicorn` cli command (which is what uvicorn docs recommend).
    settings: config.ArpavPpcvSettings = ctx.obj["settings"]
    uvicorn_args = [
        "uvicorn",
        "arpav_ppcv.webapp.app:create_app",
        f"--port={settings.bind_port}",
        f"--host={settings.bind_host}",
        "--factory",
    ]
    if settings.debug:
        uvicorn_args.extend(
            [
                "--reload",
                f"--reload-dir={str(Path(__file__).parent)}",
                "--log-level=debug",
            ]
        )
    else:
        uvicorn_args.extend(["--log-level=info"])
    if (log_config_file := settings.uvicorn_log_config_file) is not None:
        uvicorn_args.append(f"--log-config={str(log_config_file)}")
    sys.stdout.flush()
    sys.stderr.flush()
    os.execvp("uvicorn", uvicorn_args)


@app.command(
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    }
)
def django_admin(ctx: typer.Context, command: str):
    """Run a django command.

    Run a django management command, just like if you were calling django-admin.
    """
    settings: config.ArpavPpcvSettings = ctx.obj["settings"]
    custom_django_settings = get_custom_django_settings(settings)
    django_settings.configure(**custom_django_settings)
    django.setup()
    management.call_command(command, *ctx.args)


@dev_app.command()
def import_thredds_datasets(
        catalog: Annotated[
            Optional[list[crawler.KnownCatalogIdentifier]],
            typer.Option(default_factory=list)
        ],
        output_base_dir: Annotated[
            Optional[Path],
            typer.Option(
                help=(
                        "Where datasets should be downloaded to. If this parameter is "
                        "not provided, only the total number of found datasets "
                        "is shown."
                )
            )
        ] = None,
        wildcard_filter: Annotated[
            str,
            typer.Option(help="Wildcard filter for selecting only relevant datasets")
        ] = "*",
        force_download: Annotated[
            Optional[bool],
            typer.Option(
                help=(
                        "Whether to re-download a dataset even if it is already "
                        "present locally."
                )
            )
        ] = False,
):
    relevant_catalogs = (
        catalog if len(catalog) > 0 else list(crawler.KnownCatalogIdentifier))
    client = httpx.Client()
    for relevant_catalog in relevant_catalogs:
        print(f"Processing catalog {relevant_catalog.value!r}...")
        catalog_url = crawler.get_catalog_url(relevant_catalog)
        contents = crawler.discover_catalog_contents(catalog_url, client)
        print(f"Found {len(contents.get_public_datasets(wildcard_filter))} datasets")
        if output_base_dir is not None:
            print("Downloading datasets...")
            anyio.run(
                crawler.download_datasets,  # noqa
                output_base_dir,
                contents,
                wildcard_filter,
                force_download,
            )