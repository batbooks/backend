from django.urls import  path
from . import  views
urlpatterns=[
    path('category/',views.HomeCategoryView.as_view(),name='home'),
    path('suggestion/book/',views.HomeSuggestionBookView.as_view(),name='suggestion_book'),
    path('newest/book/',views.HomeNewestBookView.as_view(),name='newest_book'),
    path('popular/author/',views.HomeMostPopularAuthorsView.as_view(),name='popular'),
    path('active/author/',views.HomeMostActiveAuthorsView.as_view(),name='active'),
]