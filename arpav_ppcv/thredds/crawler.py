import logging
import traceback
import typing
from itertools import islice
from pathlib import Path

import anyio
import exceptiongroup
import httpx
import sqlmodel

from ..schemas import coverages
from .. import database

logger = logging.getLogger(__name__)


_NAMESPACES: typing.Final = {
    "thredds": "http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0",
    "xlink": "http://www.w3.org/1999/xlink",
}

_THREDDS_FILE_SERVER_URL_FRAGMENT = "fileServer"


def get_coverage_configuration_urls(
    session: sqlmodel.Session,
    base_thredds_url: str,
    coverage_configuration: coverages.CoverageConfiguration,
) -> list[str]:
    coverage_identifiers = database.list_allowed_coverage_identifiers(
        session, coverage_configuration_id=coverage_configuration.id
    )
    result = []
    for cov_identifier in coverage_identifiers:
        result.append(
            "/".join(
                (
                    base_thredds_url,
                    _THREDDS_FILE_SERVER_URL_FRAGMENT,
                    coverage_configuration.get_thredds_url_fragment(cov_identifier),
                )
            )
        )
    return result


async def download_datasets(
    dataset_urls: list[str],
    base_thredds_url: str,
    output_base_directory: Path,
    force_download: bool = False,
) -> None:
    client = httpx.AsyncClient()
    logger.debug(f"There are {len(dataset_urls)} URLS to process in total")
    for batch in _batched(dataset_urls, 10):
        with exceptiongroup.catch({Exception: handle_thredds_download_exception}):
            async with anyio.create_task_group() as tg:
                for dataset_url in batch:
                    output_path = Path(
                        dataset_url.replace(
                            f"{base_thredds_url}/{_THREDDS_FILE_SERVER_URL_FRAGMENT}",
                            str(output_base_directory),
                        )
                    )
                    tg.start_soon(
                        download_individual_dataset,
                        client,
                        output_path,
                        dataset_url,
                        force_download,
                    )


def handle_thredds_download_exception(excgroup: exceptiongroup.ExceptionGroup):
    for exc in excgroup.exceptions:
        logger.warning("\n".join(traceback.format_exception(exc)))


async def download_individual_dataset(
    http_client: httpx.AsyncClient,
    output_path: Path,
    dataset_url: str,
    force_download: bool = False,
) -> None:
    if (not output_path.exists()) or force_download:
        async with http_client.stream("GET", dataset_url) as response:
            try:
                # we catch the exception here because anyio task groups seem
                # to cancel all tasks as soon as one of them raises an exception
                response.raise_for_status()
            except httpx.HTTPStatusError:
                logger.exception(f"Could not download dataset: {dataset_url}")
            else:
                logger.info(f"Downloading {dataset_url!r}...")
                output_dir = output_path.parent
                output_dir.mkdir(parents=True, exist_ok=True)
                with output_path.open("wb") as fh:
                    async for chunk in response.aiter_bytes():
                        fh.write(chunk)
    else:
        logger.info(f"dataset {output_path!r} already exists locally, skipping...")


def _batched(iterable, n):
    """Custom implementation of `itertools.batched()`.

    This is a custom implementation of `itertools.batched()`, which is only available
    on Python 3.12+. This is copied verbatim from the python docs at:

    https://docs.python.org/3/library/itertools.html#itertools.batched

    """
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch
