FROM python:3

ENV DJANGO_PROJECT_NAME djangoapp
ENV WORK_DIR /opt/api
ENV DJANGO_HOME $WORK_DIR/app
ENV BIND_HOST 0.0.0.0
ENV PORT 8000

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE $DJANGO_PROJECT_NAME.settings
ENV ASGI_APPLICATION $DJANGO_PROJECT_NAME.asgi.application
ENV WSGI_APPLICATION $DJANGO_PROJECT_NAME.routing.application

ENV CELERYD_PID_FILE $DJANGO_HOME/daemons/celery.pid
ENV CELERYBEAT_PID_FILE $DJANGO_HOME/daemons/celery.beat.pid
ENV CELERYBEAT_SCHEDULE_FILE $DJANGO_HOME/daemons/celerybeat-schedule
ENV CELERYD_LOG_LEVEL INFO
ENV CELERYD_LOG_FILE $DJANGO_HOME/daemons/celery.log
ENV CELERYD_TIMELIMIT 7200
ENV CELERYD_CONCURRENCY 1

ENV GUNICORN_LOG_LEVEL info
ENV GUNICORN_LOG_FILE -
ENV GUNICORN_ACCESS_LOG_FILE -
ENV GUNICORN_WORKERS 5

ENV CHANNEL_WORKER_THREADS 2

# Install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    jq gdal-bin apt-utils libgdal-dev sqlite3

# Install proj 7 (mimimum supported version by pyproj is 6.2.0 - Buster provides 5.2.0

RUN cd /tmp && \
    wget https://github.com/OSGeo/PROJ/releases/download/9.1.0/proj-9.1.0.tar.gz && \
    tar -xf proj-9.1.0.tar.gz && \
    cd proj-9.1.0 && apt install cmake -y && mkdir build && cd build && cmake .. && cmake --build . && cmake --build . --target install

# create folders and set properties
RUN mkdir $WORK_DIR \
    && mkdir $DJANGO_HOME \
    && mkdir $DJANGO_HOME/storage \
    && mkdir $DJANGO_HOME/static

# Add django entrypoint
ADD docker/backend/docker-entrypoint.sh $WORK_DIR/docker-entrypoint.sh
RUN chmod +x ${WORK_DIR}/docker-entrypoint.sh
ADD check_db.py $WORK_DIR/check_db.py
RUN chmod +x ${WORK_DIR}/check_db.py

# install python dependencies
ADD docker/backend/project_requirements.txt $WORK_DIR/project_requirements.txt
RUN apt install -y postgresql-client && pip install --upgrade pip && pip install -r $WORK_DIR/project_requirements.txt && chmod +x $WORK_DIR/docker-entrypoint.sh
# copy default django folder

COPY backend $DJANGO_HOME
# correct file and folder permissionsok
RUN find $DJANGO_HOME -type f | xargs chmod -v 644 \
    && find $DJANGO_HOME -type d | xargs chmod -v 755 \
    && chmod -R 777 $DJANGO_HOME/storage \
    && chmod +x $DJANGO_HOME/manage.py

# set workdir
WORKDIR $DJANGO_HOME

#set user
#USER $DJANGO_PROJECT_NAME

# expose port
EXPOSE $PORT

ENTRYPOINT ["../docker-entrypoint.sh"]
# Run daphne
CMD ["daphne"]



