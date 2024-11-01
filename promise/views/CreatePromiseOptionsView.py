from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.db.models import Q

from promise.models import PromiseOption, Promise
from plan.models import Plan
from users.models import Profile

from promise.serializers import CreatePromiseOptionsSerializer, PromiseSerializer


# 가능한 약속시간 탐색
class CreatePromiseOptionsView(APIView):
    def post(self, request, format=None):
        serializer = CreatePromiseOptionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 유효성 검사

        # 유효한 데이터 가져오기
        validated_data = serializer.validated_data
        username = validated_data['username']
        members_usernames = validated_data['members_username']
        title = validated_data['title']
        start_date = validated_data['start']
        end_date = validated_data['end']
        length = validated_data['length']

        if (start_date == end_date):
            return Response({"message": "시작 시간과 끝나는 시간이 같습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if (end_date - start_date < timedelta(hours=length)):
            return Response({"message": "시작 시간과 끝나는 시간의 기간이 약속 길이보다 짧습니다."}, status=status.HTTP_400_BAD_REQUEST)


        promise_options_except_only_me = []

        # 먼저 내가 가능한 시간부터 탐색함
        user_profile = get_object_or_404(Profile, username=username)
        my_options = findAvailable(user_profile, start_date, end_date, length)

        # 약속 가능한 시간이 있다면 저장
        for option in my_options:
            # 각 멤버에 대해 자신의 Plan이 비어있는지 확인하고 비어있으면 추가
            for member_username in members_usernames:
                member_profile = get_object_or_404(Profile, username=member_username)
                if isAvailable(member_profile, option["start"], option["end"]):
                    option["members"].append(member_profile)

        for option in my_options:
            # 나 혼자만 가능한 일정은 제외해야 함
            if len(option["members"]) != 1:
                promise_option = PromiseOption.objects.create(
                    title=title,
                    start=option["start"],
                    end=option["end"],
                    length=length
                )
                promise_option.members_can_attend.set(option["members"])  # 일정 가능한 사람들 추가
                promise_options_except_only_me.append(promise_option)

        # Promise 인스턴스 생성
        promise = Promise.objects.create(
            user=user_profile,
            title=title,
            start=start_date,
            end=end_date,
            length=length,
            status="created",
        )

        promise.members.set(Profile.objects.filter(username__in=members_usernames + [username]))
        promise.promise_options.set(promise_options_except_only_me)
        
        serializer = PromiseSerializer(promise)

        return Response({"message": "가능한 약속시간 탐색에 성공하였습니다.", "result": serializer.data}, status=status.HTTP_201_CREATED)


# 한 사용자의 가능한 시간을 반환해주는 함수
def findAvailable(user_profile, start_date, end_date, length):
    promise_options = []

    # 사용자 일정 조회
    plans = Plan.objects.filter(
        Q(author=user_profile),
        Q(end__gte=start_date) & Q(start__lte=end_date)
    ).order_by("start")

    available_start = start_date
    for plan in plans:
        # 현재 가능한 시간과 계획의 시작 시간을 비교
        while available_start + timedelta(hours=length) <= plan.start:
            option = {
                "start": available_start,
                "end": available_start + timedelta(hours=length),
                "members" : [user_profile]
            }
            promise_options.append(option)
            available_start += timedelta(minutes=30)  # 30분씩 이동하여 다음 가능한 시간을 찾음

        available_start = max(available_start, plan.end)  # 다음 가능한 시작시간 업데이트

    # 마지막으로 전체 시간 범위 내에서 남은 시간 추가
    while available_start + timedelta(hours=length) <= end_date:
        option = {
            "start": available_start,
            "end": available_start + timedelta(hours=length),
            "members" : [user_profile]
        }
        promise_options.append(option)
        available_start += timedelta(minutes=30)

    return promise_options


# start와 end 사이에 일정이 없는지 확인하여 Bool로 반환하는 함수
def isAvailable(user_profile, start, end):
    # 사용자 일정 조회
    plans = Plan.objects.filter(
        Q(author=user_profile),
        Q(end__gt=start) & Q(start__lt=end)
    )

    # 만약 계획이 없다면 True 반환 (비어있음)
    if not plans.exists():
        return True

    # 계획이 존재한다면 False 반환 (비어있지 않음)
    return False
