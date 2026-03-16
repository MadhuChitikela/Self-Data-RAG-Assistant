import streamlit as st

st.set_page_config(
    page_title="Novotel Digital Services",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "text": "Namaskaram! Welcome to Novotel. I am Aria, your personal concierge. How may I make your stay exceptional today?"}
    ]
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Accommodations"

SERVICES = {
    "Accommodations": [
        {"name": "Standard Smart Room",      "desc": "28 sqm · City view · Smart controls",    "price": "7,500",  "tag": "Popular", "icon": "🛏️"},
        {"name": "Superior Family Suite",    "desc": "48 sqm · King bed · Living area",         "price": "12,500", "tag": "",        "icon": "🛏️"},
        {"name": "Executive Panoramic Room", "desc": "35 sqm · Floor-to-ceiling city view",     "price": "15,000", "tag": "",        "icon": "🛏️"},
        {"name": "Presidential Suite",       "desc": "90 sqm · Butler and chauffeur included",  "price": "38,000", "tag": "Luxury",  "icon": "🛏️"},
    ],
    "Dining": [
        {"name": "The Glass Kitchen",        "desc": "International buffet · Open 7 to 11 AM",  "price": "Incl.",  "tag": "",          "icon": "🍽️"},
        {"name": "Ember and Gold",           "desc": "Fine dining · Reservations required",     "price": "3,500",  "tag": "Signature", "icon": "🍽️"},
        {"name": "Sky Lounge Bar",           "desc": "Rooftop cocktails · 5 PM to midnight",    "price": "800+",   "tag": "",          "icon": "🍽️"},
        {"name": "In-Room Dining",           "desc": "24 by 7 · Full kitchen menu delivery",    "price": "500+",   "tag": "",          "icon": "🍽️"},
    ],
    "Wellness": [
        {"name": "Lumina Spa",               "desc": "Full body treatments · Aromatic oils",    "price": "4,500",  "tag": "Featured", "icon": "💆"},
        {"name": "Infinity Pool",            "desc": "Rooftop · Heated year-round",             "price": "Incl.",  "tag": "",         "icon": "🏊"},
        {"name": "Fitness Studio",           "desc": "State-of-the-art equipment · 24 by 7",   "price": "Incl.",  "tag": "",         "icon": "🏋️"},
        {"name": "Yoga Pavilion",            "desc": "Morning sessions · Outdoor terrace",      "price": "800",    "tag": "",         "icon": "🧘"},
    ],
    "Events": [
        {"name": "Grand Ballroom",           "desc": "Seats 500 · Full AV and catering",        "price": "Quote",  "tag": "", "icon": "🎪"},
        {"name": "Boardroom Suites",         "desc": "4 rooms · 8 to 30 persons each",          "price": "8,000",  "tag": "", "icon": "🏢"},
        {"name": "Garden Pavilion",          "desc": "Outdoor · 200 person capacity",           "price": "Quote",  "tag": "", "icon": "🌿"},
        {"name": "Business Centre",          "desc": "Printing · High-speed internet",          "price": "500",    "tag": "", "icon": "💼"},
    ],
}

AMENITIES = [
    ("📍", "Premium Location",  "City centre & business hub"),
    ("🤝", "24/7 Concierge",    "Smart AI assistance"),
    ("💎", "ALL Membership",    "Exclusive rewards & perks"),
    ("🌿", "Planet 21",         "Zero single-use plastics"),
    ("📱", "Smart Rooms",       "Voice & app controlled"),
]

