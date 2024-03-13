"""Command-line interface for the project."""

import dataclasses
import datetime as dt
import enum
import itertools
import typing
from pathlib import Path
from xml.etree import ElementTree as et

import requests
import typer


@dataclasses.dataclass
class ForecastTemporalPeriodMetadata:
    name: str
    code: str


class ForecastTemporalPeriod(enum.Enum):
    TW1 = ForecastTemporalPeriodMetadata(name="2021 - 2050", code="tw1")
    TW2 = ForecastTemporalPeriodMetadata(name="2071 - 2100", code="tw2")


@dataclasses.dataclass
class ForecastSeasonMetadata:
    name: str
    code: str


class ForecastSeason(enum.Enum):
    DJF = ForecastSeasonMetadata(name="Winter", code="DJF")
    MAM = ForecastSeasonMetadata(name="Spring", code="MAM")
    JJA = ForecastSeasonMetadata(name="Summer", code="JJA")
    SON = ForecastSeasonMetadata(name="Autumn", code="SON")


@dataclasses.dataclass
class ForecastModelMetadata:
    name: str
    code: str
    thredds_base_path: str


@dataclasses.dataclass
class ForecastScenarioMetadata:
    name: str
    code: str


class ForecastScenario(enum.Enum):
    RCP26 = ForecastScenarioMetadata(name="RCP26", code="rcp26")
    RCP45 = ForecastScenarioMetadata(name="RCP45", code="rcp45")
    RCP85 = ForecastScenarioMetadata(name="RCP85", code="rcp85")


class ForecastAnomalyVariablePathPattern(enum.Enum):
    TAS_ENSEMBLE = "ensembletwbc/clipped/tas_avg_anom_{period}_{scenario}_{season}_VFVGTAA.nc"
    TASMIN_ENSEMBLE = "ensembletwbc/clipped/tasmin_avg_anom_{period}_{scenario}_{season}_VFVGTAA.nc"
    TASMAX_ENSEMBLE = "ensembletwbc/clipped/tasmax_avg_anom_{period}_{scenario}_{season}_VFVGTAA.nc"
    PR_ENSEMBLE = "ensembletwbc/clipped/pr_avg_percentage_{period}_{scenario}_{season}_VFVGTAA.nc"
    TR_ENSEMBLE = "ensembletwbc/clipped/ecatran_20_avg_{period}_{scenario}_ls_VFVG.nc"
    SU30_ENSEMBLE = "ensembletwbc/clipped/ecasuan_30_avg_{period}_{scenario}_ls_VFVG.nc"
    FD_ENSEMBLE = "ensembletwbc/clipped/ecafdan_0_avg_{period}_{scenario}_ls_VFVG.nc"
    HWDI_ENSEMBLE = "ensembletwbc/clipped/heat_waves_anom_avg_55_{period}_{scenario}_JJA_VFVGTAA.nc"
    TAS_ECEARTHCCLM4817 = "taspr5rcm/clipped/tas_EC-EARTH_CCLM4-8-17_{scenario}_seas_{period}{season}_VFVGTAA.nc"
    TASMIN_ECEARTHCCLM4817 = "taspr5rcm/clipped/tasmin_EC-EARTH_CCLM4-8-17_{scenario}_seas_{period}{season}_VFVGTAA.nc"
    TASMAX_ECEARTHCCLM4817 = "taspr5rcm/clipped/tasmax_EC-EARTH_CCLM4-8-17_{scenario}_seas_{period}{season}_VFVGTAA.nc"
    HWDI_ECEARTHCCLM4817 = "indici5rcm/clipped/heat_waves_anom_EC-EARTH_CCLM4-8-17_{scenario}_JJA_55_{period}_VFVGTAA.nc"


app = typer.Typer()


