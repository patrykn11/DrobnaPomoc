from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nazwa",
    )
    min_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Cena minimalna (zł)",
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    max_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Cena maksymalna (zł)",
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktywna",
    )

    class Meta:
        verbose_name = "Kategoria usługi"
        verbose_name_plural = "Kategorie usług"
        ordering = ["name"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(min_price__isnull=True) | models.Q(min_price__gte=0),
                name="service_category_min_price_non_negative",
            ),
            models.CheckConstraint(
                condition=models.Q(max_price__isnull=True)
                | models.Q(min_price__isnull=True)
                | models.Q(max_price__gte=models.F("min_price")),
                name="service_category_max_price_gte_min_price",
            ),
        ]

    def __str__(self) -> str:
        return self.name
