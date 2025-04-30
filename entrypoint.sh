#!/bin/bash

set -e
echo ">> Running Migrations"
python manage.py migrate --noinput

echo ">> Collecting static files"
python manage.py collectstatic --noinput

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
