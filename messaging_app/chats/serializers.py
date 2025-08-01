from .models import Conversation, Message, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number", "role"]
        read_only_fields = ["user_id", "created_at"]


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False,
                                          slug_field="email",
                                          queryset=User.objects.all())
    recipient = serializers.SlugRelatedField(many=False,
                                             slug_field="email",
                                             queryset=User.objects.all())
    conversation = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(),
        pk_field=serializers.UUIDField(format="hex"))
    message_subject = serializers.CharField(max_length=50, allow_blank=True)

    class Meta:
        model = Message
        fields = [
            "message_id", "sent_at", "message_subject", "sender", "recipient",
            "message_body", "conversation"
        ]
        read_only_fields = ["message_id", "sent_at"]

    def create(self, validated_data):
        conversation = validated_data.get("conversation")
        sender = validated_data.get("sender")
        recipient = validated_data.get("recipient")

        if not conversation.participants.filter(
                user_id=sender.user_id).exists():
            raise serializers.ValidationError(
                "Sender must be part of the conversation.")

        if not conversation.participants.filter(
                user_id=recipient.user_id).exists():
            raise serializers.ValidationError(
                "Recipient must be part of the conversation.")
        return Message.objects.create(**validated_data)

    def update(self, instance, validated_data):
        conversation = validated_data.get("conversation",
                                          instance.conversation)
        sender = validated_data.get("sender", instance.sender)
        recipient = validated_data.get("recipient", instance.recipient)

        if not conversation.participants.filter(
                user_id=sender.user_id).exists():
            raise serializers.ValidationError(
                "Sender must be part of the conversation.")

        if not conversation.participants.filter(
                user_id=recipient.user_id).exists():
            raise serializers.ValidationError(
                "Recipient must be part of the conversation.")

        instance.sender = sender
        instance.recipient = recipient
        instance.conversation = conversation
        instance.message_body = validated_data.get("message_body",
                                                   instance.message_body)
        instance.message_subject = validated_data.get("message_subject",
                                                      instance.message_subject)
        instance.save()
        return instance


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SlugRelatedField(many=True,
                                                slug_field="email",
                                                queryset=User.objects.all())
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["conversation_id", "created_at", "participants", "messages"]
        read_only_fields = ["conversation_id", "created_at"]

    def get_messages(self, obj):
        messages = obj.messages.all()
        return MessageSerializer(messages, many=True).data
