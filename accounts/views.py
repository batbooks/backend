from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer
from .models import User
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
import os


class RegisterView(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            send_mail('hello', 'iam you', settings.EMAIL_HOST_USER, [request.data['email']])
            user = User.objects.create_user(email=request.data['email'], password=request.data['password'])
            return Response({'user': ser_data.data, })
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
