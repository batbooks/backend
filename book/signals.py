# signals.py

from django.db.models.signals import post_save , post_migrate
from django.dispatch import receiver
from .models import Book
from forum.models import Forum


@receiver(post_save, sender=Book)
def create_forum_for_book(sender, instance, created, **kwargs):
    if created:
        Forum.objects.create(
            book=instance,
            name=instance.name,
            description=instance.description,
            image=instance.image
        )

