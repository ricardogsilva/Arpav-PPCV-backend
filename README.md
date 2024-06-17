# Backend - Piattaforma Proiezioni Climatiche per il Nord-Est

{Intro - about}

This repository contains the source code for the backend components of the ARPAV-PPCV platform.

Its main goal is to serve climate-related data in the form of both historical observations and forecast models.

Briefly, the backend component is a web application that serves an OpenAPI API that is consumed by the frontend.
It contains some additional services, which are used to support it and provide additional functionality, namely:

- a vector tile server
- The integration with ARPA's THREDDS server, which is used for tasks related to model data (WMS service, download of
  NetCDF files, data subsetting for time series visualizations)

The main application is launched by maeans of a custom CLI command. This CLI additionally provides a multitude of
maintenance commands, such as upgrading the database schema, refreshing historical observations data, etc.

This component is implemented in Python, using these main libraries and frameworks:

- starlette
- starlette_admin
- FastAPI
- pydantic
- htmx
- sqlalchemy
- geoalchemy2
- shapely


### Installation

The primary means of installing the various backend components is by using docker compose. Use the `compose.*` files
provided in the `docker` directory.

For example, for development:

```shell
docker compose -f docker/compose.yaml -f compose.dev.yaml up -d
```

Standing up the various components without docker is also possible, check out the compose file for how to do it. The
main web application uses poetry, so installing it is just a matter of doing `poetry install`.


### Configuration

This application is configured via environment variables. By defaul all settings are prefixed with `ARPAV_PPCV__`, but
this can also be modified if needed. The system recognizes the following environment variables:

- `ARPAV_PPCV__DEBUG` - (bool - `False`) Whether the application runs in debug mode or not. Debug mode outputs more logging
  information and can be slower. Additionally, it may leak sensitive data to the console. Use it only during development
- `ARPAV_PPCV__BIND_HOST` - (str - `"127.0.0.1"`) Which host is allowed to make requests to the web application server.
  When running under docker, be sure to set this to allow all hosts (`*`).
- `ARPAV_PPCV__BIND_PORT` - (int - `5001`) Which port is the web application server accepting requests on.
- `ARPAV_PPCV__PUBLIC_URL` - (str - `"http://localhost:5001"`) The public URL of the web application.
- `ARPAV_PPCV__DB_DSN` - (pydantic.PostgresDsn - `"postgresql://user:password@localhost:5432/arpav_ppcv"`) Connection
  string to be used for accessing the backend database. This application only works with postgresql as the DB server.
- `ARPAV_PPCV__TEST_DB_DSN` - (pydantic.PostgresDsn - `None`) Connection string used to connect to the test database.
  This is only needed for running the tests.
- `ARPAV_PPCV__VERBOSE_DB_LOGS` - (bool - `False`) Whether to output verbose logs related to database-related commands.
  Use this only in development, as it will slow down the system.
- `ARPAV_PPCV__CONTACT__NAME` - (str - `"info@geobeyond.it"`)
- `ARPAV_PPCV__CONTACT__URL` - (str - `"http://geobeyond.it"`)
- `ARPAV_PPCV__CONTACT__EMAIL` - (str - `"info@geobeyond.it"`)
- `ARPAV_PPCV__TEMPLATES_DIR` - (Path - `"webapp/templates"`) Where to store custom templates. This is mainly useful
  for development, so avoid modifying it.
- `ARPAV_PPCV__STATIC_DIR` - (Path - `"webapp/static"`) Where to store static files. This is mainly useful for
  development, so avoid modifying it.
- `ARPAV_PPCV__THREDDS_SERVER__BASE_URL` - (str - `"http://localhost:8080/thredds"`) Base URL of the THREDDS server
- `ARPAV_PPCV__THREDDS_SERVER__WMS_SERVICE_URL_FRAGMENT` - (str - `"wms"`) URL fragment used by the THREDDS server's
  WMS service. This is mainly useful for development, so avoid modifying it.
- `ARPAV_PPCV__THREDDS_SERVER__NETCDF_SUBSET_SERVICE_URL_FRAGMENT` - (str - `"ncss/grid"`) URL fragment used by the
  THREDDS server's NetCDF subset service. This is mainly useful for development, so avoid modifying it.
- `ARPAV_PPCV__THREDDS_SERVER__UNCERTAINTY_VISUALIZATION_SCALE_RANGE` - (tuple[float, float] - `(0, 9)`) - Min, max
  values for the uncertainty pattern used in the WMS uncertainty visualization display.

- `ARPAV_PPCV__MARTIN_TILE_SERVER_BASE_URL` - (str - "http://localhost:3000") Base URL of the Martin vector tile server.
- `ARPAV_PPCV__NEAREST_STATION_RADIUS_METERS` - (int - 10_000) Distance to use when looking for the nearest
  observation station.
- `ARPAV_PPCV__V1_API_MOUNT_PREFIX` - (str - "/api/v1") URL prefix of the legacy API. Do not modify this unless you
  know what you are doing, as other parts of the system rely on it.
