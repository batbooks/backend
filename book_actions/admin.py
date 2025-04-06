from django.contrib import admin

from .models import Favorite,Blocked


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user',]


@admin.register(Blocked)
class BlockedAdmin(admin.ModelAdmin):
    list_display = ['user',]