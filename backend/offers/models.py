import secrets
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


def generate_visit_code() -> str:
    return f"{secrets.randbelow(10000):04d}"


class Offer(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Złożona"
        WITHDRAWN = "WITHDRAWN", "Wycofana"
        REJECTED = "REJECTED", "Odrzucona"
        ACCEPTED = "ACCEPTED", "Zaakceptowana"

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.PROTECT,
        related_name="offers",
        verbose_name="Zlecenie",
    )
    # TODO: ContractorProfile (feat/contractor-verification)
    # TODO: przy usuwaniu konta (WU-03/RODO) anonimizować użytkownika zamiast fizycznego DELETE
    contractor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="offers",
        verbose_name="Wykonawca",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name="Cena (zł)",
    )
    proposed_date = models.DateField(verbose_name="Proponowany termin")
    comment = models.TextField(
        blank=True,
        default="",
        verbose_name="Komentarz",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED,
        verbose_name="Status",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Utworzono")

    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Oferty"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gt=0),
                name="check_offer_price_positive",
            ),
            models.UniqueConstraint(
                fields=["order"],
                condition=models.Q(status="ACCEPTED"),
                name="unique_accepted_offer_per_order",
            ),
            models.UniqueConstraint(
                fields=["order", "contractor"],
                condition=~models.Q(status="WITHDRAWN"),
                name="unique_active_offer_per_contractor",
            ),
        ]

    def __str__(self) -> str:
        return f"Oferta #{self.pk} do zlecenia #{self.order_id} ({self.price} zł)"


class Visit(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Zaplanowana"
        IN_PROGRESS = "IN_PROGRESS", "W trakcie"
        COMPLETED = "COMPLETED", "Zakończona"
        CANCELLED = "CANCELLED", "Anulowana"

    offer = models.ForeignKey(
        Offer,
        on_delete=models.PROTECT,
        related_name="visits",
        verbose_name="Oferta",
    )
    scheduled_date = models.DateField(verbose_name="Zaplanowana data")
    code = models.CharField(
        max_length=4,
        default=generate_visit_code,
        editable=False,
        validators=[RegexValidator(r"^\d{4}$")],
        verbose_name="Kod wizyty",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
        verbose_name="Status",
    )
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        verbose_name="Rozpoczęto",
    )
    finished_at = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        verbose_name="Zakończono",
    )
    cancel_reason = models.TextField(
        blank=True,
        default="",
        verbose_name="Powód anulowania",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Utworzono")

    class Meta:
        verbose_name = "Wizyta"
        verbose_name_plural = "Wizyty"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(code__regex=r"^\d{4}$"),
                name="check_visit_code_4_digits",
            ),
            models.CheckConstraint(
                condition=~models.Q(status="CANCELLED") | ~models.Q(cancel_reason=""),
                name="check_cancel_reason_when_cancelled",
            ),
            models.CheckConstraint(
                condition=models.Q(started_at__isnull=True)
                | models.Q(finished_at__isnull=True)
                | models.Q(finished_at__gte=models.F("started_at")),
                name="check_visit_finished_at_gte_started_at",
            ),
            models.UniqueConstraint(
                fields=["offer"],
                condition=~models.Q(status="CANCELLED"),
                name="unique_active_visit_per_offer",
            ),
        ]

    def __str__(self) -> str:
        return f"Wizyta #{self.pk} do oferty #{self.offer_id} ({self.get_status_display()})"
