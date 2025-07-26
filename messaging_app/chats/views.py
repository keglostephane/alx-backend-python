from django.db.models import Q
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["message_subject", "message_body"]

    def get_queryset(self):
        queryset = super().get_queryset()
        conversation_id = self.kwargs.get("conversation_id")
        search_query = self.request.query_params.get("search", None)

        if conversation_id:
            queryset = queryset.filter(
                conversation__conversation_id=conversation_id)

        if search_query:
            queryset = queryset.filter(
                Q(message_subject__icontains=search_query)
                | Q(message_body__icontains=search_query))

        return queryset

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


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__first_name", "participants__last_name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get("search", None)

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
