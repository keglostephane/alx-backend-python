import uuid
from datetime import datetime

from django.contrib.auth.models import AbstractUser
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
    phone_number = models.CharField("Phone", max_length=20, blank=True)
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
    sender_id = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name="messages")
    message_body = models.TextField("message")
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender_id.get_full_name()} at \
        {datetime.isoformat(self.sent_at)}"


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True,
                                       default=uuid.uuid4,
                                       editable=False)
    participants_id = models.ManyToManyField(User,
                                             related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.conversation_id}"
