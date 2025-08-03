from django.db.models import Q
from rest_framework import permissions

from .models import Conversation, Message


class IsSenderOrRecipient(permissions.BasePermission):
    """Checks if user can access messages.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and Message.objects.filter(
            Q(sender__email__exact=request.user.email)
            | Q(recipient__email__exact=request.user.email)).exists()


class IsParticipantOfConversation(permissions.BasePermission):
    """Check if user is part of the conversation.
    """

    def has_permission(self, request, view):
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            conversation_id = view.kwargs.get("conversation_pk")
            return request.user.is_authenticated and Conversation.objects.filter(
                conversation_id=conversation_id,
                participants__email__exact=request.user.email)
        return request.user.is_authenticated
