from django.contrib import admin
from forum.models import Forum, Thread

# Register your models here.
@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('name', 'forum', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'forum')
    search_fields = ('name',)
    ordering = ('-created_at',)