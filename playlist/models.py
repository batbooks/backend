from django.db import models
from book.models import Book
from tag.models import Tag,Genre
from accounts.models import User

# Create your models here.

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField('tag.Tag', blank=True, related_name='playlists')
    genres = models.ManyToManyField('tag.Genre', blank=True, related_name='playlists')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.name}"



class PlaylistBook(models.Model):
    playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE)
    rank = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('playlist', 'book')
        ordering = ['rank']

    def save(self, *args, **kwargs):
        if self.rank is None:
            last_rank = (
                PlaylistBook.objects.filter(playlist=self.playlist)
                .aggregate(models.Max('rank'))['rank__max']
            )
            self.rank = 1 if last_rank is None else last_rank + 1
        super().save(*args, **kwargs)


Playlist.books = models.ManyToManyField(Book, through=PlaylistBook, related_name='in_playlists')