import pydantic

from .base import ResourceList


class ForecastModelScenario(pydantic.BaseModel):
    name: str
    code: str


class ThreddsDatasetConfiguration(pydantic.BaseModel):
    identifier: str
    dataset_id_pattern: str
    unit: str | None = None
    palette: str
    range: list[float]
    allowed_values: dict[str, list[str]] | None = None


class ThreddsDatasetConfigurationList(ResourceList):
    items: list[ThreddsDatasetConfiguration]


class ThreddsDatasetConfigurationIdentifierList(ResourceList):
    items: list[str]


class ForecastModelScenarioList(ResourceList):
    items: list[ForecastModelScenario]
