from django.urls import  path
from . import  views
urlpatterns=[
    path('toggle/favorite/<int:book_id>/',views.BookToggleFavoriteView.as_view(),),
    path('get/favorite/',views.UserFavoriteView.as_view(),),
    path('is/favorite/<int:book_id>/', views.BookIsFavoriteView.as_view(), ),

    path('toggle/blocked/<int:book_id>/',views.BookToggleBlockedView.as_view(),),
    path('get/blocked/',views.UserBlockedView.as_view(),),
    path('rating/',views.BookRatingView.as_view(),),

    path('toggle/favoritePlaylist/<int:playlist_id>/', views.PlaylistToggleFavoriteView.as_view(), ),
    path('get/favoritePlaylist/', views.UserPlaylistFavoriteView.as_view(), ),
    path('is/favoritePlaylist/<int:playlist_id>/', views.PlaylistIsFavoriteView.as_view(), ),


]