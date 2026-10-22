def chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits text into chunks of roughly `chunk_size` words.
    Overlap ensures we don't lose context at the boundaries.
    """
    if not text:
        return []

    # Split the text into a list of individual words
    words = text.split(" ")
    chunks = []
    
    # Start at the beginning
    start = 0
    
    while start < len(words):
        # Figure out where this chunk should end
        end = start + chunk_size
        
        # Grab the words for this chunk
        chunk_words = words[start:end]
        
        # Join them back into a string
        chunk_string = " ".join(chunk_words)
        chunks.append(chunk_string)
        
        # Move the start pointer forward by (chunk_size - overlap)
        # If we didn't subtract overlap, sentences would get cut in half at the edges
        start += (chunk_size - overlap)
        
    return chunks