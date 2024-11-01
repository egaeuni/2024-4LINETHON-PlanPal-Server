from rest_framework import serializers
from .models import Promise, PromiseOption
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

# 약속 시리얼라이저
class PromiseSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    members = ProfileSerializer(many=True, read_only=True)
    accept_members = ProfileSerializer(many=True, read_only=True)
    reject_members = ProfileSerializer(many=True, read_only=True)
    promise_options = PromiseOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Promise
        fields = ['id', 'title', 'start', 'end', 'length', 'created_at', 'status', 'user', 'members', 'accept_members', 'reject_members', 'promise_options']

# 가능한 약속시간 탐색 필드 검증을 위한 시리얼라이저 
class CreatePromiseOptionsSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    members_username = serializers.ListField(child=serializers.CharField(), required=True)
    title = serializers.CharField(required=True)
    start = serializers.DateTimeField(required=True)
    end = serializers.DateTimeField(required=True)
    length = serializers.IntegerField(required=True)

