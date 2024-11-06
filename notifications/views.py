from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.views import APIView

class PlanNotificationView(APIView):
    def get(self, request, *args, **kwargs):
        filtered_notifications = Notification.objects.filter(
            notification_type__in=['plan_deadline', 'daily_achievement'])

        serializer = NotificationSerializer(filtered_notifications, many=True)

        return Response({"message":"계획 알림을 불러왔습니다.", "result":serializer.data}, status=status.HTTP_200_OK)

class PromiseNotificationView(APIView):
    def get(self, request, *args, **kwargs):
        filtered_notifications = Notification.objects.filter(
            notification_type__in=['vote', 'promise_accept'])

        serializer = NotificationSerializer(filtered_notifications, many=True)

        return Response({"message":"약속 알림을 불러왔습니다.", "result":serializer.data}, status=status.HTTP_200_OK)

class FriendNotificationView(APIView):
    def get(self, request, *args, **kwargs):
        filtered_notifications = Notification.objects.filter(
            notification_type__in=['brag', 'cheering', 'add_friend'])

        serializer = NotificationSerializer(filtered_notifications, many=True)

        return Response({"message":"친구 알림을 불러왔습니다.", "result":serializer.data}, status=status.HTTP_200_OK)