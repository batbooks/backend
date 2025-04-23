from django.db.models.signals import post_save, post_delete , pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import transaction
from user_info.models import UserNotInterested
from .models import Blocked, Rating
from book.models import Book

User = get_user_model()


@receiver(post_save, sender=UserNotInterested)
def add_blocked_books(sender, instance, created, **kwargs):
    if created:
        blocker = instance.user
        blocked_user = instance.not_interested
        blocked_books = Book.objects.filter(Author=blocked_user)

        blocked_obj, _ = Blocked.objects.get_or_create(user=blocker)
        blocked_obj.book.add(*blocked_books)


@receiver(post_delete, sender=UserNotInterested)
def remove_blocked_books(sender, instance, **kwargs):
    blocker = instance.user
    unblocked_user = instance.not_interested
    unblocked_books = Book.objects.filter(Author=unblocked_user)

    try:
        blocked_obj = Blocked.objects.get(user=blocker)
        blocked_obj.book.remove(*unblocked_books)
    except Blocked.DoesNotExist:
        pass


@receiver(post_save, sender=Rating)
def update_book_rating_on_create(sender, instance, created, **kwargs):
    if created:
        book = instance.book
        book.rating_count += 1
        book.rating_sum += float(instance.rating)
        transaction.on_commit(lambda: book.save())


@receiver(post_delete, sender=Rating)
def update_book_rating_on_delete(sender, instance, **kwargs):
    book = instance.book
    if book.rating_count > 0:
        book.rating_count -= 1
    book.rating_sum -= float(instance.rating)
    if book.rating_sum<0:
        book.rating_sum = 0

    transaction.on_commit(lambda: book.save())

