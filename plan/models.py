from django.db import models
from users.models import  Profile
from django.contrib.auth import get_user_model

from promise.models import Promise

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification

User = get_user_model()

class Category(models.Model):
    COLOR_CHOICES = [
        ("#FF6A3B", "Orange"),
        ("#4076BA", "Blue"),
        ("#C04277", "Pink"),
        ("#16857A", "Green"),
        ("#A97C50", "Brown"),
    ]
    
    title = models.CharField(max_length=30) # unique = True 제거 : 약속 카테고리 때문에 !
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default="#FF6A3B")
    is_public = models.BooleanField(default=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Plan(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')
    title = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="plans", blank=True, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    memo = models.TextField(blank=True, null=True)
    participant = models.ManyToManyField("users.Profile", related_name="participating_plan", blank=True)
    is_completed = models.BooleanField(default=False)

    # 약속으로 생성된 Plan인 경우 promise를 참조하도록
    promise = models.ForeignKey(Promise, on_delete=models.CASCADE, related_name='promise_creates_this_plan', null=True)

    def __str__(self):
        return self.title

class PlanCategory(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)