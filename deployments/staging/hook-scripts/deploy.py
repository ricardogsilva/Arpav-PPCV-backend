# ARPAV-PPCV deployment script
#
# This script is to be run by the `webhook` server whenever there
# is a push to the arpav-ppcv-backend repository.
#
# In order to simplify deployment, this script only uses stuff from the Python
# standard library.

import argparse
import dataclasses
import json
import logging
import os
import shlex
import shutil
from pathlib import Path
from typing import (
    Protocol,
    Sequence,
)
from subprocess import run

logger = logging.getLogger(__name__)


class DeployStepProtocol(Protocol):
    name: str

    def handle(self) -> None:
        ...


@dataclasses.dataclass
class _ValidateRequestPayload:
    raw_payload: str
    name: str = "validate request payload"

    def handle(self) -> bool:
        try:
            payload = json.loads(self.raw_payload)
        except json.JSONDecodeError as err:
            raise RuntimeError("Could not decode payload as valid JSON") from err
        else:
            return all(
                (
                    payload.get("event") == "push",
                    payload.get("ref") == "refs/heads/main",
                    payload.get("repository", "").lower()
                    in (
                        "geobeyond/arpav-ppcv",
                        "geobeyond/arpav-ppcv-backend",
                    ),
                )
            )


@dataclasses.dataclass
class _FindDockerDir:
    docker_dir: Path
    name: str = "confirm docker dir exists"

    def handle(self) -> None:
        if not self.docker_dir.exists():
            raise RuntimeError(f"Docker dir {str(self.docker_dir)!r} does not exist")


@dataclasses.dataclass
class _StopCompose:
    docker_dir: Path
    compose_files_fragment: str
    name: str = "stop docker compose"

    def handle(self) -> None:
        print("Stopping docker compose stack...")
        run_result = run(
            shlex.split(f"docker compose {self.compose_files_fragment} down"),
        )
        if run_result.returncode == 14:
            logger.info("docker compose stack was not running, no need to stop")
        else:
            run_result.check_returncode()


@dataclasses.dataclass
class _CloneRepo:
    clone_destination: Path
    name: str = "clone git repository"

    def handle(self) -> None:
        print("Cloning repo...")
        if self.clone_destination.exists():
            shutil.rmtree(self.clone_destination)
        run(
            shlex.split(
                f"git clone https://github.com/geobeyond/Arpav-PPCV-backend.git "
                f"{self.clone_destination}"
            ),
            check=True,
        )


@dataclasses.dataclass
class _ReplaceDockerDir:
    docker_dir: Path
    repo_dir: Path
    name: str = "copy docker directory"

    def handle(self) -> None:
        # copy the `docker` directory and delete the rest - we are deploying docker
        # images, so no need for the source code
        repo_docker_dir = self.repo_dir / "docker"
        print(
            f"Copying the docker dir in {repo_docker_dir!r} "
            f"to {self.docker_dir!r}..."
        )
        shutil.rmtree(self.docker_dir, ignore_errors=True)
        shutil.copytree(repo_docker_dir, self.docker_dir)
        shutil.rmtree(str(repo_docker_dir), ignore_errors=True)


@dataclasses.dataclass
class _FindEnvFiles:
    env_files: dict[str, Path]
    name: str = "find environment file"

    def handle(self) -> None:
        print("Looking for env_file...")
        for env_file_path in self.env_files.values():
            if not env_file_path.exists():
                raise RuntimeError(
                    f"Could not find environment file {env_file_path!r}, aborting..."
                )


@dataclasses.dataclass
class _PullImage:
    images: Sequence[str]
    name: str = "pull new docker images from container registry"

    def handle(self) -> None:
        print("Pulling updated docker images...")
        run(shlex.split(f"docker pull {' '.join(self.images)}"), check=True)


@dataclasses.dataclass
class _StartCompose:
    env_file_db_service: Path
    env_file_legacy_db_service: Path
    env_file_webapp_service: Path
    env_file_frontend_service: Path
    compose_files_fragment: str
    name: str = "start docker compose"

    def handle(self) -> None:
        print("Restarting the docker compose stack...")
        run(
            shlex.split(
                f"docker compose {self.compose_files_fragment} up --detach "
                f"--force-recreate"
            ),
            env={
                **os.environ,
                "ARPAV_PPCV_DEPLOYMENT_ENV_FILE_DB_SERVICE": self.env_file_db_service,
                "ARPAV_PPCV_DEPLOYMENT_ENV_FILE_LEGACY_DB_SERVICE": self.env_file_legacy_db_service,  # noqa
                "ARPAV_PPCV_DEPLOYMENT_ENV_FILE_WEBAPP_SERVICE": self.env_file_webapp_service,  # noqa
                "ARPAV_PPCV_DEPLOYMENT_ENV_FILE_FRONTEND_SERVICE": self.env_file_frontend_service,  # noqa
            },
            check=True,
        )


