from django.urls import  path
from . import  views
urlpatterns=[
    path('category/',views.HomeCategoryView.as_view(),name='home'),
    path('popular/author/',views.HomeMostPopularAuthorsView.as_view(),name='popular'),
    path('active/author/',views.HomeMostActiveAuthorsView.as_view(),name='popular'),
]