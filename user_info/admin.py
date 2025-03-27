from django.contrib import admin

from .models import UserInfo


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user','bio','gender']