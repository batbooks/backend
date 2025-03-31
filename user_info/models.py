from django.db import models
from django.conf import settings
# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_info')
    bio = models.TextField()
    gender = models.CharField(max_length=10,choices=[('male','male'),('female','female')])
    image = models.ImageField(upload_to='users/%Y/%m/%d/',null=True,blank=True)


class UserFollow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower}'
