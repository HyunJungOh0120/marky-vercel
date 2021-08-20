from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError

from .models import MyUser

# Register your models here.


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = ('email', 'username', 'is_admin')
    list_filter = ('email', 'username', 'is_active', 'is_admin',)
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)


admin.site.register(MyUser, UserAdmin)
