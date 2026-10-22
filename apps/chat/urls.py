from django.urls import path
from . import views

urlpatterns = [
    path("<uuid:document_id>/", views.chat_with_document, name="chat_with_document"),
]