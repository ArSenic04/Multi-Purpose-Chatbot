# from .CodeGen import CodeGPTPlus
from codegpt import CodeGPTPlus

# Initialize CodeGPT instance
dhi_codebot = CodeGPTPlus()

class DHI_CodeBot:
    def __init__(self):
        self.agent_id = "17bb7886-6ef6-4d00-8fe3-8d5ac8ee445d"
    
    def query(self, question: str) -> str:
        try:
            response = dhi_codebot.chat_completion(
                agent_id=self.agent_id, 
                messages=[{"role": "user", "content": question}]
            )
            return response
        except Exception as e:
            return f"❌ Error processing query: {str(e)}"