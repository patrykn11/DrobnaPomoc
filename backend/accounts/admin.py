from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    fieldsets = UserAdmin.fieldsets + (
        ('Daty profilu', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = UserAdmin.readonly_fields + ('created_at', 'updated_at')

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dane użytkownika', {'fields': ('email', 'first_name', 'last_name')}),
    )
