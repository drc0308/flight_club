#!/bin/sh

# I'm walking through a tutorial
# https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec python app.py
