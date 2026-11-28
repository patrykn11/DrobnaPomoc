from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.test import TestCase

from orders.models import Order, ServiceCategory

from .models import Offer

User = get_user_model()


class OfferModelTest(TestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(
            username="klient_offer",
            email="klient_offer@example.com",
            password="password123",
            first_name="Jan",
            last_name="Kowalski",
        )
        self.contractor_1 = User.objects.create_user(
            username="wykonawca1",
            email="wykonawca1@example.com",
            password="password123",
            first_name="Adam",
            last_name="Nowak",
        )
        self.contractor_2 = User.objects.create_user(
            username="wykonawca2",
            email="wykonawca2@example.com",
            password="password123",
            first_name="Piotr",
            last_name="Zieliński",
        )
        self.category = ServiceCategory.objects.get(name="Hydraulika")
        self.order = Order.objects.create(
            created_by=self.client_user,
            category=self.category,
            description="Naprawa uszczelki",
            requested_date=date(2026, 12, 5),
            street="Puławska",
            building_number="15",
            postal_code="02-515",
            city="Warszawa",
        )
        self.other_order = Order.objects.create(
            created_by=self.client_user,
            category=self.category,
            description="Wymiana baterii",
            requested_date=date(2026, 12, 6),
            street="Puławska",
            building_number="16",
            postal_code="02-515",
            city="Warszawa",
        )

    def test_price_zero_raises_error(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Offer.objects.create(
                    order=self.order,
                    contractor=self.contractor_1,
                    price=Decimal("0.00"),
                    proposed_date=date(2026, 12, 5),
                )

    def test_negative_price_raises_error(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Offer.objects.create(
                    order=self.order,
                    contractor=self.contractor_1,
                    price=Decimal("-50.00"),
                    proposed_date=date(2026, 12, 5),
                )

    def test_only_one_accepted_offer_per_order(self):
        Offer.objects.create(
            order=self.order,
            contractor=self.contractor_1,
            price=Decimal("150.00"),
            proposed_date=date(2026, 12, 5),
            status=Offer.Status.ACCEPTED,
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Offer.objects.create(
                    order=self.order,
                    contractor=self.contractor_2,
                    price=Decimal("140.00"),
                    proposed_date=date(2026, 12, 5),
                    status=Offer.Status.ACCEPTED,
                )

        # Zaakceptowana oferta dla innego zlecenia jest dozwolona
        other_offer = Offer.objects.create(
            order=self.other_order,
            contractor=self.contractor_2,
            price=Decimal("180.00"),
            proposed_date=date(2026, 12, 6),
            status=Offer.Status.ACCEPTED,
        )
        self.assertEqual(other_offer.status, Offer.Status.ACCEPTED)

    def test_one_active_offer_per_contractor_and_withdrawn_allows_new(self):
        first_offer = Offer.objects.create(
            order=self.order,
            contractor=self.contractor_1,
            price=Decimal("150.00"),
            proposed_date=date(2026, 12, 5),
            status=Offer.Status.SUBMITTED,
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Offer.objects.create(
                    order=self.order,
                    contractor=self.contractor_1,
                    price=Decimal("130.00"),
                    proposed_date=date(2026, 12, 5),
                    status=Offer.Status.SUBMITTED,
                )

        # Wycofanie pozwala złożyć nową ofertę na to samo zlecenie
        first_offer.status = Offer.Status.WITHDRAWN
        first_offer.save(update_fields=["status"])

        new_offer = Offer.objects.create(
            order=self.order,
            contractor=self.contractor_1,
            price=Decimal("130.00"),
            proposed_date=date(2026, 12, 5),
            status=Offer.Status.SUBMITTED,
        )
        self.assertEqual(new_offer.status, Offer.Status.SUBMITTED)

    def test_deleting_order_with_offer_is_protected(self):
        Offer.objects.create(
            order=self.order,
            contractor=self.contractor_1,
            price=Decimal("150.00"),
            proposed_date=date(2026, 12, 5),
        )
        with self.assertRaises(ProtectedError):
            self.order.delete()
