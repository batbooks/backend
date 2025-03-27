from django.db import models
from accounts.models import User
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
    rating = models.DecimalField(max_digits=2,decimal_places=1)
    status = models.CharField(choices=STATUS_CHOICE,max_length=256)
    Author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='books')

    class Meta:
        ordering = ['rating', 'name']

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        # The 'reviews' is the reverse relation to the Book model in Review
        return self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0




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






