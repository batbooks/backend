from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from paginations import CustomPagination
from tag.models import TagCategory, Tag, Genre
from  tag.serializer import TagCategorySerializer,TagSerializer,GenreSerializer


# Create your views here.
class GenreListView(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(genres, request)

        serializer = GenreSerializer(page, many=True) if page is not None else GenreSerializer(genres, many=True)

        if page is not None:
            return paginator.get_paginated_response(serializer.data)

        return Response({"genres": serializer.data}, status=status.HTTP_200_OK)



class TagCategoryView(APIView):
    def get(self, request):
        tag_categories = TagCategory.objects.all()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(tag_categories, request)

        serializer = TagCategorySerializer(page, many=True) if page is not None else TagCategorySerializer(tag_categories, many=True)

        if page is not None:
            return paginator.get_paginated_response(serializer.data)

        return Response({"tag_categories": serializer.data}, status=status.HTTP_200_OK)