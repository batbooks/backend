from django.db import models
from accounts.models import User
from tag.models import Tag,Genre
from django.db.models import Avg


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
    chapter_num = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['book', 'chapter_num']


    def save(self, *args, **kwargs):
        if self.chapter_num is None:
            last_chapter = Chapter.objects.filter(book=self.book).order_by('-chapter_num').first()
            if last_chapter:
                self.chapter_num = last_chapter.chapter_num + 1
            else:
                self.chapter_num = 1
        super().save(*args, **kwargs)

    def show_body(self):
        return self.body[:30]

    def __str__(self):
        return self.title




class UserBookProgress(models.Model):
    STATUS_READING = 'reading'
    STATUS_COMPLETED = 'completed'
    STATUS_DROPPED = 'dropped'
    STATUS_PLAN_TO_READ = 'plan_to_read'
    STATUS_ON_HOLD = 'on_hold'

    STATUS_CHOICES = [
        (STATUS_READING, 'Reading'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_DROPPED, 'Dropped'),
        (STATUS_PLAN_TO_READ, 'Plan to Read'),
        (STATUS_ON_HOLD, 'On Hold'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_progress')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='user_progress')
    last_read_chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, blank=True, related_name='last_read_by_users')
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_PLAN_TO_READ)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.name} - {self.book.name} ({self.status})"












