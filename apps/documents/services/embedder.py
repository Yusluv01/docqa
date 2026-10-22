import chromadb
from chromadb.utils import embedding_functions
from django.conf import settings

# We use a free, local model to turn text into numbers (vectors).
# This downloads a small model the first time it runs.
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def get_chroma_client():
    # This creates a folder called 'chroma_data' in your project root to save the vectors
    return chromadb.PersistentClient(path=str(settings.BASE_DIR / "chroma_data"))

def add_chunks_to_vector_db(chunks, document_id):
    """
    Takes a list of Chunk objects and stores their text + ID in the vector database.
    """
    client = get_chroma_client()
    
    # Create or get a collection (like a table in a normal database)
    collection = client.get_or_create_collection(
        name="documents", 
        embedding_function=embedding_func
    )
    
    # Prepare the data for Chroma
    ids = [str(chunk.id) for chunk in chunks]
    texts = [chunk.text for chunk in chunks]
    metadatas = [{"document_id": str(document_id)} for chunk in chunks]
    
    # Add to the database (Chroma automatically embeds the text for us!)
    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas
    )
    print(f"Added {len(chunks)} chunks to ChromaDB.")

def search_chunks(query_text, document_id, n_results=3):
    """
    Takes a user's question and finds the most relevant chunks for that document.
    """
    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name="documents", 
        embedding_function=embedding_func
    )
    
    # Search ChromaDB, filtering by the specific document_id
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where={"document_id": str(document_id)} # Only search this document!
    )
    
    # results['documents'][0] contains the actual text strings
    # results['ids'][0] contains the chunk IDs
    return results['documents'][0], results['ids'][0]