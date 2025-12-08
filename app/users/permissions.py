from rest_framework.permissions import BasePermission

class Is_Admin(BasePermission):
    message = "siz Admin emassiz"

    def has_permission(self, request, view):
        return request.user and request.user.is_admin