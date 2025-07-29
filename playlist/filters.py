from django_filters import rest_framework as filters
from .models import Playlist  # Ensure you're importing Playlist model
from django.db.models import Q

class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class PlaylistFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    date = filters.DateFromToRangeFilter(field_name='created_at')
    user = filters.CharFilter(field_name='user__name', lookup_expr='icontains')
    book_count = filters.RangeFilter(field_name='book_count')
    tag_or = filters.CharFilter(method='filter_by_tag_or')
    genre_or = filters.CharFilter(method='filter_by_genre_or')
    tag_and = filters.CharFilter(method='filter_by_tag_and')
    genre_and = filters.CharFilter(method='filter_by_genre_and')
    ordering = filters.OrderingFilter(fields=(
        ('updated_at', 'updated_at'),
        ('created_at', 'created_at'),
        ('name', 'name'),
        ('book_count', 'book_count')
    ))

    class Meta:
        model = Playlist  # Change from Book to Playlist
        fields = ['name', 'description', 'date', 'user', 'book_count',
                  'tag_or', 'genre_or', 'tag_and', 'genre_and']

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
