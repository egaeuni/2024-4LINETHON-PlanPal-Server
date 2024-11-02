from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Plan, Category
from .serializers import PlanSerializer, CategorySerializer
from .permissions import CustomReadOnly
from django.db.models import Q
from datetime import datetime, timedelta, time
from django.utils import timezone
from calendar import monthrange
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        username = self.kwargs.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            return Category.objects.filter(author__username=username)
        return Category.objects.all()

    def create(self, request, username=None):
        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, username=None, pk=None):
        user = get_object_or_404(User, username=username)
        category = get_object_or_404(Category, pk=pk, author=user)
        serializer = self.get_serializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, username=None, pk=None):
        user = get_object_or_404(User, username=username)
        category = get_object_or_404(Category, pk=pk, author=user)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    def get_queryset(self):
        username = self.kwargs.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            return Plan.objects.filter(author=user)
        return super().get_queryset()

    def create(self, request, username=None):
        user = get_object_or_404(User, username=username)
        user = get_object_or_404(User, username=username)
        if request.user.username == username:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, username=None, pk=None):
        user = get_object_or_404(User, username=username)
        plan = get_object_or_404(Plan, pk=pk, author=user)
        serializer = self.get_serializer(plan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, username=None, pk=None):
        user = get_object_or_404(User, username=username)
        plan = get_object_or_404(Plan, pk=pk, author=user)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def monthly(self, request, username=None):
        user = get_object_or_404(User, username=username)
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))

        _, last_day = monthrange(year, month)
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, last_day, 23,59,59)  # 년, 월, 일, 시, 분, 초

        plans = self.get_queryset().filter(
            author=user,
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
            start_hour = plan.start.hour
            end_hour = plan.end.hour
            plan_counts[date_key] = plan_counts.get(date_key, 0) + 1

            plan_data= {
                'id' : plan.id,
                'title': plan.title,
                'start' : plan.start.isoformat(),
                'end': plan.end.isoformat(),
            }

            if len(calendar_data[date_key]['displayed_plans']) < 2:
                calendar_data[date_key]['displayed_plans'].append(plan_data)
            else:
                calendar_data[date_key]['remaining_count'] += 1
        
        return Response(calendar_data)

    @action(detail=False, methods=['get'])
    def weekly(self, request, username=None):
        user = get_object_or_404(User, username=username)
        date_str = request.query_params.get('date')
        if date_str:
            try:
                current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error":"YYYY-MM-DD로 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                current_date = timezone.now().date()

            start_of_week = current_date - timedelta(days=current_date.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            plans = self.get_queryset().filter(
                author=user,
                start__date__gte = start_of_week,
                start__date__lte = end_of_week + timedelta(days=1)
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
                start_hour = plan.start.hour
                end_hour = plan.end.hour if plan.end else date_key

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

    @action(detail=False, methods=['get'])
    def daily(self, request, username=None):
        user = get_object_or_404(User, username=username)
        date_str = request.query_params.get('date')
        if date_str:
            try:
                current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "YYYY-MM-DD로 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            current_date = timezone.now().date()

        time_slots = {hour: [] for hour in range(24)}   # 0시 ~ 23시
        categories = {}

        plans = self.get_queryset().filter(author=user, start__date=current_date).order_by('start')

        for plan in plans:
            start_hour = plan.start.hour
            end_hour = plan.end.hour if plan.end else start_hour
            plan_data = {
                'id': plan.id,
                'title': plan.title,
                'category': plan.category.title if plan.category else None,
                'start': plan.start.isoformat(),
                'end': plan.end.isoformat() if plan.end else None,
            }

            for hour in range(start_hour, end_hour + 1):
                time_slots[hour].append(plan_data)

            category_title = plan.category.title if plan.category else "Uncategorized"
            if category_title not in categories:
                categories[category_title] = []
            categories[category_title].append(plan_data)

        return Response({
            "time_slots": time_slots,
            "categories": categories
        })