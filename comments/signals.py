from django.db.models.signals import post_save, post_delete , pre_delete
from django.dispatch import receiver
from .models import Review
from django.db import transaction


@receiver(post_delete, sender=Review)
def update_book_rating_on_delete(sender, instance, **kwargs):
    instance.book.book_rating.get(user=instance.user,book=instance.book).delete()

    # transaction.on_commit(lambda: book.save())
