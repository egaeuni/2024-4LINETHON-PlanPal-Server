from .models import Profile
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from plan.models import Category

# 회원가입
class Register(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators = [validate_password]
    )

    password2 = serializers.CharField(write_only=True, required=True,)

    nickname = serializers.CharField(required=True)
    
    class Meta:
        model = Profile
        fields = ('username', 'password', 'password2','nickname')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password":"비밀번호가 일치하지 않습니다."}
            )
        return data

    def create(self, validated_data):
        user = Profile.objects.create(
            username=validated_data['username'],
            nickname=validated_data['nickname']  
        )
        user.set_password(validated_data['password'])
        user.save()
        
        # 약속 카테고리 생성
        Category.objects.create(
            author=user,
            title="약속",
            color="#FF6A3B",
            is_public=True
        )

        return user

# 로그인
class Login(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

# 프로필 정보 확인
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('nickname', 'image', 'intro')
    
    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.image = validated_data.get('image', instance.image)
        instance.intro = validated_data.get('intro', instance.intro)
        instance.save()
        return instance

# 친구 추가 및 삭제
class Friends(serializers.Serializer):
    username = serializers.CharField()
    
    def create(self, validated_data):
        request_user = self.context['request'].user
        target_user = get_object_or_404(Profile, user__username=validated_data['username'])

        request_user.friends.add(target_user)
        return target_user