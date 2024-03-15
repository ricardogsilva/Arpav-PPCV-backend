"""Command-line interface for the project."""

import enum
import logging
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
    YEARLY_ANOMALY_5_MODEL_AVERAGE_TAS_PR = "anomaly-ensemble-tas-pr"
    YEARLY_ABSOLUTE_5_MODEL_AVERAGE = "yearly-ensemble-absolute"
    YEARLY_ANOMALY_EC_EARTH_CCLM4_8_17 = "anomaly-ec-earth-cclm4-8-17"
    YEARLY_ABSOLUTE_EC_EARTH_CCLM4_8_17 = "yearly-ec-earth-cclm4-8-17-absolute"
    YEARLY_ANOMALY_EC_EARTH_RACM022E = "anomaly-ec-earth-racm022e"
    YEARLY_ABSOLUTE_EC_EARTH_RACM022E = "yearly-ec-earth-racm022e-absolute"
    YEARLY_ANOMALY_EC_EARTH_RCA4 = "anomaly-ec-earth-rca4"
    YEARLY_ABSOLUTE_EC_EARTH_RCA4 = "yearly-ec-earth-rca4-absolute"
    YEARLY_ANOMALY_HADGEM2_ES_RACMO22E = "anomaly-hadgem2-es-racmo22e"
    YEARLY_ABSOLUTE_HADGEM2_ES_RACMO22E = "yearly-hadgem2-es-racmo22e-absolute"
    YEARLY_ANOMALY_MPI_ESM_LR_REMO2009 = "anomaly-mpi-esm-lr-remo2009"
    YEARLY_ABSOLUTE_MPI_ESM_LR_REMO2009 = "yearly-mpi-esm-lr-remo2009-absolute"



def _get_catalog_url(catalog_identifier: KnownCatalogIdentifier) -> str:
    return {
        KnownCatalogIdentifier.THIRTY_YEAR_ANOMALY_5_MODEL_AVERAGE: (
            "https://thredds.arpa.veneto.it/thredds/catalog/ensembletwbc/clipped"),
        KnownCatalogIdentifier.THIRTY_YEAR_ANOMALY_TEMPERATURE_PRECIPITATION: (
            "https://thredds.arpa.veneto.it/thredds/catalog/taspr5rcm/clipped"),
        KnownCatalogIdentifier.THIRTY_YEAR_ANOMALY_CLIMATIC_INDICES: (
            "https://thredds.arpa.veneto.it/thredds/catalog/indici5rcm/clipped"),
        KnownCatalogIdentifier.YEARLY_ANOMALY_5_MODEL_AVERAGE_TAS_PR: (
            "https://thredds.arpa.veneto.it/thredds/catalog/ens5ym/clipped"),
        KnownCatalogIdentifier.YEARLY_ABSOLUTE_5_MODEL_AVERAGE: (
            "https://thredds.arpa.veneto.it/thredds/catalog/ensymbc/clipped"),
        KnownCatalogIdentifier.YEARLY_ANOMALY_EC_EARTH_CCLM4_8_17: (
            "https://thredds.arpa.veneto.it/thredds/catalog/EC-EARTH_CCLM4-8-17ym/clipped"),
        KnownCatalogIdentifier.YEARLY_ABSOLUTE_EC_EARTH_CCLM4_8_17: (
            "https://thredds.arpa.veneto.it/thredds/catalog/EC-EARTH_CCLM4-8-17ymbc/clipped"),
        KnownCatalogIdentifier.YEARLY_ANOMALY_EC_EARTH_RACM022E: (
            "https://thredds.arpa.veneto.it/thredds/catalog/EC-EARTH_RACMO22Eym/clipped"),
        KnownCatalogIdentifier.YEARLY_ABSOLUTE_EC_EARTH_RACM022E: (
            "https://thredds.arpa.veneto.it/thredds/catalog/EC-EARTH_RACMO22Eymbc/clipped"),
        KnownCatalogIdentifier.YEARLY_ANOMALY_EC_EARTH_RCA4: (
            "https://thredds.arpa.veneto.it/thredds/catalog/EC-EARTH_RCA4ym/clipped"),
        KnownCatalogIdentifier.YEARLY_ABSOLUTE_EC_EARTH_RCA4: (
            "https://thredds.arpa.veneto.it/thredds/catalog/EC-EARTH_RCA4ymbc/clipped"),
        KnownCatalogIdentifier.YEARLY_ANOMALY_HADGEM2_ES_RACMO22E: (
            "https://thredds.arpa.veneto.it/thredds/catalog/HadGEM2-ES_RACMO22Eym/clipped"),
        KnownCatalogIdentifier.YEARLY_ABSOLUTE_HADGEM2_ES_RACMO22E: (
            "https://thredds.arpa.veneto.it/thredds/catalog/HadGEM2-ES_RACMO22Eymbc/clipped"),
        KnownCatalogIdentifier.YEARLY_ANOMALY_MPI_ESM_LR_REMO2009: (
            "https://thredds.arpa.veneto.it/thredds/catalog/MPI-ESM-LR_REMO2009ym/clipped"),
        KnownCatalogIdentifier.YEARLY_ABSOLUTE_MPI_ESM_LR_REMO2009: (
            "https://thredds.arpa.veneto.it/thredds/catalog/MPI-ESM-LR_REMO2009ymbc/clipped"),
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
        verbose: Annotated[
            Optional[bool],
            typer.Option(
                help=(
                        "Verbose output"
                )
            )
        ] = False
):
    if verbose:
        logging.basicConfig(level=logging.INFO)
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
            wildcard_filter,
            force_download,
        )
