from django.contrib import admin
from .models import Genre, Tag,TagCategory
# Register your models here.

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
    list_display = ("title", "category", "description")  # Use "category" instead of "tags"
    search_fields = ("title", "category__title")  # Search by the title of the related category
    list_filter = ("category",)  # Filter by category
