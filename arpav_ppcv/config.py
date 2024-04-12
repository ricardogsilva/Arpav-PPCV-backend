import logging
import re
from pathlib import Path

import pydantic
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)

logger = logging.getLogger(__name__)


class ContactSettings(pydantic.BaseModel):
    name: str = "info@geobeyond.it"
    url: str = "http://geobeyond.it"  # noqa
    email: str = "info@geobeyond.it"


class ThreddsDatasetSettings(pydantic.BaseModel):
    thredds_url_pattern: str
    unit: str | None = None
    palette: str
    range: list[float]
    allowed_values: dict[str, list[str]] | None = None

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
        allowed = self.allowed_values or {}
        for name, value in id_parameters.items():
            if value not in allowed.get(name, []):
                raise ValueError(
                    f"Invalid dataset identifier: {name!r} cannot take the "
                    f"value {value!r}"
                )
        return id_parameters


class ThreddsServerSettings(pydantic.BaseModel):
    base_url: str = "http://localhost:8080/thredds"
    wms_service_url_fragment: str = "wms"
    netcdf_subset_service_url_fragment: str = "ncss/grid"  # noqa
    datasets: dict[str, ThreddsDatasetSettings] = pydantic.Field(
        default_factory=dict)
    uncertainty_visualization_scale_range: tuple[float, float] = pydantic.Field(
        default=(0, 9))

    @pydantic.model_validator(mode="after")
    def strip_slashes_from_urls(self):
        self.base_url = self.base_url.strip("/")
        self.wms_service_url_fragment = (
            self.wms_service_url_fragment.strip("/"))
        self.netcdf_subset_service_url_fragment = (
            self.netcdf_subset_service_url_fragment.strip("/"))
        return self

    @pydantic.model_validator(mode="after")
    def validate_dataset_config_ids(self):
        illegal_strings = (
            "-",
        )
        for ds_conf_id in self.datasets.keys():
            for patt in illegal_strings:
                if patt in ds_conf_id:
                    raise ValueError(
                        f"Invalid dataset identifier: {ds_conf_id!r} - these patterns "
                        f"are not allowed to be part of a dataset "
                        f"identifier: {', '.join(repr(p) for p in illegal_strings)}"
                    )
        return self


class DjangoEmailSettings(pydantic.BaseModel):
    host: str = "localhost"
    host_user: str = "user"
    host_password: str = "password"
    port: int = 587


class DjangoThreddsSettings(pydantic.BaseModel):
    host: str = "localhost"
    auth_url: str = (
        "https://thredds.arpa.veneto.it/thredds/restrictedAccess/dati_accordo")
    port: int = 8080
    user: str = 'admin'
    password: str = 'admin'
    proxy: str = 'http://proxy:8089/thredds/'


class DjangoAppSettings(pydantic.BaseModel):
    settings_module: str = "djangoapp.settings"
    secret_key: str = "changeme"
    mount_prefix: str = "/legacy"
    static_root: Path = Path.home() / "django_static"
    static_mount_prefix: str = "/static/legacy"
    db_engine: str = "django.contrib.gis.db.backends.postgis"
    db_dsn: pydantic.PostgresDsn = pydantic.PostgresDsn(
        "postgresql://django_user:django_password@localhost:5432/django_db")
    email: DjangoEmailSettings = DjangoEmailSettings()
    redis_dsn: pydantic.RedisDsn = pydantic.RedisDsn("redis://localhost:6379")
    thredds: DjangoThreddsSettings = DjangoThreddsSettings()



class ArpavPpcvSettings(BaseSettings):  # noqa
    model_config = SettingsConfigDict(
        env_prefix="ARPAV_PPCV__",  # noqa
        env_nested_delimiter="__",
    )

    debug: bool = False
    bind_host: str = "127.0.0.1"
    bind_port: int = 5001
    public_url: str = "http://localhost:5001"
    db_dsn: pydantic.PostgresDsn = pydantic.PostgresDsn(
        "postgresql://user:password@localhost:5432/arpav_ppcv"
    )
    verbose_db_logs: bool = False
    contact: ContactSettings = ContactSettings()
    thredds_server: ThreddsServerSettings = ThreddsServerSettings()
    v1_mount_prefix: str = "/v1/api"
    v2_mount_prefix: str = "/v2/api"
    django_app: DjangoAppSettings = DjangoAppSettings()
    log_config_file: Path | None = None


def get_settings() -> ArpavPpcvSettings:
    return ArpavPpcvSettings()
