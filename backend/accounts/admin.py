from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ContractorProfile, Role, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "roles_display",
        "is_staff",
    )
    list_filter = ("roles", "is_staff", "is_active")
    search_fields = (
        "username",
        "email",
        "phone_number",
        "first_name",
        "last_name",
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Role aplikacji", {"fields": ("roles", "phone_number")}),
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
                    "roles",
                )
            },
        ),
    )

    @admin.display(description="Role")
    def roles_display(self, user):
        return ", ".join(user.roles.values_list("code", flat=True))

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        client_role, _ = Role.objects.get_or_create(code=Role.Code.CLIENT)
        form.instance.roles.add(client_role)


@admin.register(ContractorProfile)
class ContractorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "service_radius_km")
    search_fields = ("user__username", "user__email", "city")
