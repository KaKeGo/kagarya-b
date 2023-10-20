from rest_framework.permissions import BasePermission
from rest_framework import status
from rest_framework.exceptions import APIException



class NoPermission(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Dont have permission to access this view.'

class UserRolePermissionFactory:
    def __init__(self, roles):
        self.roles = roles

    def __call__(self):
        roles = self.roles
        class UserRolePermission(BasePermission):
            def has_permission(self, request, view):
                if request.user.is_anonymous:
                    raise NoPermission
                has_permission = any(request.user.roles.filter(title=role).exists() for role in roles)
                if not has_permission:
                    raise NoPermission
                return True
        return UserRolePermission
