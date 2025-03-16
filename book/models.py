from django.db import models

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
    rating = models.DecimalField(max_digits=2,decimal_places=1)
    status = models.CharField(choices=STATUS_CHOICE,max_length=256)

    class Meta:
        ordering = ['rating', 'name']


