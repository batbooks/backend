#!/bin/bash

set -e  # اسکریپت رو در صورت ارور قطع کن

echo ">> Running Migrations"
python manage.py migrate --noinput

echo ">> Collecting static files"
python manage.py collectstatic --noinput

echo ">> Loading initial fixtures (optional)"
python run_fixture.py || echo "Fixtures not loaded!"

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
