from django.contrib import admin
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,OTP
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    readonly_fields = ['joined_date']
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email', 'name', 'is_active', 'last_login','id']
    list_filter = ['is_admin']
    fieldsets = [
        (None, {
            "fields": ['email', 'password'],
        }), (
            "Personal Info", {"fields": ['name', 'last_login','joined_date','is_active']}
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

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user','code']