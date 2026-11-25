from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ContractorProfile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "role",
        "is_staff",
    )
    list_filter = ("role", "is_staff", "is_active")
    search_fields = (
        "username",
        "email",
        "phone_number",
        "first_name",
        "last_name",
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Typ konta", {"fields": ("role", "phone_number")}),
        ("Daty profilu", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = UserAdmin.readonly_fields + ("created_at", "updated_at")

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Dane użytkownika",
            {
                "fields": (
                    "email",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "role",
                )
            },
        ),
    )


@admin.register(ContractorProfile)
class ContractorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "service_radius_km")
    search_fields = ("user__username", "user__email", "city")
