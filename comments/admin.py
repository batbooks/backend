from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','body','is_approved','like_counter','dislike_counter','reply_counter']
    list_filter = ['is_approved']