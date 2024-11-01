from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from promise.models import Promise
from users.models import Profile
from plan.models import Plan, Category

from promise.serializers import PromiseSerializer

class AcceptOrRejectPromiseView(APIView):
    def put(self, request, promise_id, username, accept_or_reject, format=None):
        try:
            user = Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            promise = Promise.objects.get(id=promise_id)
        except Promise.DoesNotExist:
            return Response({"message": "해당 약속을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            category = Category.objects.get(title="약속")
        except Category.DoesNotExist:
            return Response({"message": "약속 카테고리를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        
        if promise.status != "confirming":
            return Response({"message": "아직 약속 정보가 확정되지 않았습니다. 주최자는 [내 마음대로 확정] 혹은 [투표하기]를 진행해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        if not promise.members.filter(id=user.id).exists():
            return Response({"message": "해당 약속의 참여자에 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)


        selected_option = promise.promise_options.first()

        if accept_or_reject == 'accept':
            selected_option.members_can_attend.add(user)  # 옵션에 참여 가능자에 자신 추가
            promise.accept_members.add(user)  # 약속 수락 멤버에 자신 추가

            # Plan 생성
            plan = Plan.objects.create(
                author=user,
                title=selected_option.title,
                category=category,
                start=selected_option.start,
                end=selected_option.end,
                memo="",
                is_completed=False
            )

            plan.participant.set(selected_option.members_can_attend.all())


            serializer = PromiseSerializer(promise)
            return Response({"message": "약속이 수락되었습니다.", "result": serializer.data}, status=status.HTTP_200_OK)
        
        elif accept_or_reject == 'reject':
            promise.reject_members.add(user)
            if selected_option.members_can_attend.filter(id=user.id).exists():
                selected_option.members_can_attend.remove(user)

            serializer = PromiseSerializer(promise)

            return Response({"message": "약속이 거절되었습니다.", "result": serializer.data}, status=status.HTTP_200_OK)
        
        return Response({"message": "accept 혹은 reject가 아닌 다른 String이 입력되었습니다."}, status=status.HTTP_400_BAD_REQUEST)