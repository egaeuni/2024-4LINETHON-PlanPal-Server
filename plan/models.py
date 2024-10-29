from django.db import models
from users.models import  Profile

# Create your models here.
class Category(models.Model):
    COLOR_CHOICES = [
        ("#FF6A3B", "Orange"),
        ("#4076BA", "Blue"),
        ("#C04277", "Pink"),
        ("#16857A", "Green"),
        ("#A97C50", "Brown"),
    ]
    
    title = models.CharField(max_length=30, unique=True)
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default="#FF6A3B")
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Plan(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='plans')
    title = models.CharField(max_length=30)
    category = models.ManyToManyField(to=Category, through="PlanCategory", related_name="plans")
    start = models.DateTimeField()
    end = models.DateTimeField()
    memo = models.TextField(blank=True, null=True)
    participant = models.ManyToManyField("users.Profile", related_name="participating_plan", blank=True)

    def __str__(self):
        return self.title

class PlanCategory(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('plan', 'category')