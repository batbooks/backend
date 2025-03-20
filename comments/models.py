from django.db import models
from django.contrib.auth import get_user_model

from book.models import Chapter


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='comments')
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    like = models.ManyToManyField(get_user_model(), related_name='likes', blank=True)
    dislike = models.ManyToManyField(get_user_model(),related_name='dislikes', blank=True)


    def like_counter(self):
        return self.like.all().count()

    def dislike_counter(self):
        return self.dislike.all().count()

    def reply_counter(self):
        return self.replies.all().count()

    def __str__(self):
        return self.body
