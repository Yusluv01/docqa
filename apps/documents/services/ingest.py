from apps.documents.models import Document, Chunk
from .extractor import extract_text_from_pdf
from .chunker import chunk_text
from .embedder import add_chunks_to_vector_db 

def process_document(document_id):
    """
    Takes a Document ID, extracts text from its file, 
    chunks it, saves the chunks to the database, and updates the status.
    """
    try:
        # 1. Get the document from the database
        doc = Document.objects.get(id=document_id)
        doc.status = Document.Status.PROCESSING
        doc.save()

        # 2. Extract text (we pass the Django file object directly)
        text = extract_text_from_pdf(doc.file)
        
        if not text:
            raise ValueError("Could not extract text from PDF.")

        # 3. Chunk the text
        chunks = chunk_text(text)

        # 4. Save chunks to the database
        # We use bulk_create to save all chunks in one fast database query
        chunk_objects = [
            Chunk(document=doc, position=i, text=chunk_str)
            for i, chunk_str in enumerate(chunks)
        ]
        Chunk.objects.bulk_create(chunk_objects)
     
        # 5. NEW: Add them to the Vector Database
        # bulk_create doesn't automatically return the IDs on all databases, 
        # so we fetch them back to get their database IDs.
        saved_chunks = list(Chunk.objects.filter(document=doc).order_by("position"))
        add_chunks_to_vector_db(saved_chunks, doc.id)
        

        # 6. Mark as ready!
        doc.status = Document.Status.READY
        doc.save()

        print(f"Successfully processed {doc.title} into {len(chunks)} chunks.")

    except Exception as e:
        # If anything fails, save the error to the document and mark it FAILED
        print(f"Error processing document: {e}")
        doc = Document.objects.get(id=document_id)
        doc.status = Document.Status.FAILED
        doc.error = str(e)
        doc.save()