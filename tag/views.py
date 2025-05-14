from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from paginations import CustomPagination
from tag.models import TagCategory, Tag, Genre
from  tag.serializer import TagCategorySerializer,TagSerializer,GenreSerializer


class GenreListView(APIView):
    serializer_class = GenreSerializer
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response({"genres": serializer.data}, status=status.HTTP_200_OK)


class TagCategoryView(APIView):
    serializer_class = TagSerializer
    def get(self, request):
        tag_categories = TagCategory.objects.all()
        serializer = TagCategorySerializer(tag_categories, many=True)
        return Response({"tag_categories": serializer.data}, status=status.HTTP_200_OK)