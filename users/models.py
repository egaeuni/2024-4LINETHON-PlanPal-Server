from django.db import models
import os
from uuid import uuid4
from django.utils import timezone

def upload_filepath(instance, filename):
    today_str = timezone.now().strftime("%Y%m%d")
    file_basename = os.path.basename(filename)
    return f'{instance._meta.model_name}/{today_str}/{str(uuid4())}_{file_basename}'

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    nickname = models.CharField(max_length=50)
    image = models.ImageField(upload_to='upload_filepath', default='default.png')

    def __str__(self):
        return f'{self.username}'