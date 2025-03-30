from django.urls import  path
from . import  views
urlpatterns=[
    path('toggle/favorite/<int:book_id>/',views.BookToggleFavoriteView.as_view(),),
    path('get/favorite/',views.UserFavoriteView.as_view(),),
]