from rest_framework import serializers
from .models import Promise, PromiseOption, Memo
from users.models import Profile

# 'id', 'username', 'nickname' 반환을 위한 시리얼라이저
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'nickname']

# 약속 후보들 시리얼라이저
class PromiseOptionSerializer(serializers.ModelSerializer):
    members_can_attend = ProfileSerializer(many=True, read_only=True)
    vote_members = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = PromiseOption
        fields = ['id', 'title', 'start', 'end', 'length', 'members_can_attend', 'vote_members']

# Memo 시리얼라이저
class MemoSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Memo
        fields = ['id', 'user', 'content', 'promise'] 

# Mark 시리얼라이저
class MarkSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Memo
        fields = ['id', 'user', 'promise'] 

# 약속 시리얼라이저
class PromiseSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    members = ProfileSerializer(many=True, read_only=True)
    accept_members = ProfileSerializer(many=True, read_only=True)
    reject_members = ProfileSerializer(many=True, read_only=True)
    promise_options = PromiseOptionSerializer(many=True, read_only=True)
    memos = MemoSerializer(many=True, read_only=True)

    # 특정 username의 Mark만 반환하는 필드 추가
    marks = serializers.SerializerMethodField()

    class Meta:
        model = Promise
        fields = ['id', 'title', 'start', 'end', 'length', 'created_at', 'status', 'user', 'members', 'accept_members', 'reject_members', 'promise_options', 'memos', 'marks']

    def get_marks(self, obj):
        username = self.context.get('username')  # Serializer의 context에서 username 가져오기
        marks = obj.mark.filter(user__username=username)  # 해당 username의 Mark 필터링
        return MarkSerializer(marks, many=True).data

# 가능한 약속시간 탐색 필드 검증을 위한 시리얼라이저 
class CreatePromiseOptionsSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    members_username = serializers.ListField(child=serializers.CharField(), required=True)
    title = serializers.CharField(required=True)
    start = serializers.DateTimeField(required=True)
    end = serializers.DateTimeField(required=True)
    length = serializers.IntegerField(required=True)

