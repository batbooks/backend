from django.contrib import admin

from .models import Message ,UserChannel,Group,GroupMessage


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['from_user','to_user','message','date','has_been_seen']

@admin.register(UserChannel)
class UserChannelAdmin(admin.ModelAdmin):
    list_display = ['user','channel']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(GroupMessage)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['group','message','sender','date']