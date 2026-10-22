from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Document
from .forms import DocumentForm
from .services.ingest import process_document 

@login_required
def upload_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.owner = request.user
            doc.save()
            
            # Trigger the AI pipeline!
            process_document(doc.id) 
            
            return redirect("document_list")
    else:
        form = DocumentForm()
    
    return render(request, "documents/upload.html", {"form": form})

@login_required
def document_list(request):
    documents = Document.objects.filter(owner=request.user).order_by("-created_at")
    return render(request, "documents/list.html", {"documents": documents})