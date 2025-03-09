from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager

class User(AbstractBaseUser):
    email = models.EmailField(max_length=320, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, perms):
        return True

    def save(self, *args, **kwargs):
        email_split = self.email.split('@')
        self.name = email_split[0] + '.' + email_split[1][0]
        super().save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.is_admin
