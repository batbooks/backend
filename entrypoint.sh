#!/bin/bash

# انجام مایگریشن
python manage.py migrate --noinput || { echo 'Migration failed!'; exit 1; }

# جمع‌آوری فایل‌های استاتیک
python manage.py collectstatic --noinput || { echo 'Collectstatic failed!'; exit 1; }

# شروع gunicorn
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
