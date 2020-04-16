"""Define permissions to apply to views."""

from rest_framework import permissions


class IsAdminWriteOnly(permissions.BasePermission):
    """Define permission to allow write access to admin olnly."""

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        """Implement logic to check if request should be permitted."""
        if request.method not in permissions.SAFE_METHODS:
            if request.user.is_staff:
                return True
            else:
                return False
        else:
            return True


class AllowAuthenicUserPatch(permissions.BasePermission):
    """Let object owner be able to update flight passengers."""

    def has_permission(self, request, view):
        """Implement logic to check if request should be permitted."""
        if request.method not in permissions.SAFE_METHODS:
            if not request.user.is_staff and request.method == "PATCH":
                return True
            else:
                return False
        else:
            return True
