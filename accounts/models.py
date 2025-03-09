from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager
import random
class User(AbstractBaseUser):
    email = models.EmailField(max_length=320, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    joined_date = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, perms):
        return True


    def set_name(self,email):
        email_split = email.split('@')
        self.name = email_split[0] + '.' + email_split[1][0]



    @property
    def is_staff(self):
        return self.is_admin


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        return str(random.randint(100000, 999999))