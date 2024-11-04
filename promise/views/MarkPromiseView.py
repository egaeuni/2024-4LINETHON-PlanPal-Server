from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from promise.models import Promise, Mark
from users.models import Profile

from promise.serializers import PromiseSerializer


# 즐겨찾기 선택/해제
class MarkPromiseView(APIView):
    def post(self, request, username, promise_id, format=None):
        try:
            user = Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            promise = Promise.objects.get(id=promise_id)
        except Promise.DoesNotExist:
            return Response({"message": "해당 약속을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        # 이미 즐겨찾기가 있는지 확인
        if Mark.objects.filter(user=user, promise=promise).exists():
            return Response({"message": "이미 즐겨찾기한 약속입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # Mark 인스턴스 생성
        Mark.objects.create(
            user=user,
            promise=promise
        )
        
        serializer = PromiseSerializer(promise, context={'username': username})

        return Response({"message": "즐겨찾기에 성공하였습니다.", "result": serializer.data}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, username, promise_id, format=None):
        try:
            user = Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            promise = Promise.objects.get(id=promise_id)
        except Promise.DoesNotExist:
            return Response({"message": "해당 약속을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        # 이미 즐겨찾기가 해제 되어있는지 
        if not Mark.objects.filter(user=user, promise=promise).exists():
            return Response({"message": "즐겨찾기 되어있지 않은 약속입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # Mark 인스턴스 생성
        mark = Mark.objects.get(user=user, promise=promise)
        mark.delete()
        
        serializer = PromiseSerializer(promise, context={'username': username})

        return Response({"message": "즐겨찾기 해제에 성공하였습니다.", "result": serializer.data}, status=status.HTTP_200_OK)

