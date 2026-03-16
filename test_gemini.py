from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")
    res = llm.invoke("Hello, are you there?")
    print(f"Success: {res.content}")
except Exception as e:
    print(f"Error: {e}")
