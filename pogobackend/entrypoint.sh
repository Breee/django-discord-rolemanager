#!/bin/sh

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Remove old celerybeat.pid
rm celerybeat.pid
# Start Celery.
celery -A pogobackend worker -l info &
celery -A pogobackend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &

# Start server
echo "Starting server"
if [ "$DEVELOPMENT" == "True" ]
then
  python3 manage.py runserver 0.0.0.0:8000
else
  gunicorn pogobackend.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi