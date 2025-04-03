from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain_groq import ChatGroq

from database.models import session, Conversation

class PDFQueryAgent:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.db = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db")
        self.db.persist()
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile"),
            chain_type="stuff",
            retriever=self.db.as_retriever()
        )
    
    def query(self, question: str) -> str:
        existing = session.query(Conversation).filter_by(query=question).first()
        if existing:
            return f"🧠 (From memory) {existing.result}"
        result = self.qa_chain.run(question)
        session.add(Conversation(query=question, result=result, filename=self.pdf_path))
        session.commit()
        return result