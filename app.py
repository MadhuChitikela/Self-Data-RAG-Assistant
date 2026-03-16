import streamlit as st
import json
import os
from rag_agent import get_rag_chain
from langchain_core.messages import HumanMessage, AIMessage

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Novotel Digital Services",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── DATA LOADING & AI INITIALIZATION ───────────────────────────────────────────
@st.cache_data
def load_dynamic_services():
    try:
        if os.path.exists('novotel_services.json'):
            with open('novotel_services.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                categories = {}
                for item in data:
                    cat = item.get("category", "Other").title()
                    if cat not in categories: categories[cat] = []
                    categories[cat].append({
                        "name": item.get("dish_name", "Service"),
                        "desc": f"{item.get('main_ingredient', '')} · {item.get('veg_nonveg', '')}",
                        "price": f"{item.get('price', '0')}",
                        "tag": "Featured" if item.get("spice_level") == "special" else "",
                        "icon": "🛏️" if "Accommodations" in cat else ("🍽️" if "Dining" in cat else ("💆" if "Wellness" in cat else "✦"))
                    })
                return categories
        return {}
    except Exception: return {}

DYNAMIC_SERVICES = load_dynamic_services()

AMENITIES = [
    ("📍", "Premium Location",  "City centre & business hub"),
    ("🤝", "24/7 Concierge",    "Smart AI assistance"),
    ("💎", "ALL Membership",    "Exclusive rewards & perks"),
    ("🌿", "Planet 21",         "Zero single-use plastics"),
    ("📱", "Smart Rooms",       "Voice & app controlled"),
]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "text": "Namaskaram! Welcome to Novotel. I am Aria, your personal concierge. How may I make your stay exceptional today?"}
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Namaskaram! Welcome to Novotel. I am Aria, your personal concierge. How may I make your stay exceptional today?")
    ]

if "active_tab" not in st.session_state:
    available_tabs = list(DYNAMIC_SERVICES.keys())
    st.session_state.active_tab = available_tabs[0] if available_tabs else "Accommodations"

# ── DIAGNOSTICS FOR CLOUD ──
if "agent_chain" not in st.session_state:
    required_keys = ["GOOGLE_API_KEY", "GROQ_API_KEY", "PINECONE_API_KEY"]
    missing_keys = [k for k in required_keys if not os.getenv(k)]
    
    if missing_keys:
        st.error(f"⚠️ Missing Secrets: {', '.join(missing_keys)}. Please add them in the Space Settings > Variables and secrets.")
        st.stop()
    
    with st.spinner("Initializing Concierge..."):
        try:
            st.session_state.agent_chain = get_rag_chain()
        except Exception as e:
            st.error(f"❌ Initialization Error: {e}")
            st.stop()

def get_ai_response(msg):
    st.session_state.chat_history.append(HumanMessage(content=msg))
    try:
        response = st.session_state.agent_chain.invoke({
            "input": msg,
            "chat_history": st.session_state.chat_history[:-1]
        })
        answer = response["answer"]
    except Exception as e:
        answer = f"I apologize, I'm having trouble connecting to my knowledge base. Error: {e}"
    st.session_state.chat_history.append(AIMessage(content=answer))
    return answer

