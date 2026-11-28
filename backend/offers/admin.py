from django.contrib import admin

from .models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "contractor",
        "price",
        "proposed_date",
        "status",
        "created_at",
    )
    list_filter = ("status",)
    raw_id_fields = ("order", "contractor")
