from rest_framework import permissions
from rest_framework.views import APIView

from accounts.constants import UserType
from common.exceptions import BadRequest, UnauthorizedAccess
from common.functions import decode
from accounts.models import AccessToken, User


class IsAuthenticated(permissions.BasePermission):
    """
    Check if the user is authenticated.
    """

    def has_permission(self, request, view):
        """Function to check token."""
        key = request.META.get('HTTP_BEARER')
        user_id = decode(request.META.get('HTTP_USER_ID'))
        if not key:
            raise BadRequest(
                'Can not find Bearer token in the request header.')
        if not user_id:
            raise BadRequest('Can not find User-Id in the request header.')
        try:
            user = AccessToken.objects.get(key=key, user__id=user_id).user
        except:
            raise UnauthorizedAccess(
                'Invalid Bearer token or User-Id, please re-login.')
        request.user = user
        view.kwargs['user'] = user
        return True


class IsAdmin(permissions.BasePermission):
    """
    Check if the user is authenticated.
    """

    def has_permission(self, request, view):
        if view.kwargs['user'].type == UserType.ADMIN:
            return True
        raise BadRequest("No permission")


class IsShop(permissions.BasePermission):
    """
    Check if the user is authenticated.
    """

    def has_permission(self, request, view):
        if view.kwargs['user'].type == UserType.SHOP:
            return True
        raise BadRequest("No permission")


class IsCard(permissions.BasePermission):
    """
    Check if the user is authenticated.
    """

    def has_permission(self, request, view):
        if view.kwargs['user'].type == UserType.CARD:
            view.kwargs['card'] = view.kwargs['user'].card
            return True
        raise BadRequest("No permission")


class MultiPermissionView(APIView):
    """
    Permissions can be defined using permissions attribute with a dictionary
    with the type of request as key and permission as value
    """
    permissions = {}

    def get_permissions(self):
        try:
            self.permission_classes = self.permissions[self.request.method]
        except KeyError:
            raise BadRequest("Method not allowed")
        return super(MultiPermissionView, self).get_permissions()
