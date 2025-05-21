from django.db import models
from django.contrib.auth import get_user_model
from book.models import Book
from playlist.models import Playlist

class Favorite(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    book = models.ManyToManyField(Book,related_name='favorite_groups')

class Blocked(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    book = models.ManyToManyField(Book,related_name='blocked_groups')

class Rating(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,related_name='user_rating')
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='book_rating')
    rating = models.DecimalField(max_digits=2,decimal_places=1)


class FavoritePlaylist(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    playlist = models.ManyToManyField(Playlist,related_name='favorite_playlist')
