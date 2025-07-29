from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserReadSerializer,ResetPasswordSerializer,UserRegisterSerializer
from .models import User, OTP
from rest_framework import status
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
import random
from config.mail_utils import send_mail
class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserReadSerializer
    def get(self, request:Request):

        user = request.user
        ser_data = UserReadSerializer(instance = user)
        return Response(ser_data.data, status=status.HTTP_200_OK)
class RegisterView(APIView):
    serializer_class = UserRegisterSerializer
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        ser_data.validate(request.data)
        if ser_data.is_valid(raise_exception=True):
            otp_code = random.randint(100000, 999999)

            user = User.objects.create_user(email=request.data['email'], password=request.data['password'])
            otp , created = OTP.objects.get_or_create(user=user, code=otp_code)
            send_mail(
                'کد تأیید ثبت ‌نام',
                f' کد تأیید شما: {otp_code} ',
                [request.data['email']],
            )
            return Response({'message': 'رمز شما با موفقیت فرستاده شد.', }, status=status.HTTP_200_OK)
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
                return Response({'messege': 'رمز OTP صحیح میباشد.'}, status=status.HTTP_201_CREATED)
            return Response({'error': 'رمز یکبار مصرف اشتباه است'}, status=status.HTTP_404_NOT_FOUND)
        except OTP.DoesNotExist:
            return Response({'error': 'رمز یکبار مصرف برای این ایمیل پیدا نشد'}, status=status.HTTP_404_NOT_FOUND)


class SendOTPResetView(APIView):

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'ایمیل مورد نیاز است'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response({'error': 'کاربر پیدا نشد یا غیر فعال است'}, status=status.HTTP_404_NOT_FOUND)

        otp_code = random.randint(100000, 999999)

        otp, created = OTP.objects.update_or_create(
            user=user,
            defaults={'code': otp_code}
        )


        send_mail(
            'کد تایید فراموشی پسورد',
            f' رمز یکبار مصرف شما: {otp_code}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return Response({'messege': 'رمز شما فرستاده شد.'}, status=status.HTTP_200_OK)


class VerifyOTPAndResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    def post(self, request):
        ser_data = ResetPasswordSerializer(data=request.data)
        ser_data.validate(request.data)
        if ser_data.is_valid(raise_exception=True):
            email = request.data['email']
            code = request.data['code']
            new_password = request.data['new_password']
            new_password_conf = request.data['new_password_conf']

            try:
                otp = OTP.objects.get(user__email=email, code=code)
            except OTP.DoesNotExist:
                return Response({'error': 'ایمیل یا رمز یکبار مصرف اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)

            user = otp.user
            user.password = make_password(new_password)
            user.save()

            otp.delete()

            return Response({'messege': 'گذرواژه با موفقیت بازنشانی شد'}, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


