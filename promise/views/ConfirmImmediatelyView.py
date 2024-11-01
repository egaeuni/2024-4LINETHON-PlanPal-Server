from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from promise.models import PromiseOption, Promise

from promise.serializers import PromiseSerializer


# 내 마음대로 확정하기, 즉시 확정하기
class ConfirmImmediatelyView(APIView):
    def put(self, request, promise_id, promise_option_id, format=None):
        
        # 해당 약속, 약속 후보 데이터 찾기
        try:
            promise = Promise.objects.get(id=promise_id)
        except Promise.DoesNotExist:
            return Response({"message": "해당 약속을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            promise_option = PromiseOption.objects.get(id=promise_option_id)
        except PromiseOption.DoesNotExist:
            return Response({"message": "해당 약속 후보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        
        # 해당 약속의 status 변경
        promise.status = "confirming"
        promise.promise_options.set([promise_option])

        promise.save()
        serializer = PromiseSerializer(promise)

        return Response({"message": "내 마음대로 확정하기에 성공하였습니다.", "result": serializer.data}, status=status.HTTP_200_OK)
