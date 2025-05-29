from django_filters import rest_framework as filters
from book.models import Book
from rest_framework import generics
from book.serializers import BookSerializer
from rest_framework import filters as drf_filters
from .fIlters import BookFilter
from django.db.models import F, ExpressionWrapper, DecimalField, Count, IntegerField, When, Value,Case
from django.db.models.functions import Cast, Coalesce
from django.db.models.functions import Coalesce


class SearchView(generics.ListAPIView):
    queryset = Book.objects.annotate(
        avg_rating=Case(
            When(rating_count=0, then=Value(0.0)),
            default=ExpressionWrapper(
                Cast(F("rating_sum"), DecimalField(max_digits=10, decimal_places=2))
                / Cast(F("rating_count"), DecimalField(max_digits=10, decimal_places=2)),
                output_field=DecimalField(max_digits=5, decimal_places=2),
            ),
            output_field=DecimalField(max_digits=5, decimal_places=2),
        ),
        chapter_count=ExpressionWrapper(Count("chapters"), output_field=IntegerField()),
    )
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend, drf_filters.SearchFilter)
    filterset_class = BookFilter
    search_fields = ['name', 'description']
