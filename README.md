# 📚 DocQA - AI Document Chat

DocQA is a full-stack web application that lets users upload PDF documents and ask natural language questions about them. It uses **Retrieval-Augmented Generation (RAG)** to ensure the AI only answers based on the provided document, eliminating hallucinations.

## 🚀 Features
- **Document Upload:** Securely upload PDF files.
- **AI Text Extraction:** Automatically extracts and chunks text from PDFs.
- **Vector Search:** Uses ChromaDB to find the most relevant chunks based on semantic meaning.
- **Fast AI Responses:** Integrates with Groq (Llama 3) for blazing-fast, context-aware answers.
- **Source Citations:** Shows exactly which chunks the AI used to generate the answer.

## 🛠️ Tech Stack
- **Backend:** Python, Django
- **AI / LLM:** Groq API (Llama 3), SentenceTransformers
- **Vector Database:** ChromaDB
- **Frontend:** HTML/CSS, Bootstrap 5
- **Deployment:** Render

## 💻 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Yusluv01/docqa.git
   cd docqa
