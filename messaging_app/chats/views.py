from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.db.models import Q
from rest_framework import filters, status, viewsets
from rest_framework.response import Response


class MessageViewSet(viewsets.ViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ["subject", "message_body"]

    def list(self, request, conversation_id=None):
        if conversation_id:
            queryset = Message.objects.filter(
                conversation__conversation_id=conversation_id)
        else:
            queryset = Message.objects.all()

        search_query = request.query_params.get("search", None)

        if search_query:
            queryset = queryset.filter(
                Q(subject__icontains=search_query)
                | Q(message_body__icontains=search_query))

        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"message": "Conversation not found."},
                            status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(conversation=conversation)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ConversationViewSet(viewsets.ViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__first_name", "participants__last_name"]

    def list(self, request):
        queryset = Conversation.objects.all()
        search_query = request.query_params.get("search", None)

        if search_query:
            queryset = queryset.filter(
                Q(participants__first_name__icontains=search_query)
                | Q(participants__last_name__icontains=search_query))

        serializer = ConversationSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request):
        serializer = ConversationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
