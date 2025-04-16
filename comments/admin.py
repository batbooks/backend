from django.contrib import admin

from .models import Comment,Review,Post


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','body','like_counter','dislike_counter','reply_counter','tag']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user','body','like_counter','dislike_counter','rating','book','chapter']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'thread', 'created')
    search_fields = ('body', 'user__username', 'thread__name')
    list_filter = ('created', 'thread')
    ordering = ('-created',)