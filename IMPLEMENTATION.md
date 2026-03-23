# Building a Women Safety Assistant with Python & Streamlit

> A step-by-step deep dive into how I built a real-time safety companion app — from idea to deployment — using nothing but Python, Streamlit, and a bit of CSS magic.

---

## Why I Built This

Personal safety is something every woman thinks about — walking home at night, travelling alone, being in an unfamiliar place. Most safety apps are either too complex, require account sign-ups, or are buried behind paywalls.

I wanted to build something different: **open, instant, and zero-friction**. No login. No installation. Just open a browser, and your safety tools are right there.

The goal was simple — if someone is in a scary situation, they shouldn't have to think. One tap should do everything: open maps, alert contacts, call emergency services.

---

## What the App Does

At its core, the Women Safety Assistant does three things:

1. **Quick emergency actions** — one-tap buttons to open Google Maps, call 112, or send a WhatsApp SOS
2. **AI-powered check-in** — the user describes how they feel, and the app detects danger signals in their words
3. **Panic SOS button** — a single big button that simultaneously opens Maps and WhatsApp with a pre-filled emergency message

It's built entirely in Python using Streamlit, which means it runs in the browser with zero frontend code — no React, no HTML files, no JavaScript.

---

## Tech Stack

| Layer            | Technology                            | Why                                           |
| ---------------- | ------------------------------------- | --------------------------------------------- |
| Framework        | [Streamlit](https://streamlit.io)     | Rapid Python-to-web UI, no frontend needed    |
| Language         | Python 3.8+                           | Simple, readable, widely supported            |
| Styling          | Custom CSS injected via `st.markdown` | Full design control over Streamlit's defaults |
| External Actions | Python `webbrowser` module            | Opens URLs, phone dialers, WhatsApp links     |
| Font             | Inter (Google Fonts)                  | Clean, modern, highly readable                |
| Deployment       | Streamlit Community Cloud             | Free, one-click deploy from GitHub            |

---

## Project Structure

The entire app lives in two files. That's intentional — simplicity is a feature.

```
women-safety-app/
├── app.py            # The entire application — UI, logic, styling
└── requirements.txt  # Just one line: streamlit
```

No `src/` folders, no config files, no build steps. Anyone can clone this and run it in under a minute.

---

## Setting Up

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/your-username/women-safety-app.git
cd women-safety-app

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501` automatically.

---

## Implementation Deep Dive

### Step 1 — Page Configuration

The very first thing in `app.py` is the page config. Streamlit requires this to be called before any other UI code.

```python
st.set_page_config(
    page_title="Women Safety Assistant",
    page_icon="🛡️",
    layout="centered"
)
```

`layout="centered"` keeps the content in a readable column — important for a safety app that needs to be scannable at a glance, especially under stress.

---

### Step 2 — Overriding Streamlit's Default Styles

Streamlit gives you a functional UI out of the box, but it looks generic. To make this feel like a real product, I injected a full CSS block using:

```python
st.markdown("""<style> ... </style>""", unsafe_allow_html=True)
```

The `unsafe_allow_html=True` flag is what allows raw HTML and CSS to be rendered. Streamlit warns against it for untrusted content, but since we're writing our own CSS, it's perfectly safe here.

**The design language I went with:**

- **Dark purple gradient background** — deep, serious, but not aggressive. Purple is associated with protection and calm.
- **Glassmorphism cards** — semi-transparent panels with `rgba` backgrounds and blurred borders give depth without being distracting.
- **Color-coded action buttons** — each button has a distinct color so users can identify them instantly without reading the label.
- **Left-bordered alert boxes** — a thick colored left border (red for danger, green for safe) is a universally understood visual pattern for status messages.

```css
.stApp {
  background: linear-gradient(160deg, #0f0720 0%, #1e0a3c 40%, #2a0f4a 100%);
}

.glass {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 1.6rem;
}
```

One tricky part: Streamlit renders buttons inside nested `div` elements with `data-testid` attributes. To style individual buttons differently, I used CSS nth-child selectors targeting those test IDs:

```css
/* Blue for Maps */
div[data-testid='stColumn']:nth-child(1) div[data-testid='stButton'] button {
  background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
}

/* Amber for Call */
div[data-testid='stColumn']:nth-child(2) div[data-testid='stButton'] button {
  background: linear-gradient(135deg, #d97706, #b45309) !important;
}

/* Green for WhatsApp */
div[data-testid='stColumn']:nth-child(3) div[data-testid='stButton'] button {
  background: linear-gradient(135deg, #16a34a, #15803d) !important;
}
```

This is a bit of a hack — Streamlit doesn't officially support per-button styling — but it works reliably across modern browsers.

---

### Step 3 — Quick Action Buttons

The three emergency action buttons are the most important part of the UI. They need to be immediately visible and tappable.

```python
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📍 Open Maps"):
        webbrowser.open("https://www.google.com/maps")
        st.toast("Opening Google Maps...", icon="📍")

with col2:
    if st.button("📞 Call 112"):
        webbrowser.open("tel:112")
        st.toast("Dialing emergency services...", icon="📞")

with col3:
    if st.button("💬 WhatsApp SOS"):
        webbrowser.open("https://wa.me/?text=🚨 I need help! Please check on me immediately.")
        st.toast("Opening WhatsApp...", icon="💬")
```

`st.columns(3)` splits the layout into three equal-width columns. Each button lives in its own column.

`webbrowser.open()` is Python's built-in way to open URLs. On desktop it opens the default browser. On mobile (if running locally), `tel:112` triggers the native phone dialer.

`st.toast()` shows a small non-blocking notification in the corner — good UX feedback without interrupting the flow.

The WhatsApp link uses the `wa.me` API with a pre-filled `text` query parameter. When opened, WhatsApp launches with the message already typed — the user just needs to pick a contact and hit send.

---

### Step 4 — The Keyword Detection Engine

This is the brain of the app. When a user types how they're feeling, the app scans the text for distress signals.

```python
DANGER_KEYWORDS = [
    "unsafe", "help", "scared", "danger", "follow", "threat", "attack",
    "harass", "afraid", "emergency", "hurt", "fear", "alone", "stalking",
    "chase", "violence", "abuse", "trapped", "kidnap", "assault"
]

def safety_response(text):
    text_lower = text.lower()
    if any(kw in text_lower for kw in DANGER_KEYWORDS):
        return "danger"
    return "safe"
```

The logic is intentionally simple:

- Convert input to lowercase to make matching case-insensitive
- Use Python's `any()` with a generator expression — this short-circuits on the first match, so it's efficient
- Return a status string that drives the UI response

**Why keyword matching and not AI/ML?**

A few reasons:

1. **Speed** — keyword matching is instantaneous. An ML model adds latency and complexity.
2. **Offline-friendliness** — no API calls, no model downloads.
3. **Predictability** — in a safety context, you want deterministic behavior. An ML model might confidently misclassify "I'm not scared" as dangerous.
4. **Good enough for v1** — the keyword list covers the most common distress expressions.

When danger is detected, the app shows a red alert card with actionable steps and automatically opens Google Maps:

```python
if status == "danger":
    st.markdown("""
    <div class="alert-danger">
        🚨 <strong>Potential Danger Detected</strong><br><br>
        • Call <strong>112</strong> immediately if you feel threatened<br>
        • Move to a crowded, well-lit public area<br>
        • Share your live location with a trusted contact<br>
        ...
    </div>
    """, unsafe_allow_html=True)
    webbrowser.open("https://www.google.com/maps")
```

The auto-open of Maps is intentional — in a panic, you want the app to do as much as possible automatically.

---

### Step 5 — The SOS Panic Button

The big red button at the bottom is designed for worst-case scenarios — when there's no time to think.

```python
if st.button("🆘  EMERGENCY SOS — PRESS FOR IMMEDIATE HELP"):
    webbrowser.open("https://www.google.com/maps")
    webbrowser.open("https://wa.me/?text=🚨 EMERGENCY! I need help immediately.")
    st.toast("🚨 SOS Activated!", icon="🚨")
```

One press does three things simultaneously:

- Opens Google Maps (for navigation and location sharing)
- Opens WhatsApp with a pre-filled emergency message
- Shows a toast notification confirming activation

The button is styled to be unmissable — full width, deep red gradient, large font, strong drop shadow. It should feel like a real panic button.

---

### Step 6 — Safety Tips Section

The tips section at the bottom serves a dual purpose: it fills the page with useful content when the user isn't in an emergency, and it reinforces safe habits passively.

```python
t1, t2, t3 = st.columns(3)

with t1:
    st.markdown("""
    <div class="tip-card">
        <div class="tip-icon">📱</div>
        <div class="tip-title">Stay Connected</div>
        Share your live location with a trusted friend when travelling alone at night.
    </div>
    """, unsafe_allow_html=True)
```

These are static HTML cards — no Python logic, just content. Keeping them simple means they load instantly and never break.

---

## UI Design Decisions

A few intentional choices worth calling out:

**Why dark theme?**
A dark UI is less conspicuous if someone is trying to use the app discreetly. A bright white screen draws attention. Dark purple is also calming — important when someone is already stressed.

**Why centered layout?**
Safety apps need to be usable under pressure. A centered, single-column layout means the user's eye always knows where to look. No sidebars, no distractions.

**Why color-coded buttons?**
Color is processed faster than text. Blue = navigation, amber = call, green = message, red = emergency. These map to intuitive associations most users already have.

**Why a text area instead of a text input?**
A text area invites more expressive input. Someone in distress might type a full sentence — "I think someone is following me home" — not just a single word. More text means better keyword matching.

---

## Deployment

### Streamlit Community Cloud (Recommended — Free)

1. Push your code to a public GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click "New app", select your repo, set the main file to `app.py`
4. Hit Deploy — your app gets a public URL in about 60 seconds

No server setup, no Docker, no CI/CD pipeline needed.

### Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Running on a Server (Optional)

If you want to self-host on a VPS:

```bash
# Run in background
nohup streamlit run app.py --server.port 8501 &

# Or use a process manager
pm2 start "streamlit run app.py" --name safety-app
```

Then point a reverse proxy (nginx/caddy) at port 8501.

---

## Limitations & Known Issues

**Keyword matching has false positives**
Typing "I'm not scared" will still trigger the danger alert because "scared" is in the keyword list. A negation-aware model would fix this.

**`webbrowser.open()` behavior varies**
On some systems or cloud deployments, `webbrowser.open()` may not work as expected because there's no display environment. This works best when running locally or on a user's machine.

**No persistent state**
There's no database or session storage. Trusted contacts, history, and settings don't persist between sessions. This is a v1 limitation.

**Not a replacement for real emergency services**
This app is a convenience tool, not a substitute for calling 112 or your local emergency number directly.

---

## What I'd Build Next

**Trusted Contacts Manager**
Let users save phone numbers. On SOS, automatically send SMS/WhatsApp to all saved contacts with a single tap.

**Live Location Sharing**
Use a Streamlit custom component to access the browser's Geolocation API and embed a shareable live-location link in the SOS message.

**Smarter Danger Detection**
Replace keyword matching with a fine-tuned text classifier. A small model like `distilbert-base-uncased` fine-tuned on safety-related text would dramatically reduce false positives.

```python
# Future implementation sketch
from transformers import pipeline
classifier = pipeline("text-classification", model="safety-classifier")
result = classifier(user_input)
if result[0]["label"] == "DANGER":
    trigger_sos()
```

**Twilio SMS Fallback**
If the user has no internet, fall back to SMS via Twilio's API. A pre-configured Twilio number could send location + alert to saved contacts automatically.

**Offline PWA**
Package the app as a Progressive Web App so it works without internet. Core features like the SOS button and saved contacts should work offline.

**Shake-to-SOS**
On mobile, detect a rapid shake gesture using the DeviceMotion API and trigger SOS automatically — no screen interaction needed.

---

## Final Thoughts

This project started as a simple idea — what's the minimum viable safety tool I can build in Python? The answer turned out to be surprisingly capable.

Streamlit made it possible to go from idea to working app in a single afternoon. The real work was in the UX decisions: what goes above the fold, how big the SOS button should be, what color means "safe" vs "danger". Those choices matter more than the code.

If you're building something similar, the most important thing is to keep it simple. In an emergency, complexity kills. Every extra tap, every extra decision is friction that could cost someone precious seconds.

The code is intentionally minimal. That's not laziness — it's a design principle.

---

_Built with Python 🐍 and Streamlit ⚡ — Emergency: 112_