RESPONSES = {
    "room service":  "Our in-room dining runs 24/7 with 40+ dishes from Andhra cuisine to continental classics. I can send the full menu to your room TV or WhatsApp — which works best?",
    "book spa":      "Lumina Spa has availability tomorrow at 10 AM and 3 PM. Our signature Abhyanga massage (90 min) is the most requested. Shall I confirm a slot for you?",
    "spa":           "Lumina Spa has availability tomorrow at 10 AM and 3 PM. Our signature Abhyanga massage (90 min) is the most requested. Shall I confirm a slot for you?",
    "local dining":  "For authentic Telugu cuisine, I recommend Chutneys (2 min walk) and Paradise Biryani (5 min cab). For upscale dining, Kebabs and Kurries at ITC Kohenur is excellent. Shall I arrange transport?",
    "checkout":      "Standard checkout is 12 noon. As our guest, you qualify for a complimentary late checkout until 2 PM on request. Would you like me to arrange that?",
    "wifi":          "Complimentary high-speed Wi-Fi is available throughout the property. Your room network is NOVOTEL-GUEST and the password is printed on your key card envelope.",
    "pool":          "Our heated rooftop infinity pool is open daily from 7 AM to 10 PM. Towels and loungers are provided at no extra charge.",
    "breakfast":     "Breakfast is served at The Glass Kitchen from 7 to 11 AM. We offer Continental, Indian, and live cooking station options. Guests on breakfast packages have full complimentary access.",
    "transport":     "We provide airport transfers (Rs 1,200 one-way), city taxi service, and a complimentary shuttle to Uppal Metro Station every hour. Shall I book something?",
    "book":          "Happy to help with a reservation! Please let me know which service you would like — a room, spa treatment, dining, or event space — and your preferred date and time.",
}

def bot_reply(msg):
    m = msg.lower()
    for key, resp in RESPONSES.items():
        if key in m:
            return resp
    return "Thank you for reaching out. I am connecting you with our team. You can also ask me about rooms, dining, spa, pool, wifi, transport, or checkout."


# ── STYLES ────────────────────────────────────────────────────────────────────
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">'
    '<style>'
    '#MainMenu,footer,header{visibility:hidden!important}'
    '.block-container{padding:0!important;max-width:100%!important}'
    '.stApp{background:#F8F4EE!important;font-family:Jost,sans-serif!important}'
    'section[data-testid="stSidebar"]{display:none!important}'
    '[data-testid="column"]{padding:0!important}'
    '[data-testid="stVerticalBlock"]{gap:0!important}'
    '.element-container{margin:0!important;padding:0!important}'
    '.stButton{margin:0!important}'
    '.stTextInput{margin:0!important}'

    '.stTextInput>div>div>input{'
    'background:rgba(255,255,255,0.07)!important;'
    'border:1px solid rgba(201,169,110,0.35)!important;'
    'border-radius:2px!important;color:white!important;'
    'font-family:Jost,sans-serif!important;font-size:13px!important;'
    'padding:10px 14px!important;height:40px!important}'
    '.stTextInput>div>div>input::placeholder{color:rgba(255,255,255,0.32)!important}'
    '.stTextInput>div>div>input:focus{border-color:rgba(201,169,110,0.65)!important;box-shadow:none!important}'
    '.stTextInput label{display:none!important}'

    '.stButton>button{'
    'background:transparent!important;border:1px solid rgba(201,169,110,0.4)!important;'
    'color:#E8D5B0!important;font-family:Jost,sans-serif!important;font-size:11px!important;'
    'letter-spacing:.07em!important;padding:7px 12px!important;border-radius:2px!important;'
    'transition:all .15s!important;white-space:nowrap!important}'
    '.stButton>button:hover{background:rgba(201,169,110,0.12)!important;border-color:#C9A96E!important;color:#C9A96E!important}'

    '.send-btn .stButton>button{background:#C9A96E!important;border:none!important;'
    'color:#0D1B2A!important;font-weight:500!important;width:100%!important;'
    'padding:9px 4px!important;font-size:18px!important;border-radius:2px!important}'
    '.send-btn .stButton>button:hover{background:#E8D5B0!important}'

    '.tab-btn .stButton>button{'
    'background:transparent!important;border:none!important;border-bottom:2px solid transparent!important;'
    'border-radius:0!important;color:#9B8E7E!important;font-size:11px!important;'
    'letter-spacing:.1em!important;text-transform:uppercase!important;'
    'padding:10px 4px!important;width:100%!important;box-shadow:none!important}'
    '.tab-btn .stButton>button:hover{background:transparent!important;color:#0D1B2A!important;border-color:rgba(201,169,110,0.3)!important}'
    '.tab-active .stButton>button{border-bottom:2px solid #C9A96E!important;color:#0D1B2A!important;font-weight:500!important}'

    '.qr-btn .stButton>button{font-size:11px!important;padding:7px 6px!important;width:100%!important}'
    '</style>',
    unsafe_allow_html=True,
)

