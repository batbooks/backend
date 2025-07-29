from django.db import models
from book.models import Book
from django.utils import timezone

# Create your models here.



class BookStatsSnapshot(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='stats_snapshots')
    date = models.DateField(default=timezone.now)

    reviews_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    favorites_count = models.IntegerField(default=0)
    blocks_count = models.IntegerField(default=0)
    avg_comment_likes = models.FloatField(default=0.0)

    class Meta:
        unique_together = ['book', 'date']