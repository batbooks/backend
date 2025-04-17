from django_filters import rest_framework as filters
from book.models import Book

class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['name', 'description']
