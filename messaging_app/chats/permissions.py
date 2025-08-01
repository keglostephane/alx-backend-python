from rest_framework import permissions
from .models import Message
from django.db.models import Q


class IsSenderOrRecipient(permissions.BasePermission):
    """Checks if user can access messages.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.email:
            return Message.objects.filter(
                Q(sender__email__exact=request.user.email)
                | Q(recipient__email__exact=request.user.email)).exists()
        return False


class IsSender(permissions.BasePermission):
    """Checks if user has full control on his messages.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.email:
            return obj.sender == request.user.email
        return False
