import os
import fitz  # PyMuPDF for PDF parsing
import docx  # python-docx for DOCX parsing
from judini import CodeGPTPlus
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API credentials
CODEGPT_API_KEY = os.getenv("CODEGPT_API_KEY")
ORG_ID = os.getenv("ORG_ID")

# Ensure API credentials are set
if not CODEGPT_API_KEY or not ORG_ID:
    raise ValueError("API Key and Organization ID must be set in environment variables.")

# Initialize CodeGPTPlus agent
codegpt = CodeGPTPlus(api_key=CODEGPT_API_KEY, org_id=ORG_ID)

# Set default LLM model
DEFAULT_MODEL = "llama-3.3-70b-versatile"

# File path (directly specified)
FILE_PATH = "Backend API Development & Integration for Flutter Web App & Wordpress website.docx"

# Agent ID
AGENT_ID = "6936c7cd-5518-4a56-a414-7f0a03789b66"

def read_docx(file_path):
    """Extract text from a DOCX file."""
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def read_pdf(file_path):
    """Extract text from a PDF file."""
    doc = fitz.open(file_path)
    text = "\n".join([page.get_text() for page in doc])
    return text

def read_file(file_path):
    """Read content from DOCX or PDF file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == ".docx":
        return read_docx(file_path)
    elif file_ext == ".pdf":
        return read_pdf(file_path)
    else:
        raise ValueError("Unsupported file format. Only DOCX and PDF are allowed.")

def generate_prompt(file_content, user_query):
    """Generate a structured prompt based on the document content and user query."""
    return f"""
    You are an AI coding assistant. A user has uploaded a document containing details about Backend API Development & Integration.

    Document Content:
    ```\n{file_content}\n```

    User Query: {user_query}

    Your Task:
    - Answer the user's query based on the document.
    - If the query requests code, generate clean, efficient Python code.
    - Ensure responses are relevant and correctly structured.
    """

def chat_with_agent(agent_id, messages, model, stream=False):
    """Send a request to the CodeGPTPlus agent and print the response."""
    print(f"\n🔍 Using Model: {model}\n")

    if stream:
        print("Streaming response:\n")
        for chunk in codegpt.chat_completion(agent_id=agent_id, messages=messages, stream=True):
            print(chunk, end="", flush=True)
    else:
        chat = codegpt.chat_completion(agent_id=agent_id, messages=messages)
        print("\nResponse:\n", chat)

if __name__ == "__main__":
    try:
        document_content = read_file(FILE_PATH)
    except Exception as e:
        print(f"Error processing file: {e}")
        exit()

    while True:
        user_query = input("\nEnter your query about the document (or type 'exit' to quit): ").strip()
        if user_query.lower() == "exit":
            print("Exiting...")
            break

        prompt = generate_prompt(document_content, user_query)
        messages = [{"role": "user", "content": prompt}]

        use_stream = input("\nEnable streaming? (y/n): ").lower().strip() == "y"

        chat_with_agent(agent_id=AGENT_ID, messages=messages, model=DEFAULT_MODEL, stream=use_stream)
