from celery import Celery
from celery import shared_task
from django.utils import timezone
from main.models import Coach
from django.http import JsonResponse

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@shared_task
def update_coach_years_of_experience():
    try:
        coaches = Coach.objects.all()
        for coach in coaches:
            coach.years_of_experience += 1.0
            coach.save()
    except Exception as e:
        logger.error("Error connecting to database: {}".format(e))