# ── GLOBAL STYLES (Novotel Brand Specific) ──
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&family=Playfair+Display:ital,wght@1,400&display=swap" rel="stylesheet">'
    '<style>'
    '#MainMenu,footer,header{visibility:hidden!important}'
    '.block-container{padding:0!important;max-width:100%!important}'
    '.stApp{background:#FFFFFF!important;font-family:Montserrat,sans-serif!important}'
    'section[data-testid="stSidebar"]{display:none!important}'
    '[data-testid="column"]{padding:0!important}'
    '[data-testid="stVerticalBlock"]{gap:0!important}'
    
    '/* Button styling (Sharp edges as per brand) */'
    '.stButton>button{'
        'background:transparent!important;'
        'border:1px solid #1E22AA!important;'
        'color:#1E22AA!important;'
        'font-family:Montserrat,sans-serif!important;'
        'font-size:12px!important;'
        'letter-spacing:.1em!important;'
        'text-transform:uppercase!important;'
        'padding:10px 20px!important;'
        'border-radius:0px!important;'
        'transition:all .2s!important;'
        'white-space:nowrap!important;'
        'font-weight: 500!important}'
    '.stButton>button:hover{background:#1E22AA!important;color:#FFFFFF!important}'
    
    '/* Primary Chat Bubble (Bot) */'
    '.bot-bubble {'
        'background: #F5F5F5 !important;'
        'color: #333333 !important;'
        'padding: 15px !important;'
        'border-radius: 0px !important;'
        'border-left: 4px solid #1E22AA !important;'
        'font-size: 14px !important;'
        'line-height: 1.6 !important;'
        'margin-bottom: 15px !important;'
    '}'
    
    '/* User Chat Bubble */'
    '.user-bubble {'
        'background: #1E22AA !important;'
        'color: #FFFFFF !important;'
        'padding: 15px !important;'
        'border-radius: 0px !important;'
        'text-align: right !important;'
        'font-size: 14px !important;'
        'margin-left: auto !important;'
        'width: fit-content !important;'
        'max-width: 85% !important;'
        'margin-bottom: 15px !important;'
    '}'

    '.stTextInput>div>div>input{'
        'background:#FFFFFF!important;'
        'border:1px solid #DDDDDD!important;'
        'border-radius:0px!important;color:#333333!important;'
        'font-family:Montserrat,sans-serif!important;font-size:14px!important;'
        'padding:12px 15px!important;height:45px!important}'
    '.stTextInput>div>div>input:focus{border-color:#1E22AA!important;box-shadow:none!important}'
    '.stTextInput label{display:none!important}'

    '.send-btn .stButton>button{background:#1E22AA!important;border:none!important;'
    'color:#FFFFFF!important;font-weight:600!important;width:100%!important;'
    'padding:11px!important;font-size:18px!important}'
    
    '.tab-btn .stButton>button{'
    'background:transparent!important;border:none!important;border-bottom:3px solid transparent!important;'
    'border-radius:0!important;color:#777777!important;font-size:12px!important;'
    'letter-spacing:.12em!important;text-transform:uppercase!important;'
    'padding:15px 10px!important;width:100%!important;box-shadow:none!important}'
    '.tab-btn.active .stButton>button{border-bottom:3px solid #1E22AA!important;color:#1E22AA!important;font-weight:600!important}'
    '</style>',
    unsafe_allow_html=True,
)

# ── NAV (Novotel Style) ──
st.markdown(
    '<div style="background:#FFFFFF;border-bottom:1px solid #EEEEEE;padding:0 3rem;height:80px;display:flex;'
    'align-items:center;justify-content:space-between;position:sticky;top:0;z-index:999;">'
    '<div style="display:flex;flex-direction:column;">'
    '<div style="font-family:Montserrat,sans-serif;font-size:24px;font-weight:600;color:#1E22AA;letter-spacing:.2em;">NOVOTEL</div>'
    '<div style="font-size:10px;text-transform:uppercase;color:#777777;letter-spacing:.1em;margin-top:-5px;">Hyderabad Convention Centre</div>'
    '</div>'
    '<div style="display:flex;gap:2.5rem;align-items:center;">'
    + "".join(
        f'<span style="color:{"#1E22AA" if i==0 else "#333333"};font-size:12px;font-weight:500;'
        f'letter-spacing:.12em;text-transform:uppercase;cursor:pointer;">{link}</span>'
        for i, link in enumerate(["Home", "Rooms", "Dining", "Wellness", "MICE"])
    ) +
    '<button style="background:#1E22AA;border:none;color:#FFFFFF;padding:10px 25px;font-size:12px;'
    'letter-spacing:.12em;text-transform:uppercase;cursor:pointer;font-family:Montserrat,sans-serif;'
    'font-weight:600;transition:opacity .2s;">Book a Room</button>'
    '</div></div>',
    unsafe_allow_html=True,
)

