from decimal import Decimal

from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import ServiceCategory


class ServiceCategoryModelTest(TestCase):
    def test_seed_categories_exist(self):
        """Seed migration should create 6 initial service categories."""
        expected_names = [
            "Hydraulika",
            "Elektryka",
            "Drobne naprawy",
            "Sprzątanie",
            "Zakupy",
            "Prace w ogrodzie",
        ]
        categories = ServiceCategory.objects.filter(name__in=expected_names)
        self.assertEqual(categories.count(), 6)

    def test_str_representation(self):
        category = ServiceCategory.objects.create(name="Malowanie")
        self.assertEqual(str(category), "Malowanie")

    def test_max_price_less_than_min_price_raises_error(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ServiceCategory.objects.create(
                    name="Błędna kategoria",
                    min_price=Decimal("150.00"),
                    max_price=Decimal("100.00"),
                )

    def test_negative_min_price_raises_error(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ServiceCategory.objects.create(
                    name="Ujemna kategoria",
                    min_price=Decimal("-10.00"),
                )