@dataclasses.dataclass
class _RunMigrations:
    webapp_service_name: str
    name: str = "run DB migrations"

    def handle(self) -> None:
        print("Upgrading database...")
        run(
            shlex.split(
                f"docker exec {self.webapp_service_name} poetry run "
                f"arpav-ppcv db upgrade"
            ),
            check=True,
        )


@dataclasses.dataclass
class _RunLegacyMigrations:
    webapp_service_name: str
    name: str = "run legacy DB migrations"

    def handle(self) -> None:
        print("Upgrading legacy database...")
        run(
            shlex.split(
                f"docker exec {self.webapp_service_name} poetry run "
                f"arpav-ppcv django-admin migrate"
            ),
            check=True,
        )


@dataclasses.dataclass
class _CollectLegacyStaticFiles:
    webapp_service_name: str
    name: str = "collect legacy static files"

    def handle(self) -> None:
        print("Collecting legacy static files...")
        run(
            shlex.split(
                f"docker exec {self.webapp_service_name} poetry run "
                f"arpav-ppcv django-admin collectstatic --no-input"
            ),
            check=True,
        )


def perform_deployment(
    *, raw_request_payload: str, deployment_root: Path, confirmed: bool = False
):
    if not confirmed:
        print("Performing a dry-run")
    logger.info(f"{deployment_root=}")
    docker_dir = deployment_root / "docker"
    compose_files = (
        f"-f {docker_dir}/compose.yaml " f"-f {docker_dir}/compose.staging.yaml"
    )
    clone_destination = Path("/tmp/arpav-ppcv-backend")
    deployment_env_files = {
        "db_service": deployment_root / "environment-files/db-service.env",
        "legacy_db_service": deployment_root
        / "environment-files/legacy-db-service.env",
        "webapp_service": deployment_root / "environment-files/webapp-service.env",
        "frontend_service": deployment_root / "environment-files/frontend-service.env",
    }
    relevant_images = (
        "ghcr.io/geobeyond/arpav-ppcv-backend/arpav-ppcv-backend",
        "ghcr.io/geobeyond/arpav-ppcv/arpav-ppcv",
    )
    webapp_service_name = "arpav-ppcv-staging-webapp-1"
    deployment_steps = [
        _ValidateRequestPayload(raw_payload=raw_request_payload),
        _FindEnvFiles(env_files=deployment_env_files),
        _FindDockerDir(docker_dir=docker_dir),
        _StopCompose(docker_dir=docker_dir, compose_files_fragment=compose_files),
        _CloneRepo(clone_destination=clone_destination),
        _ReplaceDockerDir(repo_dir=clone_destination, docker_dir=docker_dir),
        _PullImage(images=relevant_images),
        _StartCompose(
            env_file_db_service=deployment_env_files["db_service"],
            env_file_legacy_db_service=deployment_env_files["legacy_db_service"],
            env_file_webapp_service=deployment_env_files["webapp_service"],
            env_file_frontend_service=deployment_env_files["frontend_service"],
            compose_files_fragment=compose_files,
        ),
        _RunMigrations(webapp_service_name=webapp_service_name),
        _RunLegacyMigrations(webapp_service_name=webapp_service_name),
        _CollectLegacyStaticFiles(webapp_service_name=webapp_service_name),
    ]
    for step in deployment_steps:
        print(f"Running step: {step.name!r}...")
        if confirmed:
            step.handle()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "deployment_root", help="Root directory of the deployment", type=Path
    )
    parser.add_argument("payload", help="Trigger request's body payload")
    parser.add_argument(
        "--confirm",
        action="store_true",
        help=(
            "Perform the actual deployment. If this is not provided the script runs "
            "in dry-run mode, just showing what steps would be performed"
        ),
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Turn on debug logging level",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING)
    try:
        perform_deployment(
            raw_request_payload=args.payload,
            deployment_root=args.deployment_root,
            confirmed=args.confirm,
        )
    except RuntimeError as err:
        raise SystemExit(err) from err
