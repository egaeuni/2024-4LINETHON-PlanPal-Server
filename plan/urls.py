from rest_framework import routers
from .views import *
from django.urls import path

router = routers.SimpleRouter()

urlpatterns = [ 
    path('categories/<str:username>/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='categories'),
    path('categories/<str:username>/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='category-detail'),
    path('plans/<str:username>/', PlanViewSet.as_view({'get': 'list', 'post': 'create'}), name='plans'),
    path('plans/<str:username>/<int:pk>/', PlanViewSet.as_view({'get': 'retrieve','put': 'update','delete': 'destroy'}), name='plan-detail'),
    path('plans/<str:username>/monthly/', PlanViewSet.as_view({'get': 'monthly'}), name='monthly_plans'),
    path('plans/<str:username>/weekly/', PlanViewSet.as_view({'get': 'weekly'}), name='weekly_plans'),
    path('plans/<str:username>/daily/', PlanViewSet.as_view({'get': 'daily'}), name='daily_plans'),
]