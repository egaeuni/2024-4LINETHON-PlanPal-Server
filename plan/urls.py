from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register('plans', PlanViewSet)

urlpatterns = router.urls