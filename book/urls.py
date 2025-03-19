from django.urls import path
from . import views



urlpatterns = [
     path('all/', views.BookListAPIView.as_view(), name='book-list'),
     path('<int:pk>/', views.BookDetailAPIView.as_view(), name='book-detail'),
     path('create/', views.BookCreateAPIView.as_view(), name='book-create'),
]
