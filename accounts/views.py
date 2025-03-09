from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer
from .models import  User
from rest_framework import status


class RegisterView(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            user = User.objects.create_user(email=request.data['email'],password=request.data['password'])
            return Response({'user':ser_data.data,})
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
