from rest_framework import viewsets
from .models import Plan, Category
from .serializers import PlanSerializer, CategorySerializer
from .permissions import CustomReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CustomReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [CustomReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
