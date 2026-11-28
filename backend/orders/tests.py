from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Order, ServiceCategory

User = get_user_model()


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
                    name="Ujemna kategoria min",
                    min_price=Decimal("-10.00"),
                )

    def test_negative_max_price_raises_error(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ServiceCategory.objects.create(
                    name="Ujemna kategoria max",
                    max_price=Decimal("-10.00"),
                )


class OrderModelTest(TestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(
            username="klient1",
            email="klient1@example.com",
            password="password123",
            first_name="Jan",
            last_name="Kowalski",
        )
        self.category = ServiceCategory.objects.get(name="Hydraulika")

    def _base_order_kwargs(self, **overrides):
        data = {
            "created_by": self.client_user,
            "category": self.category,
            "description": "Cieknący kran w kuchni",
            "requested_date": date(2026, 12, 1),
            "street": "Marszałkowska",
            "building_number": "10",
            "postal_code": "00-001",
            "city": "Warszawa",
        }
        data.update(overrides)
        return data

    def test_order_defaults(self):
        order = Order.objects.create(**self._base_order_kwargs())
        self.assertEqual(order.status, Order.Status.AWAITING_OFFERS)
        self.assertEqual(order.channel, Order.Channel.WEB)
        self.assertIsNone(order.payment_method)
        self.assertIsNone(order.contractor)
        self.assertFalse(order.recipient_consent)

    def test_order_with_recipient_name_without_consent_raises_error(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Order.objects.create(
                    **self._base_order_kwargs(
                        recipient_name="Anna Nowak",
                        recipient_consent=False,
                    )
                )

    def test_order_with_recipient_phone_without_consent_raises_error(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Order.objects.create(
                    **self._base_order_kwargs(
                        recipient_phone="+48500600700",
                        recipient_consent=False,
                    )
                )

    def test_order_for_recipient_with_consent_succeeds(self):
        order = Order.objects.create(
            **self._base_order_kwargs(
                recipient_name="Anna Nowak",
                recipient_phone="+48500600700",
                recipient_consent=True,
            )
        )
        self.assertTrue(order.recipient_consent)
        self.assertEqual(order.recipient_name, "Anna Nowak")
