from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review
from book_actions.models import Rating


@receiver(post_save, sender=Review)
def create_rating(sender, instance, created, **kwargs):
    if created:
        Rating.objects.create(user=instance.user, book=instance.book,rating=instance.rating)


@receiver(post_delete, sender=Review)
def update_book_rating_on_delete(sender, instance, **kwargs):
    instance.book.book_rating.get(user=instance.user,book=instance.book).delete()

