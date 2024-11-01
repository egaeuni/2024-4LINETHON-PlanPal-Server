from django.urls import path
from .views.CreatePromiseOptionsView import CreatePromiseOptionsView
from .views.ConfirmImmediatelyView import ConfirmImmediatelyView
from .views.PromiseCRUDView import PromiseCRUDView

urlpatterns = [
    path('promise/option/', CreatePromiseOptionsView.as_view(), name='promise-option-create'),
    path('promise/confirm/immediately/<int:promise_id>/<int:promise_option_id>', ConfirmImmediatelyView.as_view(), name='promise-confirm-immediately'),
    path('promise/<int:promise_id>/', PromiseCRUDView.as_view(), name='promise-crud'),
]
