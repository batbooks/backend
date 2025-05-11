from django.contrib import admin

from .models import Message ,UserChannel


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['from_user','to_user','message','date','has_been_seen']

@admin.register(UserChannel)
class UserChannelAdmin(admin.ModelAdmin):
    list_display = ['user','channel']
