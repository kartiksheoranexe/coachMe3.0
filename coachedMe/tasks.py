from celery import Celery
from celery import shared_task
from django.utils import timezone
from main.models import Coach

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@shared_task
# app = Celery('coachedMe')
# @app.task
def update_coach_years_of_experience():
    logger.info("Hello12")
 
    coaches = Coach.objects.all()
    logger.info(coaches)
    for coach in coaches:
        print("Hello!")
        # coach.years_of_experience += (timezone.now() - coach.updated_at).days / 365
        coach.years_of_experience += 1
        coach.save()
