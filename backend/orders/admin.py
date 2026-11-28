from django.contrib import admin

from offers.models import Offer

from .models import Order, ServiceCategory


class OfferInline(admin.TabularInline):
    model = Offer
    extra = 0
    readonly_fields = ("contractor", "price", "proposed_date", "status", "created_at")
    can_delete = False


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "min_price", "max_price", "is_active")
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    search_fields = ("name",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
        "city",
        "status",
        "channel",
        "created_by",
        "contractor",
        "requested_date",
        "created_at",
    )
    list_filter = ("status", "channel", "category", "payment_method")
    search_fields = ("description", "city", "street", "recipient_name")
    raw_id_fields = ("created_by", "contractor")
    inlines = [OfferInline]
