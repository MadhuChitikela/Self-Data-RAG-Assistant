import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def get_rag_chain():
    # Initialize Embeddings & Vector Store
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    index_name = "novotel-hf"
    
    # Initialize vectorstore and retriever
    vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Initialize LLMs
    # Primary: Gemini
    gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.3)
    
    # Fallback: Groq (Llama 3)
    groq_llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.3)
    
    # Combine with fallback logic
    llm = gemini_llm.with_fallbacks([groq_llm])

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Answer question prompt
    system_prompt = """You are the Novotel Global Smart Concierge, a world-class virtual assistant.
You are speaking to a guest of Novotel, which is a leading global brand of Accor. 

Your job is to:
1. GLOBAL MULTILINGUAL: While you are currently serving the Hyderabad Convention Centre, you must be able to understand and respond in ANY language requested by the guest (English, Telugu, Tenglish, French, Spanish, Hindi, etc.). Always match the guest's warmth and language.
2. GREETING: If they speak in Telugu/Tenglish, respond with local warmth (e.g. "Namaskaram!"). If they speak in French, use "Bonjour!".
3. BRAND AUTHORITY: You represent the Novotel "Longevity Everyday" philosophy. Use the provided context about bedding, wellness pillars, and family offers.
4. HOSPITALITY: Address guest needs (budget, food preferences, transport) with 5-star professionalism.
5. STYLE: Maintain a sophisticated, friendly, and helpful tone. Consistent with the Novotel brand identity.

Knowledge Context:
{context}

Respond as the Novotel Global Concierge. If a request is outside the provided context, politely guide them based on general Novotel global standards.
"""
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    # LCEL RAG chain that uses user input directly for retrieval
    rag_chain = (
        RunnablePassthrough.assign(
            context=(lambda x: format_docs(retriever.invoke(x["input"])))
        )
        | qa_prompt
        | llm
        | StrOutputParser()
    )
    
    # Wrap it to return the exact same dictionary format as before
    class WrappedChain:
        def __init__(self, chain):
            self.chain = chain
            
        def invoke(self, inputs):
            answer = self.chain.invoke(inputs)
            return {"answer": answer}
            
    return WrappedChain(rag_chain)
