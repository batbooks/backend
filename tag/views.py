from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tag.models import TagCategory, Tag, Genre

# Create your views here.
class GenreListView(APIView):
    def get(self, request):
        genres = Genre.objects.values_list('title', flat=True)
        return Response({"genres": list(genres)}, status=status.HTTP_200_OK)

# View to get all tag categories and their associated tags
class TagCategoryView(APIView):
    def get(self, request):
        tag_categories = TagCategory.objects.all()
        data = []

        for category in tag_categories:
            tags = category.tags.values_list('title', flat=True)
            data.append({
                "category": category.title,
                "tags": list(tags)
            })

        return Response({"tag_categories": data}, status=status.HTTP_200_OK)
