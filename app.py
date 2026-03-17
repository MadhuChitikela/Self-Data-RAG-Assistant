import streamlit as st
import os
from rag_agent import get_rag_chain

# ── MUST BE FIRST ──
st.set_page_config(
    page_title="Novotel Digital Services",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── DATA ──
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaskaram! Welcome to Novotel. I am Aria, your personal concierge. How may I make your stay exceptional today?"}
    ]
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Accommodations"

# ── RAG INITIALIZATION ──
@st.cache_resource
def load_rag_chain():
    try:
        if not os.getenv("GOOGLE_API_KEY") or not os.getenv("PINECONE_API_KEY"):
            return None
        return get_rag_chain()
    except Exception as e:
        st.error(f"Error loading RAG chain: {e}")
        return None

rag_layer = load_rag_chain()

SERVICES = {
    "Accommodations": [
        {"name": "Standard Smart Room", "desc": "28 sqm · City view", "price": "7,500", "icon": "🛏️"},
        {"name": "Superior Family Suite", "desc": "48 sqm · King bed", "price": "12,500", "icon": "🛏️"},
        {"name": "Presidential Suite", "desc": "90 sqm · Butler included", "price": "38,000", "icon": "🛏️"},
    ],
    "Dining": [
        {"name": "The Glass Kitchen", "desc": "International buffet", "price": "Incl.", "icon": "🍽️"},
        {"name": "Ember and Gold", "desc": "Fine dining", "price": "3,500", "icon": "🍽️"},
    ],
    "Wellness": [
        {"name": "Lumina Spa", "desc": "Full treatments", "price": "4,500", "icon": "💆"},
        {"name": "Infinity Pool", "desc": "Rooftop · Heated", "price": "Incl.", "icon": "🏊"},
    ]
}

def bot_reply(msg):
    # Try RAG first
    if rag_layer:
        try:
            # Convert session messages to RAG history format
            history = []
            for m in st.session_state.messages[-10:]: # last 10 msgs
                role = "human" if m["role"] == "user" else "ai"
                history.append((role, m["content"]))
            
            response = rag_layer.invoke({"input": msg, "chat_history": history})
            return response.get("answer", "I apologize, I'm having trouble retrieving an answer right now.")
        except Exception as e:
            return f"Aria (Fallback): I encountered an issue: {str(e)}. How can I help you manually?"

    # Dummy fallback if RAG is not configured
    m = msg.lower()
    if "spa" in m: return "Lumina Spa has availability today at 3 PM. Shall I book it?"
    if "room" in m: return "Our Standard Smart Rooms are available from Rs 7,500. Would you like to see the views?"
    if "food" in m: return "In-room dining is 24/7. Shall I send the menu to your room?"
    return "Thank you! I am Aria, your concierge. I can help with rooms, spa, or dining."

# ── STYLES ──
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background: #F8F4EE;}
    [data-testid="stHeader"] {background: rgba(0,0,0,0);}
    .stButton>button {
        border-radius: 2px;
        border: 1px solid #C9A96E;
        color: #C9A96E;
        background: transparent;
    }
    .stButton>button:hover {
        background: #C9A96E;
        color: #0D1B2A;
    }
</style>
""", unsafe_allow_html=True)

# ── UI ──
# Nav
st.markdown('<div style="background:#0D1B2A;padding:1rem 2.5rem;display:flex;justify-content:space-between;align-items:center;">'
            '<div style="color:#C9A96E;font-size:22px;letter-spacing:3px;">NOVOTEL</div>'
            '<div style="color:white;font-size:12px;">HYDERABAD</div></div>', unsafe_allow_html=True)

# Hero
st.markdown('<div style="background:#0D1B2A;padding:3rem 4rem;min-height:200px;">'
            '<h1 style="color:white;font-size:48px;">Live the Art of <br><span style="color:#C9A96E;">Longevity</span></h1>'
            '<p style="color:gray;">Professional Digital Concierge Service</p></div>', unsafe_allow_html=True)

left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("Services & Amenities")
    tabs = st.tabs(list(SERVICES.keys()))
    for i, tab in enumerate(tabs):
        with tab:
            cat = list(SERVICES.keys())[i]
            for item in SERVICES[cat]:
                st.markdown(f"""
                <div style="background:white;padding:1rem;border-radius:5px;margin-bottom:10px;border-left:4px solid #C9A96E;">
                    <b>{item['icon']} {item['name']}</b><br>
                    <small>{item['desc']}</small><br>
                    <span style="color:#8A6D3B;">Rs {item['price']}</span>
                </div>
                """, unsafe_allow_html=True)

with right:
    st.subheader("Aria Concierge")
    chat_container = st.container(height=400)
    with chat_container:
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.write(m["content"])

    if prompt := st.chat_input("How can I help you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.write(prompt)
        
        reply = bot_reply(prompt)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with chat_container:
            with st.chat_message("assistant"):
                st.write(reply)
        st.rerun()
