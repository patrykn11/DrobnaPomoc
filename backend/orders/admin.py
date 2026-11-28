from django.contrib import admin

from .models import ServiceCategory


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "min_price", "max_price", "is_active")
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    search_fields = ("name",)

