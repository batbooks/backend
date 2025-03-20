from django.urls import path
from . import views



urlpatterns = [
     path('all/', views.BookListAPIView.as_view(), name='book-list'),
     path('<int:pk>/', views.BookDetailAPIView.as_view(), name='book-detail'),
     path('create/', views.BookCreateAPIView.as_view(), name='book-create'),
     path('chapter/<int:id>/',views.ChapterDetailUpdateDeleteAPIView.as_view(), name='Chapter-list'),
     path('chapter/create/', views.ChapterCreateAPIView.as_view(), name='Chapter-create'),
]
