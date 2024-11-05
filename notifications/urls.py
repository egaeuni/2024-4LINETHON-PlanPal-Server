from rest_framework import routers
from .views import *
from django.urls import path

router = routers.SimpleRouter()

urlpatterns = [ 
    path('', NotificationViewSet.as_view({'get': 'list'}), name='notifications'),

]