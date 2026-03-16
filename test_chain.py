from rag_agent import get_rag_chain
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

try:
    print("Initializing Smart Concierge with Fallback...")
    chain = get_rag_chain()
    print("Sending test query...")
    res = chain.invoke({
        "input": "Namaskaram! Tell me about Novotel services.",
        "chat_history": []
    })
    print(f"Concierge Response: {res['answer']}")
except Exception as e:
    print(f"Critical System Error: {e}")
