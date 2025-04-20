from django_filters import rest_framework as filters
from book.models import Book
from django.db.models import Count, Q, QuerySet


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class BookFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    date = filters.DateFromToRangeFilter(field_name='created_at')
    user = filters.CharFilter(field_name='Author__name', lookup_expr='icontains')
    rating = filters.RangeFilter(field_name='avg_rating')
    number_rating = filters.RangeFilter(field_name='rating_count')
    favorite_count = filters.NumericRangeFilter(method='filter_by_favorite_count')
    chapter_count = filters.RangeFilter(field_name='chapter_count')
    status = filters.CharFilter(field_name='status', lookup_expr='icontains')
    tag_or = filters.CharFilter(method='filter_by_tag_or')
    genre_or = filters.CharFilter(method='filter_by_genre_or')
    tag_and = filters.CharFilter(method='filter_by_tag_and')
    genre_and = filters.CharFilter(method='filter_by_genre_and')
    ordering = filters.OrderingFilter(fields=(
        ('updated_at', 'updated_at'),
        ('created_at', 'created_at'),
        ('name', 'name'),
        ('avg_rating', 'avg_rating'),
        ('rating_count', 'rating_count'),
        ('chapter_count', 'chapter_count')
    ))

    class Meta:
        model = Book
        fields = ['name', 'description', 'date', 'user', 'rating', 'number_rating', 'favorite_count', 'chapter_count',
                  'tag_or', 'genre_or', 'tag_and', 'genre_and', 'status']

    def filter_by_favorite_count(self, queryset, name, value):
        queryset_qs = queryset.annotate(favorite_count=Count('favorite_groups'))

        if value.start and value.stop:
            return queryset_qs.filter(Q(favorite_count__gte=value.start) & Q(favorite_count__lte=value.stop))
        elif value.start:
            return queryset_qs.filter(Q(favorite_count__gte=value.start))
        elif value.stop:
            return queryset_qs.filter(Q(favorite_count__lte=value.stop))

    def filter_by_tag_or(self, queryset, name, value):
        tags = value.split(',')
        q = Q()
        for tag in tags:
            q |= Q(tags__id=int(tag))
        return queryset.filter(q).distinct()

    def filter_by_genre_or(self, queryset, name, value):
        genres = value.split(',')
        q = Q()
        for genre in genres:
            q |= Q(genres__id=int(genre))
        return queryset.filter(q).distinct()

    def filter_by_tag_and(self, queryset, name, value):
        tags = value.split(',')
        for tag in tags:
            queryset = queryset.filter(tags__id=int(tag))
        return queryset.distinct()

    def filter_by_genre_and(self, queryset, name, value):
        genres = value.split(',')
        for genre in genres:
            queryset = queryset.filter(genres__id=int(genre))
        return queryset.distinct()
