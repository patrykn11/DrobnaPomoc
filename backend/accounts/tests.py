from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AccountsApiTests(APITestCase):
    def setUp(self):
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
                "password": "haslo123",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)

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

    def test_me_returns_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("me"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "jan")

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
