from django.urls import path
from . import views

urlpatterns = [
    path('show/<int:user_id>/', views.ShowMessageApiView.as_view()),
    path('message/<int:message_id>/', views.MessageDeleteApiView.as_view()),
    path('group/create/', views.GroupCreateView.as_view()),
]