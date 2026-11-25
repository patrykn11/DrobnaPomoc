from django.contrib import admin

from .models import ContractorApplication, VerificationAnswer, VerificationQuestion


@admin.register(VerificationQuestion)
class VerificationQuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "is_required", "is_active", "order", "created_by")
    list_filter = ("is_required", "is_active")
    search_fields = ("text",)
    readonly_fields = ("is_active", "created_at")
    actions = ("deactivate_questions",)

    @admin.action(description="Wyłącz wybrane pytania")
    def deactivate_questions(self, request, queryset):
        queryset.filter(is_active=True).update(is_active=False)


class VerificationAnswerInline(admin.TabularInline):
    model = VerificationAnswer
    extra = 0
    readonly_fields = ("question", "question_text", "answer")
    can_delete = False


@admin.register(ContractorApplication)
class ContractorApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "contractor",
        "status",
        "submitted_at",
        "reviewed_by",
        "reviewed_at",
    )
    list_filter = ("status",)
    search_fields = ("contractor__username", "contractor__email")
    inlines = (VerificationAnswerInline,)
