import uuid
from django.db import models
from django.conf import settings
from apps.documents.models import Document

class Conversation(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document   = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="conversations")
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title      = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Conversation {self.id}"

class Message(models.Model):
    class Role(models.TextChoices):
        USER      = "user",      "User"
        ASSISTANT = "assistant", "Assistant"

    conversation  = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    role          = models.CharField(max_length=20, choices=Role.choices)
    content       = models.TextField()
    cited_chunks  = models.JSONField(default=list, blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]