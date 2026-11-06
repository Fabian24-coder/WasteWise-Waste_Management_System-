from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    role = None

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == self.role)


class IsRequestor(RolePermission):
    role = "requestor"


class IsResident(IsRequestor):
    pass


class IsCollector(RolePermission):
    role = "collector"


class IsAdminRole(RolePermission):
    role = "admin"

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.role == self.role or request.user.is_superuser)
        )