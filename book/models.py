from django.db import models
from accounts.models import User
from tag.models import Tag,Genre
from django.db.models import Avg



# Create your models here.

class Book(models.Model):

    STATUS_ONGOING = 'O'
    STATUS_COMPLETE = 'C'
    MEMBERSHIP_HIATUS = 'H'

    STATUS_CHOICE = [
        (STATUS_ONGOING, 'ongoing'),
        (STATUS_COMPLETE, 'complete'),
        (MEMBERSHIP_HIATUS, 'hiatus'),
    ]

    name = models.CharField(max_length=256)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='books/%Y/%m/%d', null=True, blank=True)

    status = models.CharField(choices=STATUS_CHOICE,max_length=256)
    Author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='books')
    tags = models.ManyToManyField(Tag, related_name='books', blank=True)
    genres = models.ManyToManyField(Genre, related_name='books', blank=True)

    rating_sum = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)

    @property
    def rating_avg(self):
        if self.rating_count == 0:
            return 0
        return self.rating_sum / self.rating_count

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name





class Chapter(models.Model):

    title = models.CharField(max_length=256)
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='chapters')
    body = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['book', 'title']

    def show_body(self):
        return self.body[:30]

    def __str__(self):
        return self.title






