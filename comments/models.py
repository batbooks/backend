from django.db import models
from django.contrib.auth import get_user_model
from forum.models import Thread

from book.models import Chapter,Book


class CommentAbstract(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='u_%(app_label)s_%(class)s')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='ch_%(app_label)s_%(class)s')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(get_user_model(), related_name='%(app_label)s_%(class)s_likes', blank=True)
    dislike = models.ManyToManyField(get_user_model(), related_name='%(app_label)s_%(class)s_dislikes', blank=True)


    class Meta:
        abstract = True
        ordering = ['-created']

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

    class Meta:
        unique_together = ('user', 'book')


    def __str__(self):
        return f"{self.user.name} - {self.book.name} ({self.rating})"


class Post(CommentAbstract):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')

    chapter = None
    def __str__(self):
        return f"{self.user.username} on {self.thread.name}: {self.body[:30]}"
