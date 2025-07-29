from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.UserPlaylistListView.as_view(), name='playlist-list-get'),
    path('all/', views.PublicPlaylistListView.as_view(), name='playlist-public-get'),
    path('create/', views.PlaylistListCreateView.as_view(), name='playlist-list-create'),
    path('<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist-detail'),
    path('users/<int:user_id>/', views.AnotherUserPublicPlaylistsView.as_view(), name='playlist-of_another'),
    path('search/', views.PlaylistSearchView.as_view(), name='playlist-search'),


    path('<int:playlist_id>/books/', views.PlaylistBookListView.as_view(), name='playlistbook-list'),
    path('<int:playlist_id>/books/add/', views.AddBookToPlaylistView.as_view(), name='playlistbook-post'),
    path('<int:playlist_id>/books/<int:book_id>/', views.PlaylistBookDetailView.as_view(),
         name='playlistbook-detail'),
]