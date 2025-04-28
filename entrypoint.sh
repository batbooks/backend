#!/bin/bash

python manage.py migrate --noinput

python manage.py collectstatic --noinput

exec gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --workers 4
