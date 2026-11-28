from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.validators import MinValueValidator
from django.db import models, transaction


class Role(models.Model):
    class Code(models.TextChoices):
        CLIENT = "client", "Zleceniodawca"
        CONTRACTOR = "contractor", "Wykonawca"
        CONSULTANT = "consultant", "Konsultant"

    code = models.CharField(max_length=20, choices=Code.choices, unique=True)

    def __str__(self):
        return self.get_code_display()


class UserManager(DjangoUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        with transaction.atomic(using=self.db):
            user = super()._create_user(username, email, password, **extra_fields)
            client_role, _ = Role.objects.db_manager(self.db).get_or_create(
                code=Role.Code.CLIENT
            )
            user.roles.add(client_role)
        return user


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    roles = models.ManyToManyField(Role, related_name="users", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def has_role(self, role_code):
        return self.roles.filter(code=role_code).exists()

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
