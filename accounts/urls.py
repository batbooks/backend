from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='home'),
    path('otp/',views.VerifyOTPView.as_view(), name='otp'),
    path('reset-password/send-otp/', SendOTPResetView.as_view(), name='send-reset-otp'),
    path('reset-password/verify-otp/', VerifyOTPAndResetPasswordView.as_view(), name='verify-reset-otp'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