# ── NAV ───────────────────────────────────────────────────────────────────────
nav_items = ["Rooms", "Dining", "Wellness", "Events", "Offers"]
links_html = "".join(
    f'<a href="#" style="color:{"#C9A96E" if i==0 else "rgba(255,255,255,.6)"};text-decoration:none;'
    f'font-size:12px;letter-spacing:.12em;text-transform:uppercase;" '
    f'onmouseover="this.style.color=\'#C9A96E\'" '
    f'onmouseout="this.style.color=\'{"#C9A96E" if i==0 else "rgba(255,255,255,.6)"}\'">{item}</a>'
    for i, item in enumerate(nav_items)
)
st.markdown(
    '<div style="background:#0D1B2A;padding:0 2.5rem;height:64px;display:flex;'
    'align-items:center;justify-content:space-between;">'
    '<div style="font-family:Cormorant Garamond,serif;font-size:22px;font-weight:300;'
    'color:#C9A96E;letter-spacing:.3em;">NOVOTEL</div>'
    '<div style="display:flex;gap:2rem;align-items:center;">'
    + links_html
    + '<a href="#" style="background:transparent;border:1px solid #C9A96E;color:#C9A96E;'
    'padding:8px 20px;font-size:11px;letter-spacing:.12em;text-transform:uppercase;'
    'text-decoration:none;font-family:Jost,sans-serif;transition:all .2s;" '
    'onmouseover="this.style.background=\'#C9A96E\';this.style.color=\'#0D1B2A\'" '
    'onmouseout="this.style.background=\'transparent\';this.style.color=\'#C9A96E\'">Book Now</a>'
    '</div></div>',
    unsafe_allow_html=True,
)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="position:relative;background:#0D1B2A;min-height:440px;display:flex;'
    'align-items:center;padding:0 4rem;overflow:hidden;">'
    '<div style="position:absolute;inset:0;background:linear-gradient(135deg,#0D1B2A 0%,#1A2D42 45%,#0A1E30 100%);"></div>'
    '<div style="position:absolute;right:0;top:0;bottom:0;width:42%;background:linear-gradient(to left,rgba(201,169,110,0.05),transparent);"></div>'
    '<div style="position:absolute;right:90px;top:0;width:1px;height:100%;background:linear-gradient(to bottom,transparent,rgba(201,169,110,0.2),transparent);"></div>'
    '<div style="position:absolute;right:190px;top:10%;width:1px;height:80%;background:linear-gradient(to bottom,transparent,rgba(201,169,110,0.08),transparent);"></div>'
    '<div style="position:absolute;right:2rem;bottom:1.5rem;font-family:Cormorant Garamond,serif;font-size:140px;font-weight:300;color:rgba(201,169,110,0.05);line-height:1;user-select:none;">21</div>'
    '<div style="position:relative;z-index:2;padding:4rem 0;">'
    '<p style="font-size:11px;letter-spacing:.25em;text-transform:uppercase;color:#C9A96E;margin-bottom:1rem;">Hyderabad &nbsp;&middot;&nbsp; Uppal</p>'
    '<h1 style="font-family:Cormorant Garamond,serif;font-size:58px;font-weight:300;color:#FFF;line-height:1.1;margin-bottom:1.5rem;">Live the Art of<br><em style="color:#E8D5B0;">Longevity Everyday</em></h1>'
    '<p style="font-size:14px;font-weight:300;color:rgba(255,255,255,0.65);line-height:1.8;max-width:420px;margin-bottom:2rem;">Where timeless luxury meets intelligent service.<br>Every stay is crafted uniquely around you.</p>'
    '<a href="#" style="display:inline-block;background:#C9A96E;color:#0D1B2A;padding:13px 32px;'
    'font-family:Jost,sans-serif;font-size:11px;letter-spacing:.15em;text-transform:uppercase;'
    'font-weight:500;text-decoration:none;" '
    'onmouseover="this.style.background=\'#E8D5B0\'" onmouseout="this.style.background=\'#C9A96E\'">Explore Rooms</a>'
    '</div></div>',
    unsafe_allow_html=True,
)

