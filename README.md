# 🏨 Novotel Smart Concierge: Self-Data RAG Agent

A premium, production-ready **Retrieval-Augmented Generation (RAG)** application designed for the hospitality industry. This agent (named **Aria**) serves as a 5-star digital concierge for Novotel Hyderabad, processing guest requests using custom hotel knowledge and a sophisticated multi-model architecture.

---

## 🌟 Key Features

- **Self-Data RAG Pipeline**: Uses a custom-built knowledge base (`novotel_info.txt`) and service catalog (`novotel_services.json`).
- **Multi-Model Fallback Engine**: 
  - **Primary**: Google Gemini 1.5 Flash (via LangChain).
  - **Fallback**: Groq (Llama 3.3 70B) — Ensures 100% uptime if Gemini encounters latency or API issues.
- **Tenglish Support**: Deeply optimized to understand and respond in **Tenglish** (a mix of Telugu and English), providing a personalized local experience.
- **Dynamic Service Discovery**: Real-time synchronization with the JSON service database for accurate pricing and availability.
- **Premium UI/UX**: Built with Streamlit, following the official **Novotel Hyderabad Convention Centre** brand identity (Montserrat typography, sharp corporate edges, and Space Blue palette).
- **Auto-Scrolling Concierge**: Intelligent chat interface that auto-scrolls and manages session history for seamless interaction.

---

## 🛠️ Technical Stack

- **Core**: Python & Streamlit
- **Orchestration**: LangChain (LCEL)
- **Vectors & Embeddings**: 
  - **Vector DB**: Pinecone
  - **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **LLMs**: Google Gemini 1.5 Flash & Groq (Llama 3.3 70B)
- **Environment**: Dotenv for secure key management

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/MadhuChitikela/Self-Data-RAG-Assistant.git
cd Self-Data-RAG-Assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=your_environment
```

### 4. Run the Application
```bash
streamlit run app.py
```

---

## 📁 Project Structure

- `app.py`: Main UI component and Streamlit dashboard.
- `rag_agent.py`: Core logic for the RAG chain and multi-model fallback.
- `novotel_vector_store.py`: Script to index and push self-data to Pinecone.
- `novotel_services.json`: Dynamic database for rooms, dining, and spa treatments.
- `novotel_info.txt`: The primary "brain" text for the concierge.

---

## 🤵 Persona: Aria
Aria is designed to be helpful, professional, and culturally aware. Whether asked about airport transfers, budget-friendly rooms, or spicy Andhra food, she leverages her indexed knowledge to provide precise, brand-authorized answers.

---

*Developed with ❤️ for Novotel Hyderabad.*
