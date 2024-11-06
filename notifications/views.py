from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.views import APIView

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        notification_type = self.kwargs.get('notification_type')
        return Notification.objects.filter(recipient=self.request.user, notification_type=notification_type)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "알림 조회에 성공했습니다.",
            "result": serializer.data
        }, status=status.HTTP_200_OK)

class PlanAlarmView(APIView):
    def get(self, request, NOTIFICATION_TYPES):
        try:
            notification = Notification.objects.filter(notification_type=plan_deadline)
        except Notification.DoesNotExist:
            return Response({"message":"Plan 관련 알림을 찾지 못했습니다."})