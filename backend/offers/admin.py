from django.contrib import admin

from .models import Offer, Visit


class VisitInline(admin.TabularInline):
    model = Visit
    extra = 0
    readonly_fields = ("code", "created_at")
    can_delete = False


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
    list_select_related = ("order", "order__category", "contractor")
    raw_id_fields = ("order", "contractor")
    inlines = [VisitInline]


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "offer",
        "scheduled_date",
        "status",
        "started_at",
        "finished_at",
    )
    list_filter = ("status",)
    list_select_related = ("offer",)
    raw_id_fields = ("offer",)
    readonly_fields = ("code", "created_at")
