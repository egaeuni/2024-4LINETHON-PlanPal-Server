from django.db import models
import os
from uuid import uuid4
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

def upload_filepath(instance, filename):
    today_str = timezone.now().strftime("%Y%m%d")
    file_basename = os.path.basename(filename)
    return f'{instance._meta.model_name}/{today_str}/{str(uuid4())}_{file_basename}'

class Profile(AbstractUser):
    nickname = models.CharField(max_length=50)
    image = models.ImageField(upload_to='upload_filepath', default='default.png')
    friends = models.ManyToManyField('self', symmetrical=False, related_name='user_friends') # symmetrical = True -> 자동 맞팔

    def __str__(self):
        return f'{self.username}'