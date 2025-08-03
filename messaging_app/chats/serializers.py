from rest_framework import serializers

from .models import Conversation, Message, User


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

    def validate_sender(self, sender):
        conversation = self.initial_data.get("conversation")

        if conversation:
            conversation = Conversation.objects.get(pk=conversation)
            if not conversation.participants.filter(
                    user_id=sender.user_id).exists():
                raise serializers.ValidationError(
                    "Sender must be part of the conversation.")
        return sender

    def validate_recipient(self, recipient):
        conversation = self.initial_data.get("conversation")

        if conversation:
            conversation = Conversation.objects.get(pk=conversation)
            if not conversation.participants.filter(
                    user_id=recipient.user_id).exists():
                raise serializers.ValidationError(
                    "Recipient must be part of the conversation.")
        return recipient

    def validate(self, attrs):
        if attrs["sender"] == attrs["recipient"]:
            raise serializers.ValidationError(
                "Sender must be different from Recipient.")
        return attrs

    def create(self, validated_data):
        return Message.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.sender = validated_data.get("sender", instance.sender)
        instance.recipient = validated_data.get("recipient",
                                                instance.recipient)
        instance.conversation = validated_data.get("conversation",
                                                   instance.conversation)
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

    class Meta:
        model = Conversation
        fields = ["conversation_id", "created_at", "participants"]
        read_only_fields = ["conversation_id", "created_at"]
