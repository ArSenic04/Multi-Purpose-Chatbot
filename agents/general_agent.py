from langchain_groq import ChatGroq
from database.models import session, Conversation

class GeneralAgent:
    def __init__(self, chat_interface):
        self.llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")
        self.chat_interface = chat_interface
        self.chat_interface.send("🤖 You can ask any queries related to Amazon Ads.", user="System", respond=False)

    def query(self, question: str) -> str:
        try:
            existing = session.query(Conversation).filter_by(query=question).first()
            if existing:
                return f"🧠 (From memory) {existing.result}"
            
            system_prompt = "You are an expert in Amazon Ads. Provide precise answers related to Amazon advertising strategies, campaign optimization, bid management, and related queries."
            response = self.llm.invoke([{"role": "system", "content": system_prompt}, {"role": "user", "content": question}])

            session.add(Conversation(query=question, result=response.content, filename="GeneralAgent"))
            session.commit()
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f"❌ Error processing query: {str(e)}"