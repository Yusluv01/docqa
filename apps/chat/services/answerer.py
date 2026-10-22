import os
from groq import Groq

def generate_answer(question, context_chunks):
    """
    Takes the user's question and the retrieved text chunks, 
    and asks the Groq API to write an answer based ONLY on those chunks.
    """
    # Combine the chunks into one big context string
    context = "\n\n---\n\n".join(context_chunks)
    
    prompt = f"""
    You are a helpful assistant. Answer the user's question using ONLY the provided context.
    If the answer is not in the context, say "I don't know based on the provided document."
    
    Context:
    {context}
    
    Question: {question}
    """
    
    # Get the API key from the .env file
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY is missing from your .env file."

    try:
        client = Groq(api_key=api_key)
        
        # Call the Llama 3 model hosted on Groq (extremely fast)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
           model="openai/gpt-oss-120b",
        )
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"Error connecting to Groq: {e}"