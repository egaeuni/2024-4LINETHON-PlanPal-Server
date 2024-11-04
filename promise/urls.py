from django.urls import path
from .views.CreatePromiseOptionsView import CreatePromiseOptionsView
from .views.ConfirmImmediatelyView import ConfirmImmediatelyView
from .views.PromiseCRUDView import PromiseCRUDView, GETPromiseByUsername
from .views.AcceptOrRejectPromiseView import AcceptOrRejectPromiseView
from .views.VotingView import VotingView, VotingChageStatusView

urlpatterns = [
    path('promise/option/', CreatePromiseOptionsView.as_view(), name='promise-option-create'),
    path('promise/confirm/<int:promise_id>/<int:promise_option_id>', ConfirmImmediatelyView.as_view(), name='promise-confirm-immediately'),
    path('promise/<int:promise_id>/', PromiseCRUDView.as_view(), name='promise-crud'),
    path('promise/<str:username>/', GETPromiseByUsername.as_view(), name='promise-list-by-username'),
    path('promise/accept/<int:promise_id>/<str:username>/<str:accept_or_reject>', AcceptOrRejectPromiseView.as_view(), name='promise-accept-or-reject'),
    path('promise/vote/<str:username>/<int:promise_id>', VotingChageStatusView.as_view(), name='promise-status-voting'),
    path('promise/vote/<str:username>/<int:promise_id>/<int:promise_option_id>', VotingView.as_view(), name='promise-vote'),
]
