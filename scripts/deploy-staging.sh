# ARPAV-PPCV deployment script
#
# This script is to be run by the `webhook` server whenever there
# is a push to the arpav-ppcv-backend repository.
#

COMPOSE_FILES="-f docker/compose.yaml -f docker/compose.staging.yaml"

# actions to perform:

# 1. stop the current docker compose stack
docker compose "${COMPOSE_FILES}" down


# 2. remove the existing `docker` directory
rm -rf docker


# 3. clone the arpav-ppcv-backend repository from the geobeyond fork
git clone https://github.com/geobeyond/Arpav-PPCV-backend.git


# 4. copy the `docker` directory and delete the rest - we are deploying docker images, so no
#    need for the source code
cp Arpav-PPCV-backend/docker .
rm -rf Arpav-PPCV-backend


# 5. ensure the `$HOME/arpav-ppcv.env` exists, hopefully with correct values

# 6. pull the newer image(s) from the container registry
docker compose "${COMPOSE_FILES}" pull


# 7. start the compose stack again
docker compose "${COMPOSE_FILES}" up --force-recreate
