from django.contrib import admin

from .models import Favorite,Blocked
def all_books(book):
    return ", ".join(book.name for book in book.book.all())

all_books.short_description = "books"

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(Blocked)
class BlockedAdmin(admin.ModelAdmin):
    list_display = ['user',all_books]