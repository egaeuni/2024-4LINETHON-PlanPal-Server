from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from promise.models import PromiseOption, Promise
from users.models import Profile

from promise.serializers import PromiseSerializer


# Promise에 대한 기본적인 CRUD API
class PromiseCRUDView(APIView):

    # 약속 정보 id로 조회
    def get(self, request, promise_id, format=None):
        try:
            promise = Promise.objects.get(id=promise_id)
        except Promise.DoesNotExist:
            return Response({"message": "해당 약속을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PromiseSerializer(promise)

        return Response({"message": "약속 정보 조회에 성공하였습니다.", "result": serializer.data}, status=status.HTTP_200_OK)

    # 약속 id로 삭제
    def delete(self, request, promise_id, format=None):
        try:
            promise = Promise.objects.get(id=promise_id)
        except Promise.DoesNotExist:
            return Response({"message": "해당 약속을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        promise.delete()

        return Response({"message": "약속 정보 삭제에 성공하였습니다."}, status=status.HTTP_200_OK)

class GETPromiseByUsername(APIView):
    # username으로 약속 정보 조회
    def get(self, request, username, format=None):
        try:
            user = Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        promises = Promise.objects.filter(user=user)
        serializer = PromiseSerializer(promises, many=True)

        return Response({"message": "약속 정보 조회에 성공하였습니다.", "result": serializer.data}, status=status.HTTP_200_OK)