from django.db import models
from users.models import Profile

# Create your models here.

class PromiseOption(models.Model):
    # 일정이 가능한 사람들
    members_can_attend = models.ManyToManyField(Profile, related_name="participants_of_promise_options")
    # 투표한 사람들
    vote_members = models.ManyToManyField(Profile, related_name="voted_promise_options")

    title = models.CharField(max_length=30)
    start = models.DateTimeField()
    end = models.DateTimeField()
    length = models.IntegerField()

class Promise(models.Model):
    STATUS_CHOICES = [
        ("created", "created"),
        ("voting", "voting"),
        ("confirming", "confirming"),
        ("completed", "completed")
    ]
    
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    members = models.ManyToManyField(Profile, related_name="promises")
    accept_members = models.ManyToManyField(Profile, related_name="promises_accept")
    reject_members = models.ManyToManyField(Profile, related_name="promises_reject")
    
    title = models.CharField(max_length=30)
    start = models.DateTimeField()
    end = models.DateTimeField()
    length = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="created")

    promise_options = models.ManyToManyField(PromiseOption, related_name='promises', blank=True)

class Memo(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(max_length=30)
    promise = models.ForeignKey(Promise, on_delete=models.CASCADE, related_name='memos')

class Mark(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    promise = models.ForeignKey(Promise, on_delete=models.CASCADE, related_name='mark')