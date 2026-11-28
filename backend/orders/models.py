from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
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
                condition=models.Q(max_price__isnull=True) | models.Q(max_price__gte=0),
                name="service_category_max_price_non_negative",
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


class Order(models.Model):
    class Status(models.TextChoices):
        AWAITING_OFFERS = "AWAITING_OFFERS", "Oczekuje na oferty"
        AWAITING_CONTRACTOR = "AWAITING_CONTRACTOR", "Oczekuje na wykonawcę"
        ASSIGNED = "ASSIGNED", "Przypisane"
        IN_PROGRESS = "IN_PROGRESS", "W trakcie realizacji"
        AWAITING_ACCEPTANCE = "AWAITING_ACCEPTANCE", "Oczekuje na akceptację"
        UNDER_CLARIFICATION = "UNDER_CLARIFICATION", "Do wyjaśnienia"
        COMPLAINT = "COMPLAINT", "Reklamacja"
        COMPLETED = "COMPLETED", "Zakończone"
        CANCELLED = "CANCELLED", "Anulowane"

    class Channel(models.TextChoices):
        WEB = "WEB", "Aplikacja"
        PHONE = "PHONE", "Telefon"

    class PaymentMethod(models.TextChoices):
        ONLINE = "ONLINE", "Płatność online"
        CASH = "CASH", "Gotówka"

    # TODO: przy usuwaniu konta (WU-03/RODO) anonimizować użytkownika zamiast fizycznego DELETE
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_orders",
        verbose_name="Zleceniodawca",
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Kategoria",
    )
    description = models.TextField(verbose_name="Opis")
    requested_date = models.DateField(verbose_name="Preferowany termin")
    # Przed akceptacją oferty wykonawca widzi jedynie pole city (ukrywanie w serializerach)
    street = models.CharField(max_length=150, verbose_name="Ulica")
    building_number = models.CharField(max_length=10, verbose_name="Numer budynku")
    apartment_number = models.CharField(
        max_length=10,
        blank=True,
        default="",
        verbose_name="Numer lokalu",
    )
    postal_code = models.CharField(
        max_length=6,
        validators=[RegexValidator(r"^\d{2}-\d{3}$")],
        verbose_name="Kod pocztowy",
    )
    city = models.CharField(max_length=100, verbose_name="Miasto")
    photo = models.ImageField(
        upload_to="orders/photos/%Y/%m/",
        blank=True,
        verbose_name="Zdjęcie",
    )
    channel = models.CharField(
        max_length=10,
        choices=Channel.choices,
        default=Channel.WEB,
        verbose_name="Kanał",
    )
    recipient_name = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Imię i nazwisko odbiorcy",
    )
    recipient_phone = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Telefon odbiorcy",
    )
    recipient_consent = models.BooleanField(
        default=False,
        verbose_name="Zgoda odbiorcy",
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PaymentMethod.choices,
        null=True,
        blank=True,
        default=None,
        verbose_name="Metoda płatności",
    )
    # TODO: przy usuwaniu konta (WU-03/RODO) anonimizować użytkownika zamiast fizycznego DELETE
    contractor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="assigned_orders",
        verbose_name="Wykonawca",
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.AWAITING_OFFERS,
        db_index=True,
        verbose_name="Status",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Utworzono")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Zaktualizowano")

    class Meta:
        verbose_name = "Zlecenie"
        verbose_name_plural = "Zlecenia"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=(models.Q(recipient_name="") & models.Q(recipient_phone=""))
                | models.Q(recipient_consent=True),
                name="order_recipient_consent_required",
            ),
        ]
        indexes = [
            models.Index(
                fields=["status", "category"], name="order_status_category_idx"
            ),
        ]

    def __str__(self) -> str:
        return (
            f"Zlecenie #{self.pk} - {self.category.name} ({self.get_status_display()})"
        )
