FROM ubuntu
LABEL Description="Tilemaker experiments" Version="1.0.0"
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /app
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
      build-essential \
      liblua5.1-0 \
      liblua5.1-0-dev \
      libprotobuf-dev \
      libsqlite3-dev \
      protobuf-compiler \
      shapelib \
      libshp-dev \
      libboost-program-options-dev \
      libboost-filesystem-dev \
      libboost-system-dev \
      libboost-iostreams-dev \
      rapidjson-dev \
      cmake git ca-certificates unzip

RUN git clone https://github.com/systemed/tilemaker.git --branch v2.2.0 --single-branch && \
    cd tilemaker && make && make install && cd /app

RUN mkdir -p landcover/ne_10m_urban_areas && cd landcover/ne_10m_urban_areas && \
	wget https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_urban_areas.zip && \
	unzip -o ne_10m_urban_areas.zip && cd ../.. && \
	mkdir -p landcover/ne_10m_antarctic_ice_shelves_polys && cd landcover/ne_10m_antarctic_ice_shelves_polys && \
	wget https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/ne_10m_antarctic_ice_shelves_polys.zip && \
	unzip -o ne_10m_antarctic_ice_shelves_polys.zip && cd ../.. && \
	mkdir -p landcover/ne_10m_glaciated_areas && cd landcover/ne_10m_glaciated_areas && \
	wget https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/ne_10m_glaciated_areas.zip && \
	unzip -o ne_10m_glaciated_areas.zip && cd ../.. && \
	mkdir -p coastline && cd coastline && \
	wget https://osmdata.openstreetmap.de/download/water-polygons-split-4326.zip && \
	unzip -o water-polygons-split-4326.zip && \
	mv water-polygons-split-4326/* . && cd /app

# TODO: delete when for real
ADD italy-latest.osm.pbf /app/italy-latest.osm.pbf

RUN tilemaker --input italy-latest.osm.pbf --output italy.mbtiles --config tilemaker/resources/config-openmaptiles.json --process tilemaker/resources/process-openmaptiles.lua

#RUN #apt update && apt install -y wget tilemaker