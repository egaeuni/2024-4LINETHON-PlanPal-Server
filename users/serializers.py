from .models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password

class Register(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators = [validate_password]
    )

    password2 = serializers.CharField(write_only=True, required=True,)

    nickname = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'password2','nickname')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password":"비밀번호가 일치하지 않습니다."}
            )
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            nickname=validated_data['nickname']  
        )
        user.make_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user
