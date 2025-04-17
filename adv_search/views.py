from django_filters import rest_framework as filters
from book.models import Book
from rest_framework import generics
from book.serializers import BookSerializer
from rest_framework import filters as drf_filters
from .fIlters import ProductFilter

class SearchView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend, drf_filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
