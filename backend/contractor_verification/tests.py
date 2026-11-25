from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

from .models import ContractorApplication, VerificationAnswer, VerificationQuestion
from .permissions import IsApprovedContractor


class ContractorVerificationApiTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.consultant = user_model.objects.create_user(
            username="consultant",
            email="consultant@example.com",
            password="haslo123",
            role=User.Role.CONSULTANT,
        )
        self.contractor = user_model.objects.create_user(
            username="contractor",
            email="contractor@example.com",
            password="haslo123",
            role=User.Role.CONTRACTOR,
        )
        self.question = VerificationQuestion.objects.create(
            text="Jakie masz doświadczenie?", created_by=self.consultant
        )

    def test_consultant_cannot_create_question(self):
        self.client.force_authenticate(user=self.consultant)

        response = self.client.post(
            reverse("verification-questions"),
            {"text": "Czy posiadasz uprawnienia?", "is_required": True, "order": 2},
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_contractor_cannot_create_question(self):
        self.client.force_authenticate(user=self.contractor)

        response = self.client.post(
            reverse("verification-questions"), {"text": "Niedozwolone pytanie"}
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_inactive_question_is_not_returned(self):
        self.question.is_active = False
        self.question.save(update_fields=["is_active"])
        self.client.force_authenticate(user=self.contractor)

        response = self.client.get(reverse("verification-questions"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_contractor_can_submit_answers(self):
        self.client.force_authenticate(user=self.contractor)

        response = self.client.post(
            reverse("my-applications"),
            {
                "answers": [
                    {
                        "question": self.question.pk,
                        "answer": "Mam pięć lat doświadczenia.",
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        application = ContractorApplication.objects.get(contractor=self.contractor)
        answer = VerificationAnswer.objects.get(application=application)
        self.assertEqual(answer.question_text, self.question.text)
        self.assertEqual(application.status, ContractorApplication.Status.PENDING)

    def test_all_required_questions_must_be_answered(self):
        self.client.force_authenticate(user=self.contractor)

        response = self.client.post(
            reverse("my-applications"), {"answers": []}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_consultant_can_approve_application(self):
        application = ContractorApplication.objects.create(contractor=self.contractor)
        self.client.force_authenticate(user=self.consultant)

        response = self.client.patch(
            reverse("review-application", args=[application.pk]),
            {"status": "approved", "review_note": "Weryfikacja poprawna."},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        application.refresh_from_db()
        self.assertEqual(application.status, ContractorApplication.Status.APPROVED)
        self.assertEqual(application.reviewed_by, self.consultant)
        self.assertIsNotNone(application.reviewed_at)

    def test_contractor_cannot_review_application(self):
        application = ContractorApplication.objects.create(contractor=self.contractor)
        self.client.force_authenticate(user=self.contractor)

        response = self.client.patch(
            reverse("review-application", args=[application.pk]), {"status": "approved"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_consultant_sees_newest_applications_first(self):
        older_application = ContractorApplication.objects.create(
            contractor=self.contractor, status=ContractorApplication.Status.REJECTED
        )
        newer_application = ContractorApplication.objects.create(
            contractor=self.contractor
        )
        self.client.force_authenticate(user=self.consultant)

        response = self.client.get(reverse("verification-applications"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = [application["id"] for application in response.data["results"]]
        self.assertEqual(returned_ids[:2], [newer_application.id, older_application.id])

    def test_consultant_applications_are_paginated(self):
        ContractorApplication.objects.bulk_create(
            [
                ContractorApplication(
                    contractor=self.contractor,
                    status=ContractorApplication.Status.REJECTED,
                )
                for _ in range(21)
            ]
        )
        self.client.force_authenticate(user=self.consultant)

        response = self.client.get(reverse("verification-applications"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 21)
        self.assertEqual(len(response.data["results"]), 20)
        self.assertIsNotNone(response.data["next"])

    def test_application_cannot_be_reviewed_twice(self):
        application = ContractorApplication.objects.create(contractor=self.contractor)
        self.client.force_authenticate(user=self.consultant)
        review_url = reverse("review-application", args=[application.pk])

        first_response = self.client.patch(review_url, {"status": "approved"})
        second_response = self.client.patch(review_url, {"status": "rejected"})

        self.assertEqual(first_response.status_code, status.HTTP_200_OK)
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_approved_application_grants_contractor_permission(self):
        application = ContractorApplication.objects.create(
            contractor=self.contractor, status=ContractorApplication.Status.APPROVED
        )
        request = type("Request", (), {"user": self.contractor})()

        self.assertTrue(IsApprovedContractor().has_permission(request, None))

        application.status = ContractorApplication.Status.REJECTED
        application.save(update_fields=["status"])
        self.assertFalse(IsApprovedContractor().has_permission(request, None))
