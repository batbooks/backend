from django.db import models
from django.conf import settings
# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_info')
    bio = models.TextField()
    gender = models.CharField(max_length=10,choices=[('male','male'),('female','female')])
