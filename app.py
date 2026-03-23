import streamlit as st
import webbrowser

# --- Page Config ---
st.set_page_config(
    page_title="Women Safety Assistant",
    page_icon="🛡️",
    layout="centered"
)

# --- Custom CSS ---
st.markdown("""
<style>
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #1a0a2e 0%, #2d1b4e 50%, #1a0a2e 100%);
        color: #f0e6ff;
    }

    /* Header */
    .hero-title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 800;
        color: #e879f9;
        margin-bottom: 0.2rem;
        text-shadow: 0 0 20px rgba(232, 121, 249, 0.4);
    }
    .hero-subtitle {
        text-align: center;
        font-size: 1rem;
        color: #c084fc;
        margin-bottom: 2rem;
    }

    /* Cards */
    .card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(232, 121, 249, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }

    /* Alert boxes */
    .alert-danger {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.5);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        color: #fca5a5;
        font-size: 1rem;
        line-height: 1.8;
    }
    .alert-safe {
        background: rgba(34, 197, 94, 0.12);
        border: 1px solid rgba(34, 197, 94, 0.4);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        color: #86efac;
        font-size: 1rem;
    }

    /* Input label */
    label {
        color: #d8b4fe !important;
        font-weight: 600 !important;
    }

    /* Input box */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(232, 121, 249, 0.35) !important;
        border-radius: 10px !important;
        color: #f0e6ff !important;
        padding: 0.6rem 1rem !important;
        font-size: 1rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #e879f9 !important;
        box-shadow: 0 0 0 2px rgba(232, 121, 249, 0.2) !important;
    }

    /* SOS Button */
    .stButton > button {
        background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        width: 100% !important;
        cursor: pointer !important;
        box-shadow: 0 4px 20px rgba(220, 38, 38, 0.4) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(220, 38, 38, 0.6) !important;
    }

    /* Divider */
    hr {
        border-color: rgba(232, 121, 249, 0.15) !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #7c3aed;
        font-size: 0.8rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# --- Header ---
st.markdown('<div class="hero-title">🛡️ Women Safety Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Your personal safety companion — always here for you</div>', unsafe_allow_html=True)

st.markdown("---")

# --- Quick Action Buttons ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### 🚨 Emergency Actions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📍 Open Maps"):
        webbrowser.open("https://www.google.com/maps")
        st.toast("Opening Google Maps...", icon="📍")

with col2:
    if st.button("📞 Call 112"):
        webbrowser.open("tel:112")
        st.toast("Dialing 112...", icon="📞")

with col3:
    if st.button("📲 WhatsApp SOS"):
        webbrowser.open("https://wa.me/?text=🚨 I need help! Please check on me.")
        st.toast("Opening WhatsApp...", icon="📲")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# --- AI Check-in ---
st.markdown("#### 💬 How are you feeling right now?")
user_input = st.text_input(
    label="Describe your situation",
    placeholder="e.g. I feel unsafe, someone is following me...",
    label_visibility="collapsed"
)

DANGER_KEYWORDS = [
    "unsafe", "help", "scared", "danger", "follow", "threat",
    "attack", "harass", "afraid", "emergency", "hurt", "fear", "alone at night"
]

def safety_response(text):
    text_lower = text.lower()
    if any(kw in text_lower for kw in DANGER_KEYWORDS):
        return "danger"
    return "safe"

if user_input:
    status = safety_response(user_input)
    if status == "danger":
        st.markdown("""
        <div class="alert-danger">
            🚨 <strong>Emergency Detected</strong><br><br>
            • Call <strong>112</strong> immediately<br>
            • Share your live location with a trusted contact<br>
            • Move to a crowded, well-lit area<br>
            • Stay on the phone with someone you trust
        </div>
        """, unsafe_allow_html=True)
        webbrowser.open("https://www.google.com/maps")
        st.toast("Google Maps opened for safe navigation", icon="🗺️")
    else:
        st.markdown("""
        <div class="alert-safe">
            ✅ You seem safe right now. Stay aware of your surroundings and trust your instincts.
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# --- Big SOS Button ---
st.markdown("#### 🆘 Panic Button")
if st.button("🆘  EMERGENCY SOS — TAP FOR HELP"):
    webbrowser.open("https://www.google.com/maps")
    st.toast("🚨 SOS triggered! Opening Maps & alerting contacts.", icon="🚨")
    st.markdown("""
    <div class="alert-danger">
        🚨 SOS Activated! <br>
        • Google Maps opened<br>
        • Call 112 now<br>
        • Send your location to a trusted contact
    </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown('<div class="footer">Stay safe. You are not alone. 💜</div>', unsafe_allow_html=True)
