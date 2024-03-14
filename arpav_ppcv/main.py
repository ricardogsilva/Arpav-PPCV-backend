"""Command-line interface for the project."""

import enum
from typing import (
    Annotated,
    Optional
)
from pathlib import Path

import anyio
import httpx
import typer

from .thredds import crawler


class KnownCatalogIdentifier(enum.Enum):
    THIRTY_YEAR_ANOMALY_5_MODEL_AVERAGE = "30y-anomaly-ensemble"
    THIRTY_YEAR_ANOMALY_TEMPERATURE_PRECIPITATION = "30y-anomaly-tas-pr"
    THIRTY_YEAR_ANOMALY_CLIMATIC_INDICES = "30y-anomaly-climate-idx"


def _get_catalog_url(catalog_identifier: KnownCatalogIdentifier) -> str:
    return {
        KnownCatalogIdentifier.THIRTY_YEAR_ANOMALY_5_MODEL_AVERAGE: (
            "https://thredds.arpa.veneto.it/thredds/catalog/ensembletwbc/clipped"),
        KnownCatalogIdentifier.THIRTY_YEAR_ANOMALY_TEMPERATURE_PRECIPITATION: (
            "https://thredds.arpa.veneto.it/thredds/catalog/taspr5rcm/clipped"),
        KnownCatalogIdentifier.THIRTY_YEAR_ANOMALY_CLIMATIC_INDICES: (
            "https://thredds.arpa.veneto.it/thredds/catalog/indici5rcm/clipped"),
    }[catalog_identifier]


app = typer.Typer()

@app.command()
def import_thredds_datasets(
        catalog: Annotated[KnownCatalogIdentifier, typer.Argument(...)],
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
        ] = "*"
):
    catalog_url = _get_catalog_url(catalog)
    client = httpx.Client()
    print(f"Parsing catalog contents...")
    contents = crawler.discover_catalog_contents(catalog_url, client)
    print(f"Found {len(contents.get_public_datasets(wildcard_filter))} datasets")
    if output_base_dir is not None:
        print("Downloading datasets...")
        anyio.run(
            crawler.download_datasets,
            output_base_dir,
            contents,
            wildcard_filter
        )
