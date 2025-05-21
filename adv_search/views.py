om django_filters import rest_framework as filters
from book.models import Book
from rest_framework import generics
from book.serializers import BookSerializer
from rest_framework import filters as drf_filters
from .fIlters import BookFilter
from django.db.models import F, ExpressionWrapper, DecimalField,Count,IntegerField
from django.db.models.functions import Cast , Coalesce
from django.db.models.functions import Coalesce

class SearchView(generics.ListAPIView):
    queryset = Book.objects.annotate(
        avg_rating=ExpressionWrapper(
            Cast(Coalesce(F('rating_sum'), 0), DecimalField()) /
            Cast(Coalesce(F('rating_count'), 1), DecimalField()),  # جلوگیری از تقسیم بر صفر
            output_field=DecimalField()
        ),
        chapter_count=ExpressionWrapper(
            Count('chapters'),
            output_field=IntegerField()
        )
    )
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend, drf_filters.SearchFilter)
    filterset_class = BookFilter
    search_fields = ['name', 'description']