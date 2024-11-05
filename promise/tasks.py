from celery import shared_task
from django.utils import timezone
from .models import Promise
from .views.VotingView import is24HoursAfter

@shared_task
def update_promise_status():
    is24HoursAfter()
