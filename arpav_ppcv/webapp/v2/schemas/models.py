import pydantic


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


class ListMeta(pydantic.BaseModel):
    returned_records: int
    total_records: int
    total_filtered_records: int


class ListLinks(pydantic.BaseModel):
    self: str
    next: str | None = None
    previous: str | None = None
    first: str | None = None
    last: str | None = None


class ResourceList(pydantic.BaseModel):
    meta: ListMeta
    links: ListLinks
    items: list


class ThreddsDatasetConfigurationList(ResourceList):
    items: list[ThreddsDatasetConfiguration]


class ThreddsDatasetConfigurationIdentifierList(ResourceList):
    items: list[str]


class ForecastModelScenarioList(ResourceList):
    items: list[ForecastModelScenario]
