from django.urls import path
from .views.CreatePromiseOptionsView import CreatePromiseOptionsView

urlpatterns = [
    path('promise/option/', CreatePromiseOptionsView.as_view(), name='promise-option-create'),
]
