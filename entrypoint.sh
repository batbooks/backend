#!/bin/bash

set -e
chown -R appuser:appuser /app/media

echo ">> Running Migrations"
python manage.py migrate --noinput

echo ">> Collecting static files"
python manage.py collectstatic --noinput

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
