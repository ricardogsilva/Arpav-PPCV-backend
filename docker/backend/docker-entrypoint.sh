#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
# http://stackoverflow.com/questions/19622198/what-does-set-e-mean-in-a-bash-script
set -e
# Check if the required PostgreSQL environment variables are set

# Used by docker-entrypoint.sh to start the dev server
# If not configured you'll receive this: CommandError: "0.0.0.0:" is not a valid port number or address:port pair.
#[ -z "$PORT" ] && echo "ERROR: Need to set PORT. E.g.: 8000" && exit 1;

#[ -z "$POSTGRES_DB_NAME" ] && echo "ERROR: Need to set POSTGRES_DB_NAME" && exit 1;
#[ -z "$POSTGRES_USER" ] && echo "ERROR: Need to set POSTGRES_USER" && exit 1;
#[ -z "$PGPASSWORD" ] && echo "ERROR: Need to set POSTGRES_PASSWORD" && exit 1;


# Define help message
show_help() {
    echo """
        Usage: docker run <imagename> COMMAND
        Commands
        dev      : Start a normal Django development server
        bash     : Start a bash shell
        manage   : Start manage.py
        setup_db : Setup the initial database. Configure \$POSTGRES_DB_NAME in docker-compose.yml
        pip      : Run pip
        lint     : Run pylint
        python   : Run a python command
        shell    : Start a Django Python shell
        uwsgi    : Run uwsgi server
        help     : Show this message
        """
}

write_uwsgi() {
    echo "Generating uwsgi config file..."
    snippet="import os;
        import sys;
        import jinja2;
        sys.stdout.write(jinja2.Template(sys.stdin.read()).render(env=os.environ))"

    cat /deployment/uwsgi.ini | python -c "${snippet}" > /uwsgi.ini
}

# Run
until ls $DJANGO_HOME
do
    echo "Waiting for django volume..."
done

if [ ! -f $DJANGO_HOME/.env ]; then
   touch $DJANGO_HOME/.env
fi

if [ ! -d $DJANGO_HOME/storage ]; then
   mkdir $DJANGO_HOME/storage
fi

if [ ! -d $DJANGO_HOME/static ]; then
   mkdir $DJANGO_HOME/static
fi

#echo "fix file and folder permissions"
#find $DJANGO_HOME -type f | xargs chmod -v 644
#find $DJANGO_HOME -type d | xargs chmod -v 755
#chmod -R 777 $DJANGO_HOME/storage
#chmod +x $DJANGO_HOME/manage.py

until python ../check_db.py --service-name Postgres --ip ${POSTGRES_PORT_5432_TCP_ADDR:-postgis} --port ${POSTGRES_PORT_5432_TCP_PORT:-5432}
do
  echo "Waiting for postgres server"
  sleep 2
done

echo "=== RUNNING COMMAND $1 ==="

case "$1" in
    dev)
        if [ ! -f $DJANGO_HOME/storage/.migrated ]; then
            touch $DJANGO_HOME/storage/.migrated
            echo "Running migrations first"
            $WORK_DIR/docker-entrypoint.sh setup_db
        fi
        echo "Running Development Server on ${BIND_HOST}:${PORT}"
        python $DJANGO_HOME/manage.py runserver ${BIND_HOST}:${PORT}
    ;;
    bash)
        /bin/bash "${@:2}"
    ;;
    manage)
        python $DJANGO_HOME/manage.py "${@:2}"
    ;;
    setup_db)
        #psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'my_db'" | grep -q 1 || psql -U postgres -c "CREATE DATABASE my_db"
        #psql -h $POSTGRES_PORT_5432_TCP_ADDR -U $PGPASSWORD -c "CREATE DATABASE $POSTGRES_DB_NAME"
        python $DJANGO_HOME/manage.py reset_db --noinput --close-sessions
        python $DJANGO_HOME/manage.py makemigrations
        python $DJANGO_HOME/manage.py migrate
        python $DJANGO_HOME/manage.py import_super_user
        #python $DJANGO_HOME/manage.py load_goup_and_permissions
    ;;
    lint)
        pylint "${@:2}"
    ;;
    python)
        python "${@:2}"
    ;;
    pip)
        pip "${@:2}"
    ;;
    shell)
        python $DJANGO_HOME/manage.py shell_plus
    ;;
    gunicorn)
        if [ ! -f $DJANGO_HOME/storage/.migrated ]; then
            touch $DJANGO_HOME/storage/.migrated
            echo "Running migrations first"
            $WORK_DIR/docker-entrypoint.sh setup_db
        fi
        python $DJANGO_HOME/manage.py collectstatic --noinput
        echo "Running App (gunicorn) on ${BIND_HOST}:${PORT}"
        gunicorn $DJANGO_PROJECT_NAME.wsgi:application \
            --name $DJANGO_PROJECT_NAME \
            --bind ${BIND_HOST}:${PORT} \
            --workers ${GUNICORN_WORKERS} \
            --log-level=${GUNICORN_LOG_LEVEL} \
            --log-file=${GUNICORN_LOG_FILE} \
            --access-logfile=${GUNICORN_ACCESS_LOG_FILE}
    ;;
    daphne)
        python $DJANGO_HOME/manage.py collectstatic --noinput
        echo "Running App (daphne) on ${BIND_HOST}:${PORT}"
        daphne -b ${BIND_HOST} -p $PORT $DJANGO_PROJECT_NAME.asgi:application
    ;;
    worker)
        echo "Running App (worker)for ${@:2}"
        python $DJANGO_HOME/manage.py runworker "${@:2}"
    ;;
    celerybeat)
        rm -f ${CELERYBEAT_PID_FILE}
        echo "Running App (celery)..."
        celery beat -A ${DJANGO_PROJECT_NAME} --pidfile=${CELERYBEAT_PID_FILE} --loglevel=${CELERYD_LOG_LEVEL} -s ${CELERYBEAT_SCHEDULE_FILE} --logfile=${CELERYD_LOG_FILE}
    ;;
    celeryworker)
        rm -f ${CELERYD_PID_FILE}
        echo "Running App (celery)..."
        celery worker -A ${DJANGO_PROJECT_NAME} --pidfile=${CELERYD_PID_FILE} --loglevel=${CELERYD_LOG_LEVEL} --logfile=${CELERYD_LOG_FILE} --time-limit=$CELERYD_TIMELIMIT --concurrency=$CELERYD_CONCURRENCY
    ;;
    *)
        show_help
    ;;
esac
