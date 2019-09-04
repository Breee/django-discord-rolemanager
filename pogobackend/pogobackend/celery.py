from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from django.core.management import call_command

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pogobackend.settings')
app = Celery('pogobackend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(name='update_user_task', bind=True)
def update_user(self, user_id):
    try:
        call_command('update_user', user_id)
    except RuntimeError as e:
        print(e)
        self.retry(countdown=2, exc=e, max_retries=5)


@app.task(name='subtract_day')
def subtract_day():
    call_command('subtract_day')

@app.task(name='subtract_fee')
def subtract_fee(user_id=None):
    if user_id:
        call_command('subtract_fee', '--pay', '--days', '--month', f'--user={user_id}')
    else:
        call_command('subtract_fee', '--pay', '--days', '--month')

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))