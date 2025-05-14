from django.urls import path
from . import views

urlpatterns = [
    path('', views.ForumListAPIView.as_view(), name='All_forum'),

    path('<int:pk>/', views.ForumThreadListAPIView.as_view(), name='api_threads_of_forum'),
    path('threads/create/', views.ThreadCreateAPIView.as_view(), name='api_thread_create'),
    path('threads/<int:pk>/', views.ThreadUpdateAPIView.as_view(), name='api_thread_update'),
]