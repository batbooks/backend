from django.contrib import admin
from  .models import Book , Chapter
from django.urls import reverse
from django.utils.html import mark_safe,escape

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name','created_at','updated_at','status','rating','Author']



@admin.register(Chapter)
class BookAdmin(admin.ModelAdmin):
    def Book_link(self, obj):
        link = reverse("admin:book_book_change", args=[obj.book.id])  # model name has to be lowercase
        return mark_safe(f'<a href="{link}">{escape(obj.book.__str__())}</a>')

    Book_link.allow_tags = True
    list_display = ['title','show_body','is_approved','updated_at','Book_link']
    filter_horizontal = ()
    list_filter = ['is_approved']
