from rest_framework import routers
from .views import *
from django.urls import path

router = routers.SimpleRouter()

urlpatterns = [ 
    path('plan/', NotificationViewSet.as_view({'get': 'list'}), {'notification_type': 'plan'}, name='notification_plan'),
    path('promise/', NotificationViewSet.as_view({'get': 'list'}), {'notification_type': 'promise'}, name='notification_promise'),
    path('friend/', NotificationViewSet.as_view({'get': 'list'}), {'notification_type': 'friend'}, name='notification_friend')
    ]