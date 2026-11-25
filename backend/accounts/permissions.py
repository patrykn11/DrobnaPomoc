from rest_framework.permissions import BasePermission

from .models import User


class HasRole(BasePermission):
    required_role = None

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == self.required_role


class IsClient(HasRole):
    required_role = User.Role.CLIENT
    message = "Ta funkcja jest dostępna tylko dla zleceniodawców."


class IsContractor(HasRole):
    required_role = User.Role.CONTRACTOR
    message = "Ta funkcja jest dostępna tylko dla wykonawców."


class IsConsultant(HasRole):
    required_role = User.Role.CONSULTANT
    message = "Ta funkcja jest dostępna tylko dla konsultantów."
