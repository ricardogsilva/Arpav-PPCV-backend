# Project
Backend structure for suppot future climates indicators and models outputs web service pllatform.

# struture
- Docker services:
python, django, postgis, 


Create a custom project
Follow the naming conventions for python packages (generally lower case with underscores (_).
In the examples below, replace padoa-backend with whatever you would like to name your project.

No need for a Python virtual environment, the project runs using Docker 

# How to start your server using Docker

You need Docker or Docker-compose XXXXXversion or higher, get the latest stable official release for your platform.

Prepare the Environment
git clone https://repositories.inkode.it/arpav/padoa-backend.git -b <your_branch>
copy env.example and customize it


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

Make migrations: 

    docker exec -ti backend.api python manage.py makemigrations

Migrate:

    docker exec -ti backend.api python manage.py migrate



