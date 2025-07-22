import uuid
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        GUEST = "guest", "Guest"
        HOST = "host", "Host"
        ADMIN = "admin", "Admin"

    user_id = models.UUIDField(primary_key=True,
                               default=uuid.uuid4,
                               editable=False)
    first_name = models.CharField("First Name", max_length=150)
    last_name = models.CharField("Last Name", max_length=150)
    email = models.EmailField("Email", unique=True)
    phone_number = models.CharField(
        "Phone",
        max_length=15,
        blank=True,
        validator=RegexValidator(
            regex=r"^\+(?:[0-9]){6,14}[0-9]$",
            message="phone number must start with '+' and contains no spaces. \
            up to 15 digits allowed."))
    role = models.CharField(max_length=5,
                            choices=Role.choices,
                            default=Role.GUEST)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        indexes = [models.Index(fields=["email"], name="email_idx")]


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True,
                                  default=uuid.uuid4,
                                  editable=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="sent_messages")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name="received_messages")
    message_body = models.TextField("message")
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.get_full_name()} at \
        {datetime.isoformat(self.sent_at)}"

    def clean(self):
        if self.sender == self.recipient:
            raise ValidationError("Sender must be different from Recipient")


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True,
                                       default=uuid.uuid4,
                                       editable=False)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          through="ConversationParticipant",
                                          related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        users = [
            f"{user.get_full_name()}" for user in self.participants.all()[:2]
        ]
        return f"Conversation: {users}"

    def clean(self):
        if self.participants.count() != 2:
            raise ValidationError(
                "Conversation must have exactly 2 participants.")


class ConversationParticipant(models.Model):
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    class Meta:
        unique_together = ["conversation_id", "user_id"]
