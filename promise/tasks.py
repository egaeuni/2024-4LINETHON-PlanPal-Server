from celery import shared_task
from django.utils import timezone
from .models import Promise

@shared_task
def update_promise_status():
    promises = Promise.objects.filter(
        status="created",
        created_at__lte=timezone.now() - timezone.timedelta(seconds=30) # hours=24
    )
    for promise in promises:
        promise.status = "confirming"
        promise.save()