# ── HERO ──
st.markdown(
    '<div style="position:relative;background:#00446E;min-height:500px;display:flex;'
    'align-items:center;padding:0 5rem;overflow:hidden;">'
    '<div style="position:absolute;inset:0;background:linear-gradient(rgba(0,0,0,0.3),rgba(0,0,0,0.3)), url(\'https://novotelhyderabad.com/wp-content/uploads/2021/08/Exterior-Novotel-Hyderabad.jpg\'); background-size:cover; background-position:center;"></div>'
    '<div style="position:relative;z-index:2;max-width:700px;background:rgba(255,255,255,0.9);padding:3rem;border-left:8px solid #1E22AA;">'
    '<p style="font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:#1E22AA;margin-bottom:1rem;font-weight:600;">Welcome to Grandeur</p>'
    '<h1 style="font-family:Montserrat,sans-serif;font-size:48px;font-weight:500;color:#333333;line-height:1.2;margin-bottom:1.5rem;text-transform:uppercase;letter-spacing:.05em;">'
    'Experience <em style="font-family:Playfair Display,serif;text-transform:none;font-weight:400;">Modern Elegance</em></h1>'
    '<p style="font-size:15px;color:#555555;line-height:1.8;margin-bottom:2.5rem;">Located in the heart of the business district, our hotel offers seamless connectivity and sophisticated comfort for the modern traveler.</p>'
    '<button style="background:#1E22AA;color:#FFFFFF;border:none;padding:15px 40px;font-family:Montserrat,sans-serif;font-size:12px;'
    'letter-spacing:.2em;text-transform:uppercase;font-weight:600;cursor:pointer;">Discover More</button>'
    '</div></div>',
    unsafe_allow_html=True,
)

# ── AMENITY STRIP ──
amenities = [
    ("📍", "Prime Location", "HITEC City central"),
    ("🤝", "Convention Centre", "Hyderabad's elite venue"),
    ("🍸", "Social Hub", "Lively bars & dining"),
    ("🌿", "Sustainability", "Planet 21 certified"),
    ("🏊", "Wellness", "Pool & Fitness studio"),
]
cells = "".join(
    '<div style="flex:1;text-align:center;padding:2rem 1rem;'
    + ('border-right:1px solid #EEEEEE;' if i < len(amenities)-1 else '')
    + '">'
    + f'<div style="font-size:24px;margin-bottom:10px;">{icon}</div>'
    + f'<div style="font-size:13px;font-weight:600;color:#1E22AA;text-transform:uppercase;letter-spacing:.1em;">{name}</div>'
    + f'<div style="font-size:11px;color:#777777;margin-top:5px;">{sub}</div>'
    + '</div>'
    for i, (icon, name, sub) in enumerate(amenities)
)
st.markdown('<div style="background:#FFFFFF;border-bottom:1px solid #EEEEEE;display:flex;padding:0 3rem;">' + cells + '</div>', unsafe_allow_html=True)

# ── MAIN CONTENT ──
st.markdown('<div style="background:#F9F9F9;padding:4rem 3rem;">', unsafe_allow_html=True)
left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.markdown('<p style="font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:#1E22AA;font-weight:600;margin-bottom:.5rem;">Explore Our World</p>'
                '<h2 style="font-family:Montserrat,sans-serif;font-size:36px;font-weight:400;color:#333333;margin-bottom:2rem;text-transform:uppercase;">Services &amp; Amenities</h2>', unsafe_allow_html=True)
    
    if DYNAMIC_SERVICES:
        st.markdown('<div style="display:flex;margin-bottom:2rem;">', unsafe_allow_html=True)
        tab_list = list(DYNAMIC_SERVICES.keys())
        tab_cols = st.columns(len(tab_list))
        for col, tab in zip(tab_cols, tab_list):
            with col:
                active = tab == st.session_state.active_tab
                st.markdown(f'<div class="tab-btn{"  active" if active else ""}">', unsafe_allow_html=True)
                if st.button(tab, key="tab_" + tab):
                    st.session_state.active_tab = tab
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        for idx, item in enumerate(DYNAMIC_SERVICES[st.session_state.active_tab]):
            tag_html = f'<span style="background:#1E22AA;color:#FFFFFF;font-size:9px;font-weight:600;padding:3px 8px;text-transform:uppercase;margin-left:10px;">{item["tag"]}</span>' if item["tag"] else ""
            st.markdown(
                f'<div style="background:#FFFFFF;border:1px solid #EEEEEE;padding:1.5rem;display:flex;align-items:center;justify-content:space-between;margin-bottom:5px;transition:all .2s;">'
                f'<div style="display:flex;align-items:center;gap:20px;">'
                f'<div style="font-size:22px;">{item["icon"]}</div>'
                f'<div><div style="display:flex;align-items:center;"><span style="font-size:15px;font-weight:600;color:#333333;text-transform:uppercase;letter-spacing:.05em;">{item["name"]}</span>{tag_html}</div>'
                f'<div style="font-size:12px;color:#777777;margin-top:5px;">{item["desc"]}</div></div></div>'
                f'<div style="text-align:right;"><div style="font-size:18px;font-weight:600;color:#1E22AA;">Rs {item["price"]}</div>'
                f'<div style="font-size:10px;color:#999;text-transform:uppercase;">Per Night</div></div></div>', unsafe_allow_html=True
            )
    else: st.info("Index your services in novotel_services.json to see them here.")

