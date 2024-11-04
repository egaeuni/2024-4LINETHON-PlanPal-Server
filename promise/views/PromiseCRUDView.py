from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from promise.models import Promise, Memo
from users.models import Profile

from promise.serializers import PromiseSerializer, MemoSerializer


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
    
    def put(self, request, promise_id, format=None):
        try:
            promise = Promise.objects.get(id=promise_id)
        except Promise.DoesNotExist:
            return Response({"message": "해당 약속을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        if not promise.status == "completed":
            return Response({"message": "해당 약속 정보가 확정되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        my_username = request.data.get('my_username')
        new_title = request.data.get('new_title')
        new_members_usernames = request.data.get('new_members_usernames', [])
        new_memo_content = request.data.get('new_memo_content')

        try:
            me = Profile.objects.get(username=my_username)
        except Profile.DoesNotExist:
            return Response({"message": "내 사용자 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        # 제목 변경
        if new_title:
            promise.title = new_title

        # 메모 변경
        # 이미 메모가 있는 경우
        try:
            memo = Memo.objects.get(promise=promise, user=me)
            if new_memo_content:
                memo.content = new_memo_content
                memo.save()
            else:
                memo.delete
        # 메모가 없는 경우 메모를 생성
        except Memo.DoesNotExist:
            Memo.objects.create(
                user=me,
                content=new_memo_content,
                promise=promise
            )

        # 참여자 변경
        if new_members_usernames:
            new_members = Profile.objects.filter(username__in=new_members_usernames)
            promise.accept_members.set(new_members)
        else:
            # 전체를 지운 경우
            promise.accept_members.clear()

        promise.save() 

        serializer = PromiseSerializer(promise)
        
        return Response({"message": "약속 수정에 성공하였습니다.", "result": serializer.data}, status=status.HTTP_200_OK)



# 사용자 이름으로 약속 리스트 조회
class GETPromiseByUsername(APIView):
    # username으로 약속 정보 조회
    def get(self, request, username, format=None):
        try:
            user = Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        promises = Promise.objects.filter(Q(user=user) | Q(accept_members=user)).distinct()
        
        serializer = PromiseSerializer(promises, many=True, context={'username': username})


        return Response({"message": "약속 정보 조회에 성공하였습니다.", "result": serializer.data}, status=status.HTTP_200_OK)