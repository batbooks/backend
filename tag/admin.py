from django.contrib import admin
from .models import Genre, Tag,TagCategory

@admin.register(TagCategory)
class TagCategoryAdmin(admin.ModelAdmin):
    list_display = ("title","description")
    search_fields = ("title",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("title","description")
    search_fields = ("title",)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "description")
    search_fields = ("title", "category__title")
    list_filter = ("category",)