# ── BOOKING STRIP ─────────────────────────────────────────────────────────────
fields = [("Check-in","18 Mar 2026"),("Check-out","21 Mar 2026"),("Guests","2 Adults, 0 Children"),("Room Type","Any Room")]
fields_html = "".join(
    '<div style="flex:1;padding:0 1.5rem;border-right:1px solid rgba(201,169,110,0.15);">'
    f'<div style="font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#C9A96E;margin-bottom:5px;">{lbl}</div>'
    f'<div style="color:white;font-size:14px;border-bottom:1px solid rgba(201,169,110,0.2);padding-bottom:4px;font-weight:300;">{val}</div>'
    '</div>'
    for lbl, val in fields
)
st.markdown(
    '<div style="background:#1A2D42;padding:1.25rem 2.5rem;display:flex;align-items:center;">'
    + fields_html
    + '<div style="padding-left:1.5rem;flex-shrink:0;">'
    '<a href="#" style="display:inline-block;background:#C9A96E;color:#0D1B2A;padding:12px 28px;'
    'font-family:Jost,sans-serif;font-size:11px;letter-spacing:.15em;text-transform:uppercase;'
    'font-weight:500;text-decoration:none;white-space:nowrap;" '
    'onmouseover="this.style.background=\'#E8D5B0\'" onmouseout="this.style.background=\'#C9A96E\'">Check Availability</a>'
    '</div></div>',
    unsafe_allow_html=True,
)

# ── AMENITY STRIP ─────────────────────────────────────────────────────────────
a_cells = "".join(
    '<div style="flex:1;display:flex;align-items:center;gap:12px;padding:1.25rem 1.2rem;'
    + ('border-right:1px solid rgba(13,27,42,0.07);' if i < len(AMENITIES)-1 else '')
    + '">'
    + f'<div style="width:40px;height:40px;background:#F5EDD8;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:17px;">{icon}</div>'
    + f'<div><div style="font-size:13px;font-weight:500;color:#0D1B2A;">{name}</div>'
    + f'<div style="font-size:11px;color:#9B8E7E;font-weight:300;margin-top:2px;">{sub}</div></div></div>'
    for i, (icon, name, sub) in enumerate(AMENITIES)
)
st.markdown(
    '<div style="background:#FFF;border-top:1px solid rgba(13,27,42,0.06);border-bottom:1px solid rgba(13,27,42,0.06);display:flex;padding:0 2.5rem;">'
    + a_cells + '</div>',
    unsafe_allow_html=True,
)

# ── MAIN GRID ─────────────────────────────────────────────────────────────────
st.markdown('<div style="background:#F8F4EE;padding:3rem 2.5rem 4rem;">', unsafe_allow_html=True)
left, right = st.columns([1.1, 0.9], gap="large")

