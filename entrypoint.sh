#!/bin/bash

set -e
chown -R appuser:appuser /app/media

echo ">> Running Migrations"
python manage.py migrate --noinput

echo ">> Collecting static files"
python manage.py collectstatic --noinput

exec su appuser -c "gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --max-requests 1000 --max-requests-jitter 50"

