from django.db import models
from accounts.models import User
from  book.models import Book

class Forum(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='forum')
    name = models.CharField(max_length=256)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='books/%Y/%m/%d', null=True, blank=True)

    class Meta:
        ordering = ['created_at','name']

    def __str__(self):
        return self.name


class Thread(models.Model):

    STATUS_OPEN = 'O'
    STATUS_CLOSED = 'C'

    STATUS_CHOICE = [
       (STATUS_OPEN, 'Open'),
       (STATUS_CLOSED, 'Closed')
   ]

    forum = models.ForeignKey(Forum, related_name='threads', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    status = models.CharField(choices=STATUS_CHOICE, max_length=1)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name