# ════════════════ LEFT — SERVICES ═════════════════════════════════════════════
with left:
    st.markdown(
        '<p style="font-size:10px;letter-spacing:.25em;text-transform:uppercase;color:#C9A96E;margin-bottom:.3rem;">Explore</p>'
        '<h2 style="font-family:Cormorant Garamond,serif;font-size:34px;font-weight:300;color:#0D1B2A;margin-bottom:1.5rem;">Services &amp; Amenities</h2>',
        unsafe_allow_html=True,
    )

    # Tabs
    st.markdown('<div style="border-bottom:1px solid rgba(13,27,42,0.12);margin-bottom:1.25rem;">', unsafe_allow_html=True)
    t_cols = st.columns(4)
    for col, tab in zip(t_cols, SERVICES.keys()):
        with col:
            is_active = tab == st.session_state.active_tab
            st.markdown(f'<div class="tab-btn{"  tab-active" if is_active else ""}">', unsafe_allow_html=True)
            if st.button(tab, key="tab_" + tab):
                st.session_state.active_tab = tab
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Cards
    cards = ""
    for idx, item in enumerate(SERVICES[st.session_state.active_tab]):
        is_first = idx == 0
        bl = "border-left:3px solid #C9A96E;" if is_first else ""
        tag_html = (
            f'<span style="background:#F5EDD8;color:#8A6D3B;font-size:10px;'
            f'padding:2px 8px;letter-spacing:.05em;margin-left:8px;border-radius:2px;">'
            f'{item["tag"]}</span>'
        ) if item["tag"] else ""
        price_val = item["price"]
        is_numeric = any(c.isdigit() for c in price_val)
        prefix = "Rs " if is_numeric and "+" not in price_val and price_val not in ["Incl.", "Quote"] else ""
        suffix = " /night" if is_numeric else ""
        cards += (
            f'<div style="background:#FFF;{bl}border:1px solid rgba(13,27,42,0.08);'
            f'padding:1.1rem 1.25rem;display:flex;align-items:center;justify-content:space-between;'
            f'margin-bottom:2px;cursor:pointer;transition:all .15s;" '
            f'onmouseover="this.style.borderColor=\'#C9A96E\';this.style.background=\'#FFFBF5\'" '
            f'onmouseout="this.style.borderColor=\'rgba(13,27,42,0.08)\';this.style.background=\'#FFF\'">'
            f'<div style="display:flex;align-items:center;gap:12px;">'
            f'<div style="width:36px;height:36px;background:#F5EDD8;border-radius:50%;'
            f'display:flex;align-items:center;justify-content:center;font-size:15px;">{item["icon"]}</div>'
            f'<div>'
            f'<span style="font-size:14px;font-weight:400;color:#0D1B2A;">{item["name"]}</span>{tag_html}'
            f'<div style="font-size:12px;color:#9B8E7E;margin-top:3px;font-weight:300;">{item["desc"]}</div>'
            f'</div></div>'
            f'<div style="display:flex;align-items:baseline;gap:3px;flex-shrink:0;">'
            f'<span style="font-family:Cormorant Garamond,serif;font-size:19px;color:#8A6D3B;">{prefix}{price_val}</span>'
            f'<span style="font-size:11px;color:#9B8E7E;">{suffix}</span>'
            f'<span style="color:#C9A96E;font-size:18px;margin-left:6px;">&#8250;</span>'
            f'</div></div>'
        )
    st.markdown(cards, unsafe_allow_html=True)


