from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        UNDEFINED = "undefined", "Nieokreślona"
        CLIENT = "client", "Zleceniodawca"
        CONTRACTOR = "contractor", "Wykonawca"
        CONSULTANT = "consultant", "Konsultant"

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.UNDEFINED, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_full_name() or self.username


class ContractorProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="contractor_profile"
    )
    description = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True, db_index=True)
    service_radius_km = models.PositiveIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f"Profil wykonawcy: {self.user}"
