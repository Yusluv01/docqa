import uuid
from django.db import models
from django.conf import settings

class Document(models.Model):
    class Status(models.TextChoices):
        PENDING    = "pending",    "Pending"
        PROCESSING = "processing", "Processing"
        READY      = "ready",      "Ready"
        FAILED     = "failed",     "Failed"

    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documents")
    title      = models.CharField(max_length=255)
    file       = models.FileField(upload_to="documents/%Y/%m/")
    status     = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    error      = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Chunk(models.Model):
    document   = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="chunks")
    position   = models.PositiveIntegerField()
    text       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position"]