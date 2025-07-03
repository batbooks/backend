from django.urls import path
from . import views


app_name='book'
urlpatterns = [
     path('all/', views.BookListAPIView.as_view(), name='book-list'),
     path('<int:pk>/', views.BookDetailAPIView.as_view(), name='book-detail'),
     path('create/', views.BookCreateAPIView.as_view(), name='book-create'),
     path('chapter/<int:id>/',views.ChapterDetailUpdateDeleteAPIView.as_view(), name='Chapter-list'),
     path('chapter/create/', views.ChapterCreateAPIView.as_view(), name='Chapter-create'),
     path('search/<str:book_name>/', views.BookSearchAPIView.as_view(), name='book-search'),
     path('user/<int:id>/', views.UserBookAPIView.as_view(), name='user-detail'),
     path('my/', views.MyBookAPIView.as_view(), name='my-detail'),
     path('uploadfile/', views.PDFUploadAPIView.as_view(), name='upload_pdf'),

     path('user-book-progress/', views.UserBookProgressListCreateView.as_view(), name='user-book-progress-list'),
     path('user-book-progress/<int:pk>/',  views.UserBookProgressDetailView.as_view(), name='user-book-progress-detail'),
]
