from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from user_info.models import UserNotInterested
from book_actions.models import Blocked
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