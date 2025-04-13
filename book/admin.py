from django.contrib import admin
from  .models import Book , Chapter
from django.urls import reverse
from django.utils.html import mark_safe,escape


def all_tags(book):
    return ", ".join(tag.title for tag in book.tags.all())

# Set a short description for the admin panel
all_tags.short_description = "Tags"

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'Author', 'status','rating_sum','rating_count', 'created_at', 'updated_at', all_tags)
    list_filter = ('status', 'genres', 'tags__category__title', 'Author')
    search_fields = ('name', 'Author__username', 'description', 'tags__title', 'tags__category__title')
    ordering = ('name',)
    filter_horizontal = ('tags', 'genres')
    list_per_page = 10

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image', 'status', 'rating_sum','rating_count', 'Author')
        }),
        ('Categories and Tags', {
            'fields': ('tags', 'genres')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Chapter)
class BookAdmin(admin.ModelAdmin):
    def Book_link(self, obj):
        link = reverse("admin:book_book_change", args=[obj.book.id])  # model name has to be lowercase
        return mark_safe(f'<a href="{link}">{escape(obj.book.__str__())}</a>')


    Book_link.allow_tags = True
    list_display = ['title','show_body','is_approved','updated_at','Book_link',]
    filter_horizontal = ()
    list_filter = ['is_approved']
