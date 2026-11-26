from rest_framework.permissions import BasePermission

from .models import Role


class HasRole(BasePermission):
    role_code = None

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_role(self.role_code)


class IsClient(HasRole):
    message = "Ta funkcja jest dostępna tylko dla zleceniodawców."
    role_code = Role.Code.CLIENT


class IsContractor(HasRole):
    message = "Ta funkcja jest dostępna tylko dla wykonawców."
    role_code = Role.Code.CONTRACTOR


class IsConsultant(HasRole):
    message = "Ta funkcja jest dostępna tylko dla konsultantów."
    role_code = Role.Code.CONSULTANT
