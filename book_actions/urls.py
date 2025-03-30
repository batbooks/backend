from django.urls import  path
from . import  views
urlpatterns=[
    path('toggle/favorite/<int:book_id>',views.BookToggleFavoriteView.as_view(),),
]