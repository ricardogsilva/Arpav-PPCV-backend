import dataclasses
import enum
import fnmatch
import urllib.parse


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
class ForecastScenarioMetadata:
    name: str
    code: str


class ForecastScenario(enum.Enum):
    RCP26 = ForecastScenarioMetadata(name="RCP26", code="rcp26")
    RCP45 = ForecastScenarioMetadata(name="RCP45", code="rcp45")
    RCP85 = ForecastScenarioMetadata(name="RCP85", code="rcp85")


class AveragingPeriod(enum.Enum):
    YEAR = "year"
    THIRTY_YEAR = "thirty-year"



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
    public_datasets: dict[str, ThreddsClientPublicDataset]
    catalog_refs: dict[str, ThreddsClientCatalogRef]


@dataclasses.dataclass
class ThreddsClientCatalog:
    url: urllib.parse.ParseResult
    services: dict[str, ThreddsClientService]
    dataset: ThreddsClientDataset

    def build_dataset_download_url(self, dataset_id: str) -> str:
        dataset = self.dataset.public_datasets[dataset_id]
        url_pattern = "{scheme}://{host}/{service_base}/{dataset_path}"
        return url_pattern.format(
            scheme=self.url.scheme,
            host=self.url.netloc,
            service_base=self.services["HTTPServer"].base.strip("/"),
            dataset_path=dataset.url_path.strip("/")
        )

    def get_public_datasets(
            self,
            wildcard_pattern: str = "*"
    ) -> dict[str, ThreddsClientPublicDataset]:
        relevant_ids = fnmatch.filter(
            self.dataset.public_datasets.keys(), wildcard_pattern)
        return {id_: self.dataset.public_datasets[id_] for id_ in relevant_ids}
