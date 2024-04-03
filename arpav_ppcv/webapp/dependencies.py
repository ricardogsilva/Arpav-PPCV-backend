import httpx

from .. import config


def get_settings() -> config.ArpavPpcvSettings:
    return config.get_settings()


def get_http_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()
