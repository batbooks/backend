from django.db import models
from django.contrib.auth import get_user_model

from book.models import Chapter,Book


class CommentAbstract(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='u_comments')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='c_comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(get_user_model(), related_name='likes', blank=True)
    dislike = models.ManyToManyField(get_user_model(), related_name='dislikes', blank=True)

    class Meta:
        abstract = True

    def like_counter(self):
        return self.like.all().count()

    def dislike_counter(self):
        return self.dislike.all().count()


class Comment(CommentAbstract):
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)
    tag = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='r_user', blank=True, null=True)

    def reply_counter(self):
        return self.replies.all().count()

    def __str__(self):
        return self.body


class Review(CommentAbstract):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    last_read_chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, blank=True, related_name='last_read_by')

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.name} - {self.book.name} ({self.rating})"
