from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.devl")

app = Celery('backend')

CELERY_TIMEZONE = 'UTC'

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)