from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


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
