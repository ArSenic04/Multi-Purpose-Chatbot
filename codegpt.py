import os
from judini import CodeGPTPlus
from dotenv import load_dotenv

# Load environment variables from .env file (if available)
load_dotenv()

# Retrieve API credentials from environment variables
CODEGPT_API_KEY = os.getenv("CODEGPT_API_KEY")
ORG_ID = os.getenv("ORG_ID")

# Ensure API credentials are set
if not CODEGPT_API_KEY or not ORG_ID:
    raise ValueError("API Key and Organization ID must be set in environment variables.")

# Initialize CodeGPTPlus agent
codegpt = CodeGPTPlus(api_key=CODEGPT_API_KEY, org_id=ORG_ID)

# Define available LLM models
AVAILABLE_MODELS = {
    "1": "gpt-4",
    "2": "gpt-3.5-turbo",
    "3": "llama-3.3-70b-versatile",
}

def choose_model():
    """Allow the user to choose an LLM model."""
    print("\nAvailable LLM Models:")
    for key, model in AVAILABLE_MODELS.items():
        print(f"{key}. {model}")

    choice = input("Select a model (1/2/3): ").strip()
    return AVAILABLE_MODELS.get(choice, "gpt-4")  # Default to GPT-4 if invalid choice

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
    AGENT_ID = "17bb7886-6ef6-4d00-8fe3-8d5ac8ee445d"  # Replace with your actual agent ID

    user_input = input("\nEnter your question: ").strip()
    selected_model = choose_model()

    messages = [{"role": "user", "content": user_input}]
    
    use_stream = input("\nEnable streaming? (y/n): ").lower().strip() == "y"
    
    chat_with_agent(agent_id=AGENT_ID, messages=messages, model=selected_model, stream=use_stream)
