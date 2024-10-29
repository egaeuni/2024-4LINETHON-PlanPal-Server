from rest_framework import viewsets
from .models import Plan
from .serializers import PlanSerializer
from .permissions import CustomReadOnly

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [CustomReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
