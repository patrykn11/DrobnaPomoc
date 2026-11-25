from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers as verification_serializers
from .models import ContractorApplication, VerificationQuestion
from .pagination import ApplicationPagination
from .permissions import IsConsultant, IsContractor


class QuestionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = VerificationQuestion.objects.filter(is_active=True)
        serializer = verification_serializers.VerificationQuestionSerializer(
            questions, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyApplicationsView(APIView):
    permission_classes = [IsAuthenticated, IsContractor]

    def get(self, request):
        applications = (
            ContractorApplication.objects.filter(contractor=request.user)
            .select_related("contractor", "reviewed_by")
            .prefetch_related("answers")
        )
        paginator = ApplicationPagination()
        page = paginator.paginate_queryset(applications, request, view=self)
        serializer = verification_serializers.ContractorApplicationSerializer(
            page, many=True
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = verification_serializers.SubmitApplicationSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        try:
            application = serializer.save()
        except IntegrityError:
            return Response(
                {"detail": "Masz już zgłoszenie oczekujące na weryfikację."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        output = verification_serializers.ContractorApplicationSerializer(application)
        return Response(output.data, status=status.HTTP_201_CREATED)


class ConsultantApplicationsView(APIView):
    permission_classes = [IsAuthenticated, IsConsultant]

    def get(self, request):
        applications = (
            ContractorApplication.objects.select_related("contractor", "reviewed_by")
            .prefetch_related("answers")
            .order_by("-submitted_at", "-id")
        )

        requested_status = request.query_params.get("status")
        if requested_status:
            valid_statuses = ContractorApplication.Status.values
            if requested_status not in valid_statuses:
                return Response(
                    {"status": "Nieprawidłowy status zgłoszenia."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            applications = applications.filter(status=requested_status)

        paginator = ApplicationPagination()
        page = paginator.paginate_queryset(applications, request, view=self)
        serializer = verification_serializers.ContractorApplicationSerializer(
            page, many=True
        )
        return paginator.get_paginated_response(serializer.data)


class ReviewApplicationView(APIView):
    permission_classes = [IsAuthenticated, IsConsultant]

    @transaction.atomic
    def patch(self, request, pk):
        application = get_object_or_404(
            ContractorApplication.objects.select_for_update(), pk=pk
        )
        serializer = verification_serializers.ReviewApplicationSerializer(
            application, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            verification_serializers.ContractorApplicationSerializer(application).data,
            status=status.HTTP_200_OK,
        )
