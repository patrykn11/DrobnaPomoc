from django.conf import settings
from django.db import models
from django.db.models import Q


class VerificationQuestion(models.Model):
    text = models.CharField(max_length=500)
    is_required = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_verification_questions",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text


class ContractorApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Oczekuje na weryfikację"
        APPROVED = "approved", "Zaakceptowane"
        REJECTED = "rejected", "Odrzucone"

    contractor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contractor_applications",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_contractor_applications",
    )
    review_note = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-submitted_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["contractor"],
                condition=Q(status="pending"),
                name="one_pending_application_per_contractor",
            )
        ]

    def __str__(self):
        return f"Zgłoszenie {self.contractor} ({self.get_status_display()})"


class VerificationAnswer(models.Model):
    application = models.ForeignKey(
        ContractorApplication, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(
        VerificationQuestion, on_delete=models.PROTECT, related_name="answers"
    )
    question_text = models.CharField(max_length=500)
    answer = models.TextField()

    class Meta:
        ordering = ["question__order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["application", "question"],
                name="unique_answer_per_application_question",
            )
        ]

    def __str__(self):
        return f"Odpowiedź na: {self.question_text}"
