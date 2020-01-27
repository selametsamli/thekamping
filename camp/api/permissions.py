from rest_framework.permissions import BasePermission
from auths.models import UserProfile


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    message = 'You must be the owner of this object'

    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user) or request.user.is_superuser


class UserIsVerified(BasePermission):
    message = 'User is not verified'

    def has_permission(self, request, view):
        return request.user.userprofile.email_confirmed
