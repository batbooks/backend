from django.contrib import admin
from django.db import transaction
from forum.models import Forum, Thread
from book.models import Book

@admin.action(description="Sync all Forums with their Books (bulk)")
def bulk_sync_forums(modeladmin, request, queryset):
    """
    Sync Forums with their related Books:
    - Create missing Forums
    - Bulk update existing Forums if Book info changed
    """
    with transaction.atomic():
        books = list(Book.objects.all())  # All books
        book_map = {book.id: book for book in books}

        forums = list(Forum.objects.filter(book_id__in=book_map.keys()))
        forum_map = {forum.book_id: forum for forum in forums}

        to_create = []
        to_update = []

        for book in books:
            forum = forum_map.get(book.id)
            if not forum:
                to_create.append(Forum(
                    book=book,
                    name=book.name,
                    description=book.description,
                    image=book.image
                ))
            else:
                # Check if fields differ
                if (forum.name != book.name or
                    forum.description != book.description or
                    forum.image != book.image):
                    forum.name = book.name
                    forum.description = book.description
                    forum.image = book.image
                    to_update.append(forum)

        if to_create:
            Forum.objects.bulk_create(to_create, batch_size=500)
        if to_update:
            Forum.objects.bulk_update(to_update, ['name', 'description', 'image'], batch_size=500)

    modeladmin.message_user(request, f"Forums synced: {len(to_create)} created, {len(to_update)} updated.")

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    actions = [bulk_sync_forums]  # ✅ Added action

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('name', 'forum', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'forum')
    search_fields = ('name',)
    ordering = ('-created_at',)
