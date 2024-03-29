from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import dotenv
from celery.schedules import crontab
from django.conf import settings

# dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ.get("DJANGO_SETTINGS_MODULE", "djangoapp.settings"))

# app = Celery('seagrid-celery')
app = Celery('docker-celery', backend="redis", broker="redis://localhost:6379")

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)

def debug_task(self):
  print('Request: {0!r}'.format(self.request))


'''
  VERIFICARE POSSIBILITA' http://docs.celeryproject.org/en/latest/userguide/tasks.html#task-naming-relative-imports
'''
app.conf.beat_schedule = {

    # 'add-every-60-seconds': {
    #     'task': 'say_hello',
    #     'schedule': 60.0,
    #     'args': ("Giorgio",)
    # },
}
