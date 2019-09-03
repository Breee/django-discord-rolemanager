#!/bin/sh

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start Celery.
celery -A pogobackend worker -l info &
celery -A pogobackend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &

# Start server
echo "Starting server"
gunicorn pogobackend.wsgi:application --bind 0.0.0.0:8000 --workers 3
