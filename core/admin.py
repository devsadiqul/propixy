from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('name', 'email', 'phone', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_active', 'is_email_verified', 'created_at')
    search_fields = ('name', 'email', 'phone')
    ordering = ('-created_at',)

    fieldsets = (
        ('Personal Info', {
            'fields': ('name', 'email', 'phone', 'image')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Account Status', {
            'fields': ('is_email_verified', 'last_login', 'date_joined', 'created_at', 'updated_at')
        }),
    )

    readonly_fields = ('last_login', 'date_joined', 'created_at', 'updated_at')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'phone', 'password1', 'password2'),
        }),
    )