with right:
    # Concierge header (Novotel Blue Style)
    st.markdown('<div style="background:#1E22AA;padding:1.5rem;display:flex;align-items:center;gap:15px;">'
                '<div style="width:45px;height:45px;border-radius:0px;background:#FFFFFF;display:flex;align-items:center;justify-content:center;font-size:22px;">🤵</div>'
                '<div><div style="font-size:16px;font-weight:600;color:#FFFFFF;text-transform:uppercase;letter-spacing:.1em;">Aria Concierge</div>'
                '<div style="display:flex;align-items:center;gap:8px;margin-top:4px;"><div style="width:8px;height:8px;border-radius:50%;background:#4CAF82;"></div>'
                '<span style="font-size:11px;color:rgba(255,255,255,0.7);text-transform:uppercase;">Live Assistance</span></div></div>'
                '<div style="margin-left:auto;font-size:9px;font-weight:600;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:.2em;">Novotel Hyatt Hub</div></div>', unsafe_allow_html=True)
    
    # Custom Bubble chat area
    st.markdown('<div id="chat-container" style="background:#FFFFFF;border:1px solid #EEEEEE;padding:1.5rem;height:350px;overflow-y:auto;display:flex;flex-direction:column;">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "bot":
            st.markdown(f'<div class="bot-bubble">{msg["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="user-bubble">{msg["text"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Quick queries (Square Blue buttons)
    st.markdown('<div style="background:#F5F5F5;padding:1rem 1.5rem;border-top:1px solid #EEEEEE;"><span style="font-size:10px;font-weight:600;text-transform:uppercase;color:#1E22AA;letter-spacing:.1em;">Common Requests</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="background:#F5F5F5;padding:0 1.5rem 1rem;">', unsafe_allow_html=True)
    qr_cols = st.columns(4)
    for col, lbl in zip(qr_cols, ["Rooms", "Spa", "Dining", "Check-out"]):
        with col:
            st.markdown('<div class="qr-btn">', unsafe_allow_html=True)
            if st.button(lbl, key=f"qr_{lbl}"):
                st.session_state.messages.append({"role": "user", "text": lbl})
                st.session_state.messages.append({"role": "bot", "text": get_ai_response(lbl)})
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Input (Sharp Blue Style)
    st.markdown('<div style="background:#FFFFFF;padding:1rem 1.5rem 1.5rem;border-top:1px solid #EEEEEE;">', unsafe_allow_html=True)
    ic, bc = st.columns([5, 1])
    with ic: user_input = st.text_input("msg", key="chat_input", placeholder="Type your request here...", label_visibility="collapsed")
    with bc:
        st.markdown('<div class="send-btn">', unsafe_allow_html=True)
        send = st.button("➤", key="send_btn")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if send and user_input.strip():
        st.session_state.messages.append({"role": "user", "text": user_input.strip()})
        st.session_state.messages.append({"role": "bot", "text": get_ai_response(user_input.strip())})
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ── FOOTER (Accor Official Style) ──
st.markdown('<div style="background:#1A2D42;padding:3rem;display:flex;flex-direction:column;align-items:center;gap:2rem;">'
            '<div style="font-family:Montserrat,sans-serif;font-size:28px;font-weight:600;color:#FFFFFF;letter-spacing:.4em;">NOVOTEL</div>'
            '<div style="display:flex;gap:3rem;color:rgba(255,255,255,0.6);font-size:11px;text-transform:uppercase;letter-spacing:.1em;">'
            + "".join(f'<span style="cursor:pointer;">{lnk}</span>' for lnk in ["Privacy Policy", "Legal Links", "Terms of Use", "Accessibility"]) +
            '</div>'
            '<div style="color:rgba(255,255,255,0.3);font-size:10px;">&#169; 2026 Accor Hotel Group. All rights reserved. Hyderabad Convention Centre.</div></div>', unsafe_allow_html=True)
