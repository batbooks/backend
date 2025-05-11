from django.contrib import admin

from chat import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['from_user','to_user','message','date','has_been_seen']