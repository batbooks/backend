from django.contrib import admin

from .models import UserInfo, UserFollow,UserNotInterested


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'gender']


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following','created_at']

@admin.register(UserNotInterested)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ['user','not_interested', 'created_at']
