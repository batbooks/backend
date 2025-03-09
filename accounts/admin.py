from django.contrib import admin
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    readonly_fields = ['joined_date']
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email', 'name', 'is_admin', 'last_login']
    list_filter = ['is_admin']
    fieldsets = [
        (None, {
            "fields": ['email', 'password'],
        }), (
            "Personal Info", {"fields": ['name', 'last_login','joined_date']}
        ),
        ("Permissions", {"fields": ["is_admin"]}),

    ]
    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')

        })
    ]
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
