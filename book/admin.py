from django.contrib import admin
from django.urls import reverse
from django.utils.html import mark_safe, escape
from .models import Book, Chapter

@admin.action(description='Fix chapter numbers for selected books')
def fix_chapter_numbers(modeladmin, request, queryset):
    for book in queryset:
        chapters = Chapter.objects.filter(book=book).order_by('created_at')
        for idx, chapter in enumerate(chapters, start=1):
            if chapter.chapter_num != idx:
                chapter.chapter_num = idx
                chapter.save(update_fields=['chapter_num'])
    modeladmin.message_user(request, "Chapter numbers updated successfully.")

def all_tags(book):
    return ", ".join(tag.title for tag in book.tags.all())
all_tags.short_description = "Tags"

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'Author', 'status', 'rating_sum', 'rating_count', 'created_at', 'updated_at', all_tags)
    list_filter = ('status', 'genres', 'tags__category__title', 'Author')
    search_fields = ('name', 'Author__username', 'description', 'tags__title', 'tags__category__title')
    ordering = ('name',)
    filter_horizontal = ('tags', 'genres')
    list_per_page = 10
    actions = [fix_chapter_numbers]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image', 'status', 'rating_sum', 'rating_count', 'Author')
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
class ChapterAdmin(admin.ModelAdmin):
    def Book_link(self, obj):
        link = reverse("admin:book_book_change", args=[obj.book.id])
        return mark_safe(f'<a href="{link}">{escape(obj.book.__str__())}</a>')

    Book_link.short_description = 'Book'

    list_display = ['title', 'chapter_num', 'show_body', 'is_approved', 'updated_at', 'Book_link']
    search_fields = ['title', 'book__name']
    filter_horizontal = ()
    list_filter = ['is_approved']