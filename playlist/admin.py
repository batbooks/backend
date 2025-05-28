from django.contrib import admin
from .models import Playlist, PlaylistBook

class PlaylistBookInline(admin.TabularInline):
    model = PlaylistBook
    extra = 1
    autocomplete_fields = ['book']
    ordering = ['rank']

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at', 'genres', 'tags')
    search_fields = ('name', 'user__username')
    autocomplete_fields = ['user', 'tags', 'genres']
    inlines = [PlaylistBookInline]

    filter_horizontal = ('tags', 'genres')

@admin.register(PlaylistBook)
class PlaylistBookAdmin(admin.ModelAdmin):
    list_display = ('playlist', 'book', 'rank')
    list_filter = ('playlist',)
    search_fields = ('playlist__name', 'book__title')
    autocomplete_fields = ['playlist', 'book']
