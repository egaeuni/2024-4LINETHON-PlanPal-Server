from django.shortcuts import render
from .models import Profile
from rest_framework import generics, status
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

class RegisterView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = Register

class LoginView(generics.GenericAPIView):
    serializer_class = Login

    def post(self, request):
        username=request.data.get("username")
        password=request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            Login(request, user)
            return Response({"message":"로그인 성공"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"사용자 이름 또는 비밀번호가 맞지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = 'username'

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(Profile, username=username)

class FriendsView(generics.CreateAPIView):
    serializer_class = Friends
    queryset = Profile.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_username = kwargs.get('username')
        try:
            user = Profile.objects.get(username=user_username)
        except ObjectDoesNotExist:
            return Response({'error': f"'{user_username}'을(를) 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        target_username = serializer.validated_data['username']
        try:
            target_user = Profile.objects.get(username=target_username)
        except ObjectDoesNotExist:
            return Response({'error': "해당 유저는 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        if user_username == target_username:
            return Response({'error': "자기 자신을 친구로 추가할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        if user.friends.filter(username=target_user.username).exists():
            return Response({'message': "이미 친구입니다."}, status=status.HTTP_200_OK)

        user.friends.add(target_user)
        return Response({'message': f"{target_user.username}님을 친구 추가했습니다."}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_username = kwargs.get('username')
        try:
            user = Profile.objects.get(username=user_username)
        except ObjectDoesNotExist:
            return Response({'error': f"프로필 '{user_username}'을(를) 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        target_username = serializer.validated_data['username']
        try:
            target_user = Profile.objects.get(username=target_username)
        except ObjectDoesNotExist:
            return Response({'error': f"프로필 '{target_username}'을(를) 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        user.friends.remove(target_user)
        return Response({'message': f"{target_user.username}님을 친구 목록에서 삭제했습니다."}, status=status.HTTP_204_NO_CONTENT)