- `ARPAV_PPCV__V2_API_MOUNT_PREFIX` - (str - "/api/v2") URL prefix of the web application API. Do not modify this unless
  you know what you are doing, as other parts of the system rely on it.

- `ARPAV_PPCV__DJANGO_APP`: DjangoAppSettings = DjangoAppSettings()

- `ARPAV_PPCV__LOG_CONFIG_FILE`: Path | None = None
- `ARPAV_PPCV__SESSION_SECRET_KEY`: str = "changeme"

- `ARPAV_PPCV__ADMIN_USER`: AdminUserSettings = AdminUserSettings()

- `ARPAV_PPCV__CORS_ORIGINS`: list[str] = []
- `ARPAV_PPCV__CORS_METHODS`: list[str] = []
- `ARPAV_PPCV__ALLOW_CORS_CREDENTIALS`: bool = False


### Operations

##### Accessing the CLI
##### Accessing the web API
##### Using the web admin

### Deployment

### Testing



#### Climate Projections Platform for North-Eastern Italy - Backend structure for support future climates indicators and models outputs web service platform
[![Piattaforma Proiezioni Climatiche per il Nord-Est](https://github.com/inkode-it/Arpav-PPCV/raw/main/public/img/screenshot.png)](https://clima.arpa.veneto.it/)

## About
This work is licensed under a <a rel="license" href="https://creativecommons.org/licenses/by-sa/3.0/it/deed.en">Creative Commons Attribution-ShareAlike 3.0 IT License</a>.
<br/><a rel="license" href="https://creativecommons.org/licenses/by-sa/3.0/it/deed.en"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/3.0/88x31.png" /></a>

Commissioned by & Data credits to <br/>
<a href="https://www.arpa.veneto.it/"><img src="https://github.com/inkode-it/Arpav-PPCV/raw/main/public/img/logo_arpav.png" alt="ARPAV" style="background-color:white;padding:4px"></a>

Designed and developed in Italy by <br/>
<a rel="author" href="mailto:info@inkode.it"><img src="https://avatars.githubusercontent.com/u/64135645" alt="INKODE soc coop"></a>


## Structure: Docker services
### Django
Django, Django Rest Framework (DRF), and GeoDjango are used together to build web applications that require geospatial data processing and API development.

Django is a popular web framework for building Python-based web applications. It provides a lot of built-in features, such as an ORM for database interactions, a templating engine, and a powerful admin interface, which can speed up development time.

DRF is a Django package that provides tools for building RESTful APIs. It extends Django's built-in views and serializers to provide a more flexible and powerful way of building APIs. DRF is widely used to build APIs for web and mobile applications.

GeoDjango is a Django package that adds support for geospatial data processing to Django. It allows developers to store, retrieve, and process geospatial data in the context of a Django application. GeoDjango provides many GIS-related tools, such as spatial indexing, geographic data models, and geospatial functions.

By combining Django, DRF, and GeoDjango, developers can build web applications that can store, process, and serve geospatial data through RESTful APIs. This can be useful for a variety of applications, such as mapping services, location-based services, and data visualization tools that require geospatial data processing.

In this application, Django framework and packages are used to:

- provide REST APIs to the frontend
- scan NetCDF files provided by Thredds and handle the attributes of climate projection models.

Root directory: `backend`

#### PostGIS
PostGIS is a spatial database extender for the PostgreSQL relational database management system. It allows you to store, query, and manipulate spatial data such as points, lines, and polygons, as well as geospatial data formats such as GeoJSON and KML. PostGIS adds support for geographic objects, allowing spatial queries to be run in SQL. It provides a wide range of spatial functions and operators for performing geometric operations such as intersection, union, and buffering, as well as distance calculations and projections. PostGIS is widely used in geographic information systems (GIS), web mapping applications, and other spatially enabled applications. It is an open-source project and is actively developed and maintained by a community of developers around the world.

In this application, PostGIS is used to query all available climate projections, manage administrative users, and geographic locations.

#### Nginx
Nginx (pronounced "engine-x") is a high-performance, open-source web server and reverse proxy server. It is designed to handle large amounts of traffic and to act as a load balancer for web applications. Nginx can serve static files quickly and efficiently, and also supports dynamic content generated by backend applications such as PHP, Python, and Node.js. In addition to its role as a web server, Nginx can also be used as a reverse proxy, which allows it to distribute incoming traffic among multiple backend servers, improve the reliability and scalability of web applications, and provide additional security features such as SSL/TLS encryption and HTTP authentication. Nginx is free and open-source software, and its development is supported by Nginx, Inc. and a community of developers around the world.

In this application, Nginx is used as a proxy-pass for other web services.

Config directory: `docker/nginx`

#### NodeJS (proxy Thredds Data Server)
A NodeJs server-side proxy application can be used to perform a variety of tasks, such as load balancing, caching, and security filtering. For example, a load-balancing proxy can distribute incoming requests among multiple backend servers, improving the scalability and availability of web applications. A caching proxy can store frequently accessed data in memory or on disk, reducing the load on backend servers and improving the performance of web applications. A security filtering proxy can inspect incoming requests and filter out potentially harmful requests or data, protecting web applications from attacks. Node.js is a popular platform for building proxy servers due to its event-driven, non-blocking I/O model, which allows it to handle large numbers of concurrent connections efficiently,

In this application it acts as an intermediary between clients and Thredds Data Server servers, allowing users to access a subset of THREDDS data and services without authentication. It receives requests from clients and forwards them to Thredds Data Server, and then sends the response back to the client.

Root directory: `backend`

#### Martin
Martin Vector Tile Server is an open-source vector tile server that allows users to serve vector tiles over the web. It is built for MapLibre, an open-source JavaScript library for interactive maps, and supports a variety of data sources, including GeoJSON, PostGIS, and Shapefile.

# Development

GIT BRANCH: `develop`

#### Required tools for development

For development on your local machine, you need to install the following tools:
   - git
   - docker
   - docker-compose -f docker-compose.dev.yml
   - a text editor or an IDE (Eg. Visual Studio Code)


#### Prepare the Environment

Starting from the root of the project, clone the backend repository, move on `develop` branch and clone frontend repository inside this project


    git clone https://github.com/inkode-it/Arpav-PPCV-backend
    cd Arpav-PPCV-backend
    git checkout develop
    git clone https://github.com/inkode-it/Arpav-PPCV

#### Copy `.env.example` in `.env` and **customize it with your local settings** both for the backend and the frontend.

NOTE: `.env`'s file are used to set the environment variables for the docker-compose -f docker-compose.dev.yml file and the running services, to configure the backend and frontend services, the PostGIS database, Nginx web server etc..


#### For Frontend `Arpav-PPCV`, follow the instructions in the *frontend README.md file to start the frontend*

NOTE: Both `Arpav-PPCV-backend` & `Arpav-PPCV` (the frontend) have a different .env file configuration with different variables


#### Run docker-compose to start it up


    docker-compose -f docker-compose.dev.yml build --no-cache
    docker-compose -f docker-compose.dev.yml up -d


#### Build images & start containers:

    docker-compose -f docker-compose.dev.yml up --build -d


#### Make django migrations:

    docker exec -ti backend.api python manage.py makemigrations users groups forecastattributes places thredds

#### Migrate database:

    docker exec -ti backend.api python manage.py migrate


#### Create a Super User to access the Django Admin interface:

    docker exec -ti backend.api python manage.py import_super_user

NOTE: this super user is intended for development in local environment, default credential are:
- username: `info@inkode.it`
- password: `inkode`


#### To create base layer attributes as Variables, Forecast models, Scenario e etc. Run:

    docker exec -ti backend.api python manage.py import_attributes


#### To collect all Municipalities (from the geojson) and define geographical boundaries:

     docker exec -ti backend.api python manage.py import_regions


#### Scanning selected Threeds folders and copying metadata:

    docker exec -ti backend.api python manage.py import_layers

NOTES:
- to update already imported layers, run the command with the `--refresh` flag
- to fully clean layers and & re-import them, run the command with the `--destroy` flag


If everything is ok and you followed also frontend README instructions, you should be able to access:
- the frontend at http://localhost:3000
- the backend administration at http://localhost/admin


## PRODUCTION USAGE

#### Clean build & start containers


    docker-compose build --no-cache
    docker-compose up -d


#### Build images & start containers:

    docker-compose up --build -d


#### Make django migrations:

    docker exec -ti backend.api python manage.py makemigrations users groups forecastattributes places thredds


#### Migrate database:

    docker exec -ti backend.api python manage.py migrate


#### Create a Super User to access the Django Admin interface:

    docker exec -ti backend.api python manage.py createsuperuser

NOTE: prompt for username, email, password


#### To create base layer attributes as Variables, Forecast models, Scenario e etc. Run:

    docker exec -ti backend.api python manage.py import_attributes


#### To collect all Municipalities (from the geojson) and define geographical boundaries:

     docker exec -ti backend.api python manage.py import_regions


#### Scanning selected Threeds folders and copying metadata:

    docker exec -ti backend.api python manage.py import_layers


#### Re-build & deploy frontend:

    cd ~/Arpav-PPCV-backend/Arpav-PPCV/;git pull;cd ..;docker-compose build frontend;docker-compose up -d

NOTES:
- to update already imported layers, run the command with the `--refresh` flag
- to fully clean layers and & re-import them, run the command with the `--destroy` flag


#### Stop & destroy containers (note using `-v` will remove the volumes)

docker-compose -f docker-compose.dev.yml down

#### SSL certificates

SSL certificate are mounted in the nginx container as a volume. The certificate files and the private key should be placed on paths listed on .env file by envars `SSL_CERTIFICATE` and `SSL_KEY`, note that certificate needs to be bundled with the full chain.
