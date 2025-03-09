from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer
from .models import User, OTP
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
import random


class RegisterView(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        ser_data.validate(request.data)
        if ser_data.is_valid(raise_exception=True):
            otp_code = random.randint(100000, 999999)

            user = User.objects.filter(email=request.data['email'])
            if user.exists():
                if user.first().is_active:
                    user.filter().delete()
                return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.create_user(email=request.data['email'], password=request.data['password'])
            OTP.objects.get_or_create(user=user, code=otp_code)
            send_mail(
                'کد تأیید ثبت‌نام',
                f' کد تأیید شما: {otp_code} ',
                settings.EMAIL_HOST_USER,
                [request.data['email']],
                fail_silently=False,
            )
            return Response({'stat': 'success', }, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        try:
            otp = OTP.objects.get(user__email=request.data['email'])
            if otp.code == request.data['code']:
                user = User.objects.get(email=request.data['email'])
                user.is_active = True
                user.save()
                otp.delete()
                return Response({'message': 'register is successful'}, status=status.HTTP_201_CREATED)
            return Response({'error': 'OTP یافت نشد'}, status=status.HTTP_404_NOT_FOUND)
        except OTP.DoesNotExist:
            return Response({'error': 'OTP یافت نشد'}, status=status.HTTP_404_NOT_FOUND)
