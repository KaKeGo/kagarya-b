from rest_framework.permissions import BasePermission
from rest_framework import status
from rest_framework.exceptions import APIException



class NoPermission(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Dont have permission to access this view.'

class UserRolePermission(BasePermission):
    def has_permission(self, request, view):
        role_title = request.GET.get('roles', '')
        has_permission = request.user.roles.filter(title=role_title).exists()
        if not has_permission:
            raise NoPermission
        return True
