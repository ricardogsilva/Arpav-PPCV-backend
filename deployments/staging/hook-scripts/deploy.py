# ARPAV-PPCV deployment script
#
# This script is to be run by the `webhook` server whenever there
# is a push to the arpav-ppcv-backend repository.
#
# In order to simplify deployment, this script only uses stuff from the Python
# standard library.

import shlex
import shutil
import sys
from pathlib import Path
from subprocess import run

def perform_deployment():
    deployment_root_dir = Path("/home/arpav")
    if (docker_dir := deployment_root_dir / "docker").is_dir():
        _compose_files_fragment = (
            f"-f {docker_dir}/compose.yaml "
            f"-f {docker_dir}/compose.staging.yaml"
        )
        # 1. stop the current docker compose stack
        print("Stopping docker compose stack...")
        # run(shlex.split(f"docker compose {_compose_files_fragment} down"), check=True)

        # 2. remove the existing `docker` directory
        print(f"Removing {docker_dir!r}...")
        # shutil.rmtree(str(docker_dir), ignore_errors=True)

        # 3. clone the arpav-ppcv-backend repository from the geobeyond fork
        print("Cloning repo...")
        # run(
        #     shlex.split(
        #         "git clone https://github.com/geobeyond/Arpav-PPCV-backend.git"),
        #     check=True,
        # )

        # 4. copy the `docker` directory and delete the rest - we are deploying docker
        #    images, so no need for the source code
        repo_docker_dir = Path.cwd() / "Arpav-PPCV-backend/docker"
        print(
            f"Copying the docker dir in {repo_docker_dir!r} "
            f"to {docker_dir!r}..."
        )
        # shutil.copytree(repo_docker_dir, docker_dir)

        # 5. ensure the `$HOME/arpav-ppcv.env` exists, hopefully with correct values
        print("Looking for env_file...")
        # if not (env_file := (Path.home() /"arpav-ppcv.env")).exists():
        #     raise RuntimeError(f"Could not find environment file {env_file!r}, aborting...")

        # 6. pull the newer image(s) from the container registry
        print("Pulling updated docker images...")
        # run(shlex.split(f"docker compose {_compose_files_fragment} pull"), check=True)

        # 7. start the compose stack again
        print("Restating the docker compose stack...")
        # run(
        #     shlex.split(
        #         f"docker compose {_compose_files_fragment} up --detach "
        #         f"--force-recreate"
        #     ),
        #     check=True
        # )
    else:
        raise RuntimeError(
            f"Could not find directory {str(docker_dir)!r}, aborting execution...")


if __name__ == "__main__":
    raw_payload, raw_headers, raw_query_params = sys.argv[1:]
    # TODO: check the content of the request in order to make sure we should
    #       redeploy
    print("Deploying...")
    try:
        perform_deployment()
    except RuntimeError as err:
        raise SystemExit(err) from err