# ════════════════ RIGHT — CONCIERGE ═══════════════════════════════════════════
with right:

    # Build full chat HTML — header + messages + quick replies + input — ONE block
    # Chat messages
    msgs_html = ""
    for msg in st.session_state.messages:
        if msg["role"] == "bot":
            msgs_html += (
                '<div style="max-width:90%;margin-bottom:10px;">'
                '<div style="background:rgba(255,255,255,0.08);color:rgba(255,255,255,0.88);'
                'border:1px solid rgba(255,255,255,0.06);padding:11px 14px;'
                f'font-size:13px;line-height:1.65;font-weight:300;">{msg["text"]}</div></div>'
            )
        else:
            msgs_html += (
                '<div style="max-width:90%;margin-left:auto;margin-bottom:10px;">'
                '<div style="background:#C9A96E;color:#0D1B2A;padding:11px 14px;'
                f'font-size:13px;line-height:1.65;font-weight:400;">{msg["text"]}</div></div>'
            )

    # Full concierge panel — header + scrollable chat (no Streamlit elements)
    st.markdown(
        '<div style="background:#0D1B2A;border-radius:2px;">'

        # Header
        '<div style="padding:1.4rem 1.5rem;border-bottom:1px solid rgba(201,169,110,0.15);'
        'display:flex;align-items:center;gap:12px;">'
        '<div style="width:40px;height:40px;border-radius:50%;background:rgba(201,169,110,0.12);'
        'border:1px solid rgba(201,169,110,0.28);display:flex;align-items:center;'
        'justify-content:center;font-size:18px;">🤵</div>'
        '<div>'
        '<div style="font-size:14px;color:#FFF;">Aria &nbsp;&middot;&nbsp; Smart Concierge</div>'
        '<div style="display:flex;align-items:center;gap:6px;margin-top:3px;">'
        '<div style="width:7px;height:7px;border-radius:50%;background:#4CAF82;"></div>'
        '<span style="font-size:11px;color:rgba(255,255,255,0.45);">Online now</span></div></div>'
        '<div style="margin-left:auto;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#C9A96E;">Virtual Concierge</div>'
        '</div>'

        # Scrollable chat area — auto-scroll via JS
        '<div id="chat-scroll" style="padding:1.25rem 1.5rem;height:320px;overflow-y:auto;'
        'display:flex;flex-direction:column;">'
        + msgs_html +
        '</div>'

        # Quick replies label
        '<div style="padding:.65rem 1.5rem .4rem;border-top:1px solid rgba(201,169,110,0.1);">'
        '<span style="font-size:10px;letter-spacing:.12em;text-transform:uppercase;'
        'color:rgba(255,255,255,0.28);">Quick requests</span></div>'

        '</div>',
        unsafe_allow_html=True,
    )

    # Auto-scroll chat to bottom via JS
    st.markdown(
        '<script>'
        'const el=document.getElementById("chat-scroll");'
        'if(el){el.scrollTop=el.scrollHeight;}'
        '</script>',
        unsafe_allow_html=True,
    )

    # Quick reply buttons — inside dark bg wrapper
    st.markdown('<div style="background:#0D1B2A;padding:.25rem 1.5rem .75rem;">', unsafe_allow_html=True)
    qr_cols = st.columns(4)
    qr_labels = ["Room service", "Book spa", "Local dining", "Checkout"]
    for col, lbl in zip(qr_cols, qr_labels):
        with col:
            st.markdown('<div class="qr-btn">', unsafe_allow_html=True)
            if st.button(lbl, key="qr_" + lbl):
                st.session_state.messages.append({"role": "user", "text": lbl})
                st.session_state.messages.append({"role": "bot",  "text": bot_reply(lbl)})
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Input row — inside dark bg
    st.markdown(
        '<div style="background:#0D1B2A;padding:.5rem 1.5rem 1.25rem;'
        'border-top:1px solid rgba(201,169,110,0.1);border-radius:0 0 2px 2px;">',
        unsafe_allow_html=True,
    )
    ic, bc = st.columns([5, 1])
    with ic:
        user_input = st.text_input(
            "msg", key="chat_input",
            placeholder="Ask Aria anything about your stay...",
            label_visibility="collapsed",
        )
    with bc:
        st.markdown('<div class="send-btn">', unsafe_allow_html=True)
        send_clicked = st.button("➤", key="send_btn")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Process input (after both columns rendered)
    if send_clicked and user_input and user_input.strip():
        st.session_state.messages.append({"role": "user", "text": user_input.strip()})
        st.session_state.messages.append({"role": "bot",  "text": bot_reply(user_input.strip())})
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)  # close main padding div

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="background:#0D1B2A;padding:2rem 2.5rem;display:flex;align-items:center;justify-content:space-between;">'
    '<div style="font-family:Cormorant Garamond,serif;font-size:20px;font-weight:300;color:#C9A96E;letter-spacing:.3em;">NOVOTEL</div>'
    '<div style="font-size:11px;color:rgba(255,255,255,0.3);letter-spacing:.06em;">&#169; 2026 Accor. All rights reserved.</div>'
    '<div style="display:flex;gap:1.5rem;">'
    + "".join(
        f'<a href="#" style="font-size:11px;color:rgba(255,255,255,0.4);text-decoration:none;'
        f'letter-spacing:.08em;text-transform:uppercase;" '
        f'onmouseover="this.style.color=\'#C9A96E\'" onmouseout="this.style.color=\'rgba(255,255,255,0.4)\'">{t}</a>'
        for t in ["Privacy", "Terms", "Contact", "Careers"]
    )
    + '</div></div>',
    unsafe_allow_html=True,
)
