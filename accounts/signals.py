from django.db.models.signals import post_save
from django.dispatch import receiver
from user_info.models import UserInfo
from django.contrib.auth import get_user_model
from book_actions.models import Favorite

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created :
        UserInfo.objects.create(user=instance,gender='',bio='')
        Favorite.objects.create(user=instance)