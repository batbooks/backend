from django.db import models
from django.contrib.auth import get_user_model
from book.models import Book

# Create your models here.
class Favorite(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    book = models.ManyToManyField(Book,related_name='favorite_groups')

class Blocked(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    book = models.ManyToManyField(Book,related_name='blocked_groups')

