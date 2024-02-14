import asyncio
import os
import shlex
import sys
from pathlib import Path

import dagger

POSTGIS_IMAGE_VERSION = "postgis/postgis:16-3.4"


def get_env_variables() -> dict[str, str | None]:
    return {
        "API_COMMAND": os.getenv("API_COMMAND", "daphne"),
        "DEBUG": os.getenv("DEBUG", "0"),
        "PGPASSWORD": os.getenv("PGPASSWORD", "postgres"),
        "POSTGRES_DB_NAME": os.getenv("POSTGRES_DB_NAME", "postgres"),
        "POSTGRES_PORT_5432_TCP_ADDR": os.getenv("POSTGRES_PORT_5432_TCP_ADDR", "postgis"),
        "POSTGRES_USER": os.getenv("POSTGRES_USER", "postgres"),
        "REDIS_HOST": os.getenv("REDIS_HOST", "redis"),
        "SECRET_KEY": os.getenv("SECRET_KEY", "generate it e.g. from https://djecrety.ir/"),
        "SSL_CERTIFICATE": os.getenv("SSL_CERTIFICATE", "/etc/letsencrypt/live/yourdomain/fullchain.pem"),
        "SSL_KEY": os.getenv("SSL_KEY", "/etc/letsencrypt/live/yourdomain/privkey.pem"),
        "THREDDS_AUTH_URL": os.getenv("THREDDS_AUTH_URL", "https://thredds.arpa.veneto.it/thredds/restrictedAccess/dati_accordo"),
        "THREDDS_HOST": os.getenv("THREDDS_HOST", "https://thredds.arpa.veneto.it/thredds/"),
        "THREDDS_PASSWORD": os.getenv("THREDDS_PASSWORD", ""),
        "THREDDS_USER": os.getenv("THREDDS_USER", ""),
    }


async def build_and_test():
    env_variables = get_env_variables()
    conf = dagger.Config(
        log_output=sys.stderr,
    )
    repo_root = Path(__file__).parents[2]
    async with dagger.Connection(conf) as client:
        postgis_service = (
            client.container()
            .from_(POSTGIS_IMAGE_VERSION)
            .with_env_variable("PGDATA", "/var/lib/postgresql/data/pgdata")
            .with_env_variable("POSTGRES_DB", env_variables["POSTGRES_DB_NAME"])
            .with_env_variable("POSTGRES_PASSWORD", env_variables["PGPASSWORD"])
            .with_env_variable("POSTGRES_USER", env_variables["POSTGRES_USER"])
            .with_exposed_port(5432)
            .as_service()
        )

        src = client.host().directory(str(repo_root))
        built_container = (
            client.container()
            .build(
                context=src,
                dockerfile="Dockerfile"
            )
        )

        test_results = await (
            built_container.with_service_binding("db", postgis_service)
            .with_mounted_directory("/opt/api/tests", client.host().directory("./tests"))
            .with_env_variable("DEBUG", env_variables["DEBUG"])
            .with_env_variable("POSTGRES_DB_NAME", env_variables["POSTGRES_DB_NAME"])
            .with_env_variable("POSTGRES_USER", env_variables["POSTGRES_USER"])
            .with_env_variable("PGPASSWORD", env_variables["PGPASSWORD"])
            .with_env_variable("POSTGRES_PORT_5432_TCP_ADDR", "db")
            .with_env_variable("REDIS_HOST", env_variables["REDIS_HOST"])
            .with_env_variable("SECRET_KEY", env_variables["SECRET_KEY"])
            .with_env_variable("THREDDS_HOST", env_variables["THREDDS_HOST"])
            .with_env_variable("THREDDS_PASSWORD", env_variables["THREDDS_PASSWORD"])
            .with_env_variable("THREDDS_USER", env_variables["THREDDS_USER"])
            .with_exec(
                shlex.split(
                    "pip install "
                    "coverage==7.4.1 "
                    "pytest==8.0.0 "
                    "pytest-cov==4.1.0 "
                    "pytest-django==4.8.0"
                ),
                skip_entrypoint=True
            )
            .with_exec(
                shlex.split(
                    "python manage.py makemigrations "
                    "users "
                    "groups "
                    "forecastattributes "
                    "places "
                    "thredds"
                ),
                skip_entrypoint=True
            )
            .with_exec(shlex.split("python manage.py migrate"), skip_entrypoint=True)
            .with_exec(
                shlex.split("pytest --verbose --cov -k 'padoa' -x --reuse-db ../tests"),
                skip_entrypoint=True
            )
        ).stdout()
        print("Done")
        print(f"{test_results=}")


if __name__ == "__main__":
    asyncio.run(build_and_test())