@app.command()
def import_anomaly_forecast_datasets(target_dir: Path):
    download_url_pattern = (
        "https://thredds.arpa.veneto.it/thredds/fileServer/{path}"
    )
    session = requests.Session()
    seasonal_patterns = []
    annual_patterns = []
    for pattern in ForecastAnomalyVariablePathPattern:
        if all(
                (
                        "{season}" in pattern.value,
                        "{scenario}" in pattern.value,
                        "{period}" in pattern.value,
                )
        ):
            seasonal_patterns.append(pattern)
        else:
            annual_patterns.append(pattern)

    paths = []
    for seasonal_pattern in seasonal_patterns:
        combinator = itertools.product(
            ForecastScenario,
            ForecastTemporalPeriod,
            ForecastSeason,
        )
        for scenario, period, season in combinator:
            path = seasonal_pattern.value.format(
                scenario=scenario.value.code,
                period=period.value.code,
                season=season.value.code
            )
            paths.append((seasonal_pattern, path))
    for annual_pattern in annual_patterns:
        combinator = itertools.product(
            ForecastScenario,
            ForecastTemporalPeriod,
        )
        for scenario, period in combinator:
            path = annual_pattern.value.format(
                scenario=scenario.value.code,
                period=period.value.code,
            )
            paths.append((annual_pattern, path))
    for pattern, path in paths:
        print(f"Processing {pattern.name!r}...")
        output_path = target_dir / path
        if not output_path.exists():
            print(f"Saving {output_path!r}...")
            download_url = download_url_pattern.format(path=path)
            response = session.get(download_url, stream=True)
            response.raise_for_status()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with output_path.open("wb") as fh:
                for chunk in response.iter_content():
                    fh.write(chunk)
        else:
            print(f"path already exists ({output_path!r}) - skipping")
    print("Done!")

#
#
# @dataclasses.dataclass
# class ThreddsWildcardFilterSelector:
#     type_: typing.Literal["wildcard", "regexp"]
#     value: str
#     applies_to_datasets: bool = True
#     applies_to_collections: bool = False
#
#
# @dataclasses.dataclass
# class ThreddsDatasetScanFilter:
#     includes: list[ThreddsWildcardFilterSelector] = dataclasses.field(
#         default_factory=list)
#     excludes: list[ThreddsWildcardFilterSelector] = dataclasses.field(
#         default_factory=list)


@dataclasses.dataclass
class ThreddsClientService:
    name: str
    service_type: str
    base: str


@dataclasses.dataclass
class ThreddsClientPublicDataset:
    name: str
    id: str
    url_path: str


@dataclasses.dataclass
class ThreddsClientCatalogRef:
    title: str
    id: str
    name: str
    href: str


@dataclasses.dataclass
class ThreddsClientDataset:
    name: str
    properties: dict[str, str]
    metadata: dict[str, str]
    public_datasets: list[ThreddsClientPublicDataset]
    catalog_refs: list[ThreddsClientCatalogRef]


@dataclasses.dataclass
class ThreddsClientCatalog:
    url: str
    services: dict[str, ThreddsClientService]
    dataset: ThreddsClientDataset


_NAMESPACES: typing.Final = {
    "thredds": "http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0",
    "xlink": "http://www.w3.org/1999/xlink",
}


def discover_catalog_contents(
        catalog_host: str,
        catalog_ref: str,
        http_client: requests.Session,
        use_https: bool = True,
) -> ThreddsClientCatalog:
    """
    host: thredds.arpa.veneto.it
    catalog_ref: /thredds/catalog/ensembletwbc/clipped
    """


    url = _build_catalog_url(catalog_host, catalog_ref, use_https)
    response = http_client.get(url)
    response.raise_for_status()
    raw_catalog_description = response.content
    parsed_services, parsed_dataset = _parse_catalog_client_description(
        raw_catalog_description)
    return ThreddsClientCatalog(
        url=url,
        services={service.service_type: service for service in parsed_services},
        dataset=parsed_dataset
    )


def build_download_urls(
        catalog_host: str,
        catalog_contents: ThreddsClientCatalog,
        use_https: bool = True
) -> dict[str, str]:
    urls = {}
    url_pattern = "{scheme}://{host}/{service_base}/{dataset_path}"
    for dataset in catalog_contents.dataset.public_datasets:
        urls[dataset.id] = url_pattern.format(
            scheme="https" if use_https else "http",
            host=catalog_host,
            service_base=catalog_contents.services["HTTPServer"].base.strip("/"),
            dataset_path=dataset.url_path.strip("/")
        )
    return urls



def _build_catalog_url(host: str, catalog_ref: str, use_https: bool = True) -> str:
    return "{scheme}://{host}/{path}/catalog.xml".format(
        scheme="https" if use_https else "http",
        host=host,
        path=catalog_ref.strip("/")
    )


def _parse_catalog_client_description(
        catalog_description: bytes
) -> tuple[list[ThreddsClientService], ThreddsClientDataset]:
    root_element = et.fromstring(catalog_description)
    service_qn = et.QName(_NAMESPACES["thredds"], "service")
    dataset_qn = et.QName(_NAMESPACES["thredds"], "dataset")
    services = []
    for service_element in root_element.findall(f"./{service_qn}/"):
        service = _parse_service_element(service_element)
        services.append(service)
    dataset = _parse_dataset_element(
        root_element.findall(f"./{dataset_qn}")[0])
    return services, dataset


