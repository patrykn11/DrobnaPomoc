from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from .models import ContractorApplication, VerificationAnswer, VerificationQuestion


class VerificationQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationQuestion
        fields = [
            "id",
            "text",
            "is_required",
            "is_active",
            "order",
            "created_at"
        ]
        read_only_fields = ["id", "is_active", "created_at"]


class AnswerInputSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=VerificationQuestion.objects.filter(is_active=True)
    )
    answer = serializers.CharField(allow_blank=False, trim_whitespace=True)


class VerificationAnswerSerializer(serializers.ModelSerializer):
    question = serializers.IntegerField(source="question_id", read_only=True)

    class Meta:
        model = VerificationAnswer
        fields = ["id", "question", "question_text", "answer"]
        read_only_fields = fields


class ContractorApplicationSerializer(serializers.ModelSerializer):
    contractor_name = serializers.CharField(
        source="contractor.get_full_name",
        read_only=True
    )
    contractor_email = serializers.EmailField(
        source="contractor.email",
        read_only=True
    )
    answers = VerificationAnswerSerializer(many=True, read_only=True)
    reviewed_by = serializers.CharField(
        source="reviewed_by.get_full_name",
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = ContractorApplication
        fields = [
            "id",
            "contractor",
            "contractor_name",
            "contractor_email",
            "status",
            "answers",
            "reviewed_by",
            "review_note",
            "submitted_at",
            "reviewed_at"
        ]
        read_only_fields = fields


class SubmitApplicationSerializer(serializers.Serializer):
    answers = AnswerInputSerializer(many=True)

    def validate_answers(self, answers):
        question_ids = [answer["question"].pk for answer in answers]
        if len(question_ids) != len(set(question_ids)):
            raise serializers.ValidationError(
                "Na każde pytanie można odpowiedzieć tylko raz."
            )

        required_ids = set(
            VerificationQuestion.objects.filter(
                is_active=True,
                is_required=True
            ).values_list("id", flat=True)
        )
        if not VerificationQuestion.objects.filter(is_active=True).exists():
            raise serializers.ValidationError("Brak aktywnych pytań w formularzu.")
        missing_ids = required_ids - set(question_ids)
        if missing_ids:
            raise serializers.ValidationError(
                "Odpowiedz na wszystkie wymagane pytania."
            )
        return answers

    def validate(self, attrs):
        contractor = self.context["request"].user
        applications = ContractorApplication.objects.filter(contractor=contractor)
        if applications.filter(status=ContractorApplication.Status.APPROVED).exists():
            raise serializers.ValidationError(
                "Twój profil wykonawcy został już zaakceptowany."
            )
        if applications.filter(status=ContractorApplication.Status.PENDING).exists():
            raise serializers.ValidationError(
                "Masz już zgłoszenie oczekujące na weryfikację."
            )
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        contractor = self.context["request"].user
        application = ContractorApplication.objects.create(contractor=contractor)
        VerificationAnswer.objects.bulk_create(
            [
                VerificationAnswer(
                    application=application,
                    question=item["question"],
                    question_text=item["question"].text,
                    answer=item["answer"]
                )
                for item in validated_data["answers"]
            ]
        )
        return application


class ReviewApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractorApplication
        fields = ["status", "review_note"]

    def validate_status(self, value):
        if value not in {
            ContractorApplication.Status.APPROVED,
            ContractorApplication.Status.REJECTED
        }:
            raise serializers.ValidationError("Wybierz decyzję approved albo rejected.")
        return value

    def validate(self, attrs):
        if self.instance.status != ContractorApplication.Status.PENDING:
            raise serializers.ValidationError("To zgłoszenie zostało już rozpatrzone.")
        return attrs

    def update(self, instance, validated_data):
        instance.status = validated_data["status"]
        instance.review_note = validated_data.get("review_note", "")
        instance.reviewed_by = self.context["request"].user
        instance.reviewed_at = timezone.now()
        instance.save(
            update_fields=[
                "status",
                "review_note",
                "reviewed_by",
                "reviewed_at"
            ]
        )
        return instance
