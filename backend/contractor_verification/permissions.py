from accounts.permissions import IsConsultant, IsContractor

from .models import ContractorApplication


class IsApprovedContractor(IsContractor):
    message = "Profil wykonawcy nie został zaakceptowany."

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return ContractorApplication.objects.filter(
            contractor=request.user, status=ContractorApplication.Status.APPROVED
        ).exists()


__all__ = ["IsApprovedContractor", "IsConsultant", "IsContractor"]
