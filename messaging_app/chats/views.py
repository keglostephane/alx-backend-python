from django.db.models import Q
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsSenderOrRecipient, IsSender


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["message_subject", "message_body"]

    def get_queryset(self):
        queryset = super().get_queryset()
        conversation_id = self.kwargs.get("conversation_pk")
        search_query = self.request.query_params.get("search", None)

        if conversation_id:
            queryset = queryset.filter(
                conversation__conversation_id=conversation_id)

        user_email = self.request.user.email
        queryset = queryset.filter(
            Q(sender__email__iexact=user_email)
            | Q(recipient__email__iexact=user_email))

        if search_query:
            queryset = queryset.filter(
                Q(message_subject__icontains=search_query)
                | Q(message_body__icontains=search_query))

        return queryset

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            self.permission_classes = [IsSender]
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsSenderOrRecipient]
        return super().get_permissions()

    def create(self, request, **kwargs):
        try:
            conversation_id = kwargs.get("conversation_pk")
            conversation = Conversation.objects.get(
                conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"message": "Conversation not found."},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def messages_by_conversation(self, request, conversation_id=None):
        try:
            print(request.query_params)
            conversation = Conversation.objects.get(
                conversation_id=conversation_id)
            messages = Message.objects.filter(conversation=conversation)
            serializer = self.get_serializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Conversation.DoesNotExist:

            return Response({"detail": "Conversation not found."},
                            status=status.HTTP_404_NOT_FOUND)


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__first_name", "participants__last_name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user_email = self.request.user.email
        search_query = self.request.query_params.get("search", None)

        queryset = queryset.filter(participants__email=user_email)

        if search_query:
            queryset = queryset.filter(
                Q(participants__first_name__icontains=search_query)
                | Q(participants__last_name__icontains=search_query))

        return queryset

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
