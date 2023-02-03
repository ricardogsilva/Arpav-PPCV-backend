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

## Procedure

1) Prepare the Environment


    git clone https://github.com/inkode-it/Arpav-PPCV-backend`


2) Copy `env.example` in `.env` and customize it with your local settings


3) Clone the Frontend repository inside this project and follow the instructions in the README.md file to start the frontend


    `git clone https://github.com/inkode-it/Arpav-PPCV`


4) Run docker-compose to start it up

    ```shell
    docker-compose build --no-cache
    docker-compose up -d
    ```    

5) Build images & start containers:

    `docker-compose up --build -d`


6) Make django migrations: 

    `docker exec -ti backend.api python manage.py makemigrations`


7) Migrate database:

    `docker exec -ti backend.api python manage.py migrate`


8) Create a Super User to access the Django Admin interface:

    `docker exec -ti backend.api python manage.py import_super_user`


9) To create base layer attributes as Variables, Forecast models, Scenario e etc. Run:

    `docker exec -ti backend.api python manage.py import_attributes`


10) To collect all Municipalities (from the geojson) and define geographical boundaries:

     `docker exec -ti backend.api python manage.py import_regions`


11) Scanning selected Threeds folders and copying metadata:

    `docker exec -ti backend.api python manage.py import_layers`


12) Stop & destroy containers (note using `-v` will remove the volumes)

    `docker-compose down`
