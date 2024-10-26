from django.shortcuts import render
from .models import Profile
from rest_framework import generics, status
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class RegisterView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = Register

class LoginView(generics.GenericAPIView):
    serializer_class = Login

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response({"token":token.key}, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class FriendsView(generics.CreateAPIView):
    serializer_class = Friends
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        target_user = Profile.objects.get(username=serializer.validated_data['username'])
        return Response({'message': f"{target_user.username}님을 친구 추가했습니다."}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target_user = Profile.objects.get(username=serializer.validated_data['username'])
        
        request.user.friends.remove(target_user)
        return Response({'message': f"{target_user.username}님을 친구 목록에서 삭제했습니다."}, status=status.HTTP_204_NO_CONTENT)