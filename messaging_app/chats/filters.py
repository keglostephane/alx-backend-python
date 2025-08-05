from django_filters import rest_framework as filters
from .models import Conversation, Message


class ConversationFilter(filters.FilterSet):
    participant = filters.CharFilter(field_name="participants__email")

    class Meta:
        model = Conversation
        fields = ["participant"]


class MessageFilter(filters.FilterSet):
    recipient = filters.CharFilter(field_name="recipient")
    conversation = filters.UUIDFilter(field_name="conversation")
    subject = filters.CharFilter(field_name="message_subject")
    message = filters.CharFilter(field_name="message_body")
    message_start_date = filters.IsoDateTimeFilter(field_name="sent_at",
                                                   lookup_expr="gte",
                                                   label="Message start-date")
    message_end_date = filters.IsoDateTimeFilter(field_name="sent_at",
                                                 lookup_expr="lte",
                                                 label="Message end-date")

    class Meta:
        model = Message
        fields = [
            "recipient", "conversation", "subject", "message",
            "message_start_date", "message_end_date"
        ]