def _parse_service_element(service_el: et.Element) -> ThreddsClientService:
    return ThreddsClientService(
        name=service_el.get("name", default=""),
        service_type=service_el.get("serviceType", default=""),
        base=service_el.get("base", default="")
    )


def _parse_dataset_element(dataset_el: et.Element) -> ThreddsClientDataset:
    prop_qname = et.QName(_NAMESPACES["thredds"], "property")
    meta_qname = et.QName(_NAMESPACES["thredds"], "metadata")
    ds_qname = et.QName(_NAMESPACES["thredds"], "dataset")
    cat_ref_qname = et.QName(_NAMESPACES["thredds"], "catalogRef")
    properties = {}
    metadata = {}
    public_datasets = []
    catalog_references = []
    for element in dataset_el.findall("./"):
        match element.tag:
            case prop_qname.text:
                properties[element.get("name")] = element.get("value")
            case meta_qname.text:
                for metadata_element in element.findall("./"):
                    key = metadata_element.tag.replace(
                        f"{{{_NAMESPACES['thredds']}}}", "")
                    metadata[key] = metadata_element.text
            case ds_qname.text:
                public_ds = ThreddsClientPublicDataset(
                    name=element.get("name", ""),
                    id=element.get("ID", ""),
                    url_path=element.get("urlPath", ""),
                )
                public_datasets.append(public_ds)
            case cat_ref_qname.text:
                title_qname = et.QName(_NAMESPACES["xlink"], "title")
                href_qname = et.QName(_NAMESPACES["xlink"], "href")
                catalog_ref = ThreddsClientCatalogRef(
                    title=element.get(title_qname.text, ""),
                    id=element.get("ID", ""),
                    name=element.get("name", ""),
                    href=element.get(href_qname.text, ""),
                )
                catalog_references.append(catalog_ref)
    return ThreddsClientDataset(
        name=dataset_el.get("name", default=""),
        properties=properties,
        metadata=metadata,
        public_datasets=public_datasets,
        catalog_refs=catalog_references,
    )
#
#
# @dataclasses.dataclass
# class ThreddsDatasetScan:
#     """DatasetScan defines a single mapping between a URL base path and a directory.
#
#     DatasetScan configuration enables TDS to discover and serve some or all of the
#     datasets found in the mapped directory. It generates nested catalogs by scanning
#     the directory named in the `location` property and creating a `Dataset` for each
#     file found and a `CatalogRef` for each subdirectory
#
#     In the THREDDS configuration, a DatasetScan element can be used wherever a Dataset
#     is expected.
#
#     In the client view, DatasetScan elements get converted to CatalogRef elements
#
#     """
#
#     name: str
#     id: str
#     path: str  # is used to create the URL for files and catalogs, must be globally unique and must not contain leading or trailing slashes
#     location: str  # must be an absolute path to a directory
#     filter_: ThreddsDatasetScanFilter | None = None
#
#     def build_client_catalog_url(self):
#         ...
#
#     def build_download_url(self) -> str:
#         ...
#
#
# ensemble_5rcm_bc = ThreddsDatasetScan(
#     name="ENSEMBLE 5rcm BC",
#     id="ensembletwbc",
#     path="",
#     location="",
#     filter_=ThreddsDatasetScanFilter(
#         excludes=[
#             ThreddsWildcardFilterSelector(type_="wildcard", value="heat_waves_avg_*.nc"),
#             ThreddsWildcardFilterSelector(type_="wildcard", value="heat_waves_*DJF.nc"),
#             ThreddsWildcardFilterSelector(type_="wildcard", value="ecasuan_25_*.nc"),
#             ThreddsWildcardFilterSelector(
#                 type_="wildcard", value="ts",
#                 applies_to_datasets=False,
#                 applies_to_collections=True,
#             ),
#             ThreddsWildcardFilterSelector(
#                 type_="wildcard", value="thralert",
#                 applies_to_datasets=False,
#                 applies_to_collections=True,
#             ),
#             ThreddsWildcardFilterSelector(
#                 type_="w_null", value="thralert",
#                 applies_to_datasets=False,
#                 applies_to_collections=True,
#             ),
#         ]
#     )
# )
#
#
# @dataclasses.dataclass
# class AnomalyModelMetadata:
#     name: str
#     id: str
#     path: Path
#     location: str
#
#
# @app.command()
# def get_anomaly_data(target_dir: Path):
#     ...
