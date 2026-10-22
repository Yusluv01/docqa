from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.documents.models import Document
from apps.documents.services.embedder import search_chunks
from apps.chat.services.answerer import generate_answer
from .models import Conversation, Message

@login_required
def chat_with_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, owner=request.user)
    
    # Get or create a conversation for this document
    conversation, _ = Conversation.objects.get_or_create(
        document=document, 
        user=request.user
    )
    
    if request.method == "POST":
        user_question = request.POST.get("question")
        
        if user_question:
            # 1. Save the user's message
            Message.objects.create(conversation=conversation, role="user", content=user_question)
            
            # 2. Retrieve relevant chunks
            texts, chunk_ids = search_chunks(user_question, document.id)
            
            # 3. Generate the answer
            answer = generate_answer(user_question, texts)
            
            # 4. Save the assistant's message and cite the chunks
            Message.objects.create(
                conversation=conversation, 
                role="assistant", 
                content=answer,
                cited_chunks=chunk_ids
            )
            
            return redirect("chat_with_document", document_id=document.id)

    # Fetch all messages to display them
    messages = conversation.messages.all()
    return render(request, "chat/chat.html", {
        "document": document, 
        "messages": messages
    })