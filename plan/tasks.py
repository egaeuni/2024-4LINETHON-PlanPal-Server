from celery import shared_task
from django.utils import timezone
from .models import Plan, Notification
from .views import PlanViewSet
@shared_task
def update_plan_status():
    plan_deadline()
    daily_achievement()