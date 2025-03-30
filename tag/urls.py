from django.urls import path
from .views import GenreListView, TagCategoryView

urlpatterns = [
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('tag-categories/', TagCategoryView.as_view(), name='tag-category-list'),
]
