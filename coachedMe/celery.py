from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('celery.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

# from tasks import update_coach_years_of_experience
from celery import Celery
# from celery.schedules import crontab

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coachedMe.settings')

app = Celery('coachedMe')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'update_coach_years_of_experience': {
        'task': 'tasks.update_coach_years_of_experience',
        'schedule': timedelta(seconds=15),
    },
}