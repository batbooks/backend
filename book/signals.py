from django.db.models.signals import post_save , post_migrate
from django.dispatch import receiver
from book.models import Book,Chapter
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

@receiver(post_save, sender=Chapter)
def update_book_timestamp(sender, instance, **kwargs):
    instance.book.save()
