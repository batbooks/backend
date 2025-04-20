from django_filters import rest_framework as filters
from book.models import Book
from django.db.models import Count ,  Q


class BookFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    date = filters.DateFromToRangeFilter(field_name='created_at')
    user = filters.CharFilter(field_name='Author__name', lookup_expr='icontains')
    rating = filters.RangeFilter(field_name='avg_rating')
    number_rating = filters.RangeFilter(field_name='rating_count')
    favorite_count = filters.NumericRangeFilter(method='filter_by_favorite_count')

    class Meta:
        model = Book
        fields = ['name', 'description', 'date', 'user', 'rating', 'number_rating', 'favorite_count']

    def filter_by_favorite_count(self, queryset, name, value):
        print("hello iam mahi")
        print(value.start)
        print(value.stop)

        queryset_qs = queryset.annotate(favorite_count=Count('favorite_groups'))
        # for i in range(11):
        #     print("#" * 20, i)
        #     print(queryset.annotate(favorite_count=Count('favorite_groups'))[i].favorite_count)
        if value.start and value.stop:
            return queryset_qs.filter(Q(favorite_count__gte=value.start) & Q(favorite_count__lte=value.stop))
        elif value.start:
            return queryset_qs.filter(Q(favorite_count__gte=value.start))
        elif value.stop:
            return queryset_qs.filter(Q(favorite_count__lte=value.stop))

