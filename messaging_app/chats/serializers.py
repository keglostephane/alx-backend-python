from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = [
            "user_id", "first_name", "last_name", "email", "password_hash",
            "phone_number", "role", "created_at"
        ]
        read_only_fields = ["user_id", "created_at"]
        extra_kwargs = {"password_hash": {"write_only: True"}}

        def create(self, validated_data):
            user = User(**validated_data)
            user.set_password(validated_data["password_hash"])
            user.save()
            return user


class MessageSerializer(serializers.Serializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["message_id", "sender_id", "message_body", "sent_at"]
        read_only_fields = ["sender_id", "message_id", "sent_at"]


class ConversationSerializer(serializers.Serializer):
    participants = UserSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ["conversation_id"]
        read_only_fields = ["conversation_id"]
