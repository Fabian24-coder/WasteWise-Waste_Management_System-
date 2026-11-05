from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    role = None

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == self.role)


class IsResident(RolePermission):
    role = "resident"


class IsCollector(RolePermission):
    role = "collector"


class IsAdminRole(RolePermission):
    role = "admin"