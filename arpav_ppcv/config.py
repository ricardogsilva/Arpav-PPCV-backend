import logging
import re

import pydantic
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)

logger = logging.getLogger(__name__)


class ContactSettings(pydantic.BaseModel):
    name: str = "info@geobeyond.it"
    url: str = "http://geobeyond.it"
    email: str = "info@geobeyond.it"


class ThreddsDatasetSettings(pydantic.BaseModel):
    thredds_url_pattern: str
    unit: str
    palette: str
    range: list[float]
    allowed_values: dict[str, list[str]]

    @pydantic.model_validator(mode="after")
    def strip_slashes_from_urls(self):
        self.thredds_url_pattern = self.thredds_url_pattern.strip("/")
        return self

    @pydantic.computed_field()
    @property
    def dataset_id_pattern(self) -> str:
        id_parts = ["{identifier}"]
        for match_obj in re.finditer(r"(\{\w+\})", self.thredds_url_pattern):
            id_parts.append(match_obj.group(1))
        return "-".join(id_parts)

    def get_dynamic_id_parameters(self, dataset_id: str) -> dict[str, str]:
        pattern_parts = re.finditer(
            r"\{(\w+)\}",
            self.dataset_id_pattern.partition("-")[-1])
        id_parts = dataset_id.split("-")[1:]
        result = {}
        for index, pattern_match_obj in enumerate(pattern_parts):
            id_part = id_parts[index]
            name = pattern_match_obj.group(1)
            result[name] = id_part
        return result

    def validate_dataset_id(self, dataset_id: str) -> dict[str, str]:
        id_parameters = self.get_dynamic_id_parameters(dataset_id)
        logger.debug(f"{id_parameters=}")
        for name, value in id_parameters.items():
            if value not in self.allowed_values.get(name, []):
                raise ValueError(
                    f"Invalid dataset identifier: {name!r} cannot take the "
                    f"value {value!r}"
                )
        return id_parameters


class ThreddsServerSettings(pydantic.BaseModel):
    base_url: str = "http://localhost:8080/thredds"
    wms_service_url_fragment: str = "wms"
    netcdf_subset_service_url_fragment: str = "ncss/grid"
    datasets: dict[str, ThreddsDatasetSettings] = pydantic.Field(
        default_factory=dict)

    @pydantic.model_validator(mode="after")
    def strip_slashes_from_urls(self):
        self.base_url = self.base_url.strip("/")
        self.wms_service_url_fragment = (
            self.wms_service_url_fragment.strip("/"))
        self.netcdf_subset_service_url_fragment = (
            self.netcdf_subset_service_url_fragment.strip("/"))
        return self


class ArpavPpcvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ARPAV_PPCV__",
        env_nested_delimiter="__",
    )

    debug: bool = False
    contact: ContactSettings = ContactSettings()
    thredds_server: ThreddsServerSettings = ThreddsServerSettings()


def get_settings() -> ArpavPpcvSettings:
    return ArpavPpcvSettings()
