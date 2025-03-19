from django.urls import path
from . import views

urlpatterns = [
    path('<str:id>/', views.UserInfoView.as_view(), name='home'),
    path('change/username/', views.UsernameUpdateView.as_view(), name='change-username'),
    path('change/<str:id>',views.UserInfoUpdateView.as_view(), name='change-info'),
]
