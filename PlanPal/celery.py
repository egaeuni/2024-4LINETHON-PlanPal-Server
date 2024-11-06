from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


# 기본 Django settings 모듈을 Celery가 사용할 수 있도록 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PlanPal.settings")

app = Celery("PlanPal")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

