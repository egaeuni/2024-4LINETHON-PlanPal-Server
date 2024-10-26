from django.shortcuts import render
from .models import Profile
from rest_framework import generics, status
from .serializers import *
from rest_framework.response import Response

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
