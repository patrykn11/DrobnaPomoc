from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ContractorProfile, Role
from .permissions import IsClient


class AccountsApiTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = get_user_model().objects.create_user(
            username="jan",
            email="jan@example.com",
            password="haslo123",
            first_name="Jan",
            last_name="Kowalski",
        )

    def test_register(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "anna",
                "email": "anna@example.com",
                "first_name": "Anna",
                "last_name": "Nowak",
                "phone_number": "+48123456789",
                "password": "haslo123",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)
        self.assertEqual(response.data["phone_number"], "+48123456789")

    def test_register_rejects_weak_password(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "anna",
                "email": "anna@example.com",
                "first_name": "Anna",
                "last_name": "Nowak",
                "password": "123",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_rejects_duplicate_email(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "anna",
                "email": self.user.email,
                "first_name": "Anna",
                "last_name": "Nowak",
                "password": "haslo123",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_login_returns_tokens(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "jan",
                "password": "haslo123",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_rejects_wrong_password(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "jan",
                "password": "wrong-password",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_logout_blacklists_refresh_token(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.force_authenticate(user=self.user)

        response = self.client.post(reverse("logout"), {"refresh": str(refresh)})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(
            BlacklistedToken.objects.filter(token__jti=refresh["jti"]).exists()
        )

    def test_me_returns_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("me"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "jan")
        self.assertEqual(response.data["roles"], [Role.Code.CLIENT])
        self.assertFalse(response.data["is_consultant"])
        self.assertFalse(response.data["is_contractor"])

    def test_new_user_receives_client_role(self):
        request = type("Request", (), {"user": self.user})()

        self.assertTrue(IsClient().has_permission(request, None))

    def test_user_can_have_multiple_roles(self):
        contractor_role, _ = Role.objects.get_or_create(code=Role.Code.CONTRACTOR)
        self.user.roles.add(contractor_role)

        self.assertTrue(self.user.has_role(Role.Code.CLIENT))
        self.assertTrue(self.user.has_role(Role.Code.CONTRACTOR))

    def test_contractor_profile_stores_service_area(self):
        profile = ContractorProfile.objects.create(
            user=self.user,
            city="Warszawa",
            service_radius_km=30,
        )

        self.assertEqual(profile.city, "Warszawa")
        self.assertEqual(profile.service_radius_km, 30)

    def test_change_password_rejects_same_password(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("change-password"),
            {
                "old_password": "haslo123",
                "new_password": "haslo123",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
