from celery import shared_task
from django.utils import timezone
from .models import Plan
from notifications.models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@shared_task
def check_plan_deadlines():
    now = timezone.now().astimezone(timezone.get_current_timezone())
    plans = Plan.objects.filter(is_completed=False)
    
    for plan in plans:
        plan_end = plan.end.astimezone(timezone.get_current_timezone())
        deadline = plan_end - now

        if deadline <= timezone.timedelta(hours=1) and not plan.is_completed:
            Notification.objects.create(
                recipient=plan.author,
                message=f"{plan.title} 마감시간까지 1시간 남았습니다! 잊지 말고 계획을 실행해주세요!",
                notification_type='plan_deadline'
        )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{plan.author.id}", 
                {
                    "type": "send_notification",
                    "message": f"{plan.title} 마감시간까지 1시간 남았습니다! 잊지 말고 계획을 실행해주세요!"
                }
            )