# Project
Backend structure for suppot future climates indicators and models outputs web service pllatform.

# Structure

Docker services:
Django, PostGIS, Redis, Threeds.

# Create a custom project
Follow the naming conventions for python packages, generally lower case with underscores (_).
In the examples below, replace padoa-backend with whatever you would like to name your project.
No need for a Python virtual environment, the project runs using Docker 

- How to start your server using Docker

You need Docker or Docker-compose, get the latest stable official release for your platform.

Prepare the Environment

    git clone https://repositories.inkode.it/arpav/padoa-backend.git -b <your_branch>

Copy env.example in .evn and customize it with your local settings

Run docker-compose to start it up

    docker-compose build --no-cache
    docker-compose up -d

Preparation of the image:

    docker-compose up --build -d

Stop the Docker Images:

    docker-compose stop

Fully Wipe-out the Docker Images
WARNING: This will wipe out all the repositories created until now.
NOTE: The images must be stopped first

    docker system prune -a

Create a Super User to access the Django Admin interface:

    docker exec -ti backend.api python manage.py import_super_user

To create base layer attributes as Variables, Forecast models, Scenario e etc. Run:

    docker exec -ti backend.api python manage.py import_attributes

To collect all Municipalities (from the geojson) and define geographical boundaries:

    docker exec -ti backend.api python manage.py import_regions

Scanning selected Threeds folders and copying metadata:

    docker exec -ti backend.api python manage.py import_layers

Make migrations: 

    docker exec -ti backend.api python manage.py makemigrations

Migrate:

    docker exec -ti backend.api python manage.py migrate
