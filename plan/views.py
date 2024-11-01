from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Plan, Category
from .serializers import PlanSerializer, CategorySerializer
from .permissions import CustomReadOnly
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from calendar import monthrange

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CustomReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [CustomReadOnly, IsAuthenticated]

    def get_queryset(self):
        return Plan.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("권한이 없습니다.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("권한이 없습니다.")
        instance.delete()

    @action(detail=False, methods=['get'])
    def monthly(self, request):
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))

        _, last_day = monthrange(year, month)
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, last_day, 23,59,59)  # 년, 월, 일, 시, 분, 초

        plans = self.get_queryset().filter(
            start__gte = start_date,
            start__lte = end_date
        ).order_by('start')

        calendar_data = {}
        
        for day in range(1, last_day+1):
            date_key = datetime(year,month,day).date().isoformat()
            calendar_data[date_key] = {
                'displayed_plans': [],
                'remaining_count': 0
            }

        plan_counts = {}
        for plan in plans:
            date_key = plan.start.date().isoformat()
            plan_counts[date_key] = plan_counts.get(date_key, 0) + 1
            plan_data= {
                'id' : plan.id,
                'title': plan.title,
                'start' : plan.start.isoformat(),
                'end': plan.end.isoformat(),
            }

            #if plan_counts[date_key] <= 3:
                #calendar_data[date_key]['displayed_plans'].append(plan_data)
            #else:
            if len(calendar_data[date_key]['displayed_plans']) < 2:
                calendar_data[date_key]['displayed_plans'].append(plan_data)
            else:
                calendar_data[date_key]['remaining_count'] += 1
        
        return Response(calendar_data)

    @action(detail=False, methods=['get'])
    def weekly(self, request):
        date_str = request.query_params.get('date')
        if date_str:
            try:
                current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error":"YYYY-MM-DD로 입력하세요"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                current_date = timezone.now().date()

            start_of_week = current_date - timedelta(days=current_date.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            plans = self.get_queryset().filter(
                start__date__gte = start_of_week,
                start__date__lte = end_of_week
            ).order_by('start')

            weekly_data = {}
            for i in range(7):
                date = start_of_week + timedelta(days=i)
                date_key = date.isoformat()
                weekly_data[date_key] = {
                    'displayed_plans' : [],
                    'remaining_count': 0
                }
            
            for plan in plans:
                date_key = plan.start.date().isoformat()
                plan_data = {
                    'id' : plan.id,
                    'title' : plan.title,
                    'start' : plan.start.isoformat(),
                    'end' : plan.end.isoformat()
                }

                if len(weekly_data[date_key]['displayed_plans']) < 2:
                    weekly_data[date_key]['displayed_plans'].append(plan_data)
                else:
                    weekly_data[date_key]['remaining_count'] += 1
                
            return Response(weekly_data)