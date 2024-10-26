from .models import Profile
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

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
        token = Token.objects.create(user=user)
        return user

# 로그인
class Login(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            return token
        else:
            raise serializers. ValidationError("사용자 이름 또는 비밀번호가 맞지 않습니다.")