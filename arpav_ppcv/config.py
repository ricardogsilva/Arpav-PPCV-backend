import logging
from pathlib import Path
from typing import Optional

import pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class ContactSettings(pydantic.BaseModel):
    name: str = "info@geobeyond.it"
    url: str = "http://geobeyond.it"  # noqa
    email: str = "info@geobeyond.it"


class ThreddsServerSettings(pydantic.BaseModel):
    base_url: str = "http://localhost:8080/thredds"
    wms_service_url_fragment: str = "wms"
    netcdf_subset_service_url_fragment: str = "ncss/grid"  # noqa
    uncertainty_visualization_scale_range: tuple[float, float] = pydantic.Field(
        default=(0, 9)
    )

    @pydantic.model_validator(mode="after")
    def strip_slashes_from_urls(self):
        self.base_url = self.base_url.strip("/")
        self.wms_service_url_fragment = self.wms_service_url_fragment.strip("/")
        self.netcdf_subset_service_url_fragment = (
            self.netcdf_subset_service_url_fragment.strip("/")
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
        "https://thredds.arpa.veneto.it/thredds/restrictedAccess/dati_accordo"
    )
    port: int = 8080
    user: str = "admin"
    password: str = "admin"
    proxy: str = "http://proxy:8089/thredds/"


class DjangoAppSettings(pydantic.BaseModel):
    settings_module: str = "djangoapp.settings"
    secret_key: str = "changeme"
    mount_prefix: str = "/legacy"
    static_root: Path = Path.home() / "django_static"
    # static_mount_prefix: str = "/static/legacy"
    static_mount_prefix: str = "/legacy-static"
    db_engine: str = "django.contrib.gis.db.backends.postgis"
    db_dsn: pydantic.PostgresDsn = pydantic.PostgresDsn(
        "postgresql://django_user:django_password@localhost:5432/django_db"
    )
    email: DjangoEmailSettings = DjangoEmailSettings()
    redis_dsn: pydantic.RedisDsn = pydantic.RedisDsn("redis://localhost:6379")
    thredds: DjangoThreddsSettings = DjangoThreddsSettings()


class AdminUserSettings(pydantic.BaseModel):
    username: str = "arpavadmin"
    password: str = "arpavpassword"
    name: str = "Admin"
    avatar: Optional[str] = None
    company_logo_url: Optional[str] = None
    roles: list[str] = pydantic.Field(
        default_factory=lambda: [
            "read",
            "create",
            "edit",
            "delete",
            "action_make_published",
        ]
    )


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
    test_db_dsn: Optional[pydantic.PostgresDsn] = None
    verbose_db_logs: bool = False
    contact: ContactSettings = ContactSettings()
    templates_dir: Optional[Path] = Path(__file__).parent / "webapp/templates"
    static_dir: Optional[Path] = Path(__file__).parent / "webapp/static"
    thredds_server: ThreddsServerSettings = ThreddsServerSettings()
    martin_tile_server_base_url: str = "http://localhost:3000"
    nearest_station_radius_meters: int = 10_000
    v1_api_mount_prefix: str = "/api/v1"
    v2_api_mount_prefix: str = "/api/v2"
    django_app: DjangoAppSettings = DjangoAppSettings()
    log_config_file: Path | None = None
    session_secret_key: str = "changeme"
    admin_user: AdminUserSettings = AdminUserSettings()
    cors_origins: list[str] = []
    cors_methods: list[str] = []
    allow_cors_credentials: bool = False

    @pydantic.model_validator(mode="after")
    def ensure_test_db_dsn(self):
        if self.test_db_dsn is None:
            rest, standard_db_name = self.db_dsn.unicode_string().rpartition("/")[::2]
            test_db_name = f"test_{standard_db_name}"
            self.test_db_dsn = pydantic.PostgresDsn(f"{rest}/{test_db_name}")
        return self


def get_settings() -> ArpavPpcvSettings:
    return ArpavPpcvSettings()
