from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from paginations import CustomPagination
from tag.models import TagCategory, Tag, Genre


# Create your views here.
class GenreListView(APIView):
    def get(self, request):
        genres = Genre.objects.values_list('title', flat=True)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(genres, request)

        if page is not None:
            return paginator.get_paginated_response(list(page))

        return Response({"genres": list(genres)}, status=status.HTTP_200_OK)


class TagCategoryView(APIView):
    def get(self, request):
        tag_categories = TagCategory.objects.all()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(tag_categories, request)

        def format_category(category):
            return {
                "category": category.title,
                "tags": list(category.tags.values_list('title', flat=True))
            }

        if page is not None:
            return paginator.get_paginated_response([format_category(c) for c in page])

        return Response({"tag_categories": [format_category(c) for c in tag_categories]}, status=status.HTTP_200_OK)