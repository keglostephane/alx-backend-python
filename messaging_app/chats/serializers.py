from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.Serializer):

    user_id = serializers.UUIDField(read_only=True)
    first_name = serializers.CharField("First Name", max_length=150)
    last_name = serializers.CharField("Last Name", max_length=150)
    email = serializers.EmailField()
    full_name = serializers.SerializerMethodField(get_full_name(self, obj))
    password_hash = serializers.CharField("Password",
                                          max_length=255,
                                          write_only=True)
    phone_number = serializers.CharField("Phone",
                                         max_length=20,
                                         allow_blank=True)
    role = serializers.ChoiceField(choices=User.Role.choices,
                                   default=User.Role.GUEST)
    created_at = serializers.DateTimeField(read_only=True)

    def get_full_name(self, obj):
        return f"{obj.}"

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name",
                                                 instance.first_name)
        instance.last_name = validated_data.get("last_name",
                                                instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.phone_number = validated_data.get("phone_number",
                                                   instance.phone_number)
        instance.role = validated_data.get("role", instance.role)
        instance.save()
        return instance


class MessageSerializer(serializers.Serializer):
    message_id = serializers.UUIDField(read_only=True)
    sender_id = UserSerializer(read_only=True)
    message_body = serializers.CharField()
    sent_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Message.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.message_body = validated_data.get("message_body",
                                                   instance.message_body)
        instance.save()
        return instance


class ConversationSerializer(serializers.Serializer):
    conversation_id = serializers.UUIDField(read_only=True)
    participants_id = UserSerializer(many=True, read_only=True)

    def create(self, validated_data):
        return Conversation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass
