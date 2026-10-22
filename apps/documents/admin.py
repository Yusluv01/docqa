from django.contrib import admin
from .models import Document, Chunk

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "status", "created_at")

@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ("document", "position")