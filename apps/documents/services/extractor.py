from pypdf import PdfReader

def extract_text_from_pdf(file_path_or_stream):
    """
    Takes a file path or a Django uploaded file stream,
    reads the PDF, and returns all the text as a single string.
    """
    try:
        reader = PdfReader(file_path_or_stream)
        text = ""
        
        # Go through every page and add it to our text block
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                
        return text.strip()
        
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None