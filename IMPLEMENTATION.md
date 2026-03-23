# Women Safety Assistant — Implementation

## Overview

A lightweight, single-page safety companion web app built with **Python** and **Streamlit**. No backend server, no database — just a fast, deployable UI that puts emergency tools one tap away.

---

## Tech Stack

| Layer                 | Technology                                           |
| --------------------- | ---------------------------------------------------- |
| Framework             | [Streamlit](https://streamlit.io)                    |
| Language              | Python 3.8+                                          |
| Styling               | Custom CSS via `st.markdown(unsafe_allow_html=True)` |
| External Actions      | Python `webbrowser` module                           |
| Dependency Management | `requirements.txt`                                   |

---

## Project Structure

```
women-safety-app/
├── app.py            # Main application
└── requirements.txt  # Python dependencies (streamlit)
```

---

## Core Modules

### 1. Page Configuration

```python
st.set_page_config(
    page_title="Women Safety Assistant",
    page_icon="🛡️",
    layout="centered"
)
```

Sets the browser tab title, favicon, and constrains the layout to a readable centered column.

---

### 2. Custom Styling

All visual styling is injected as a raw CSS block using:

```python
st.markdown("""<style> ... </style>""", unsafe_allow_html=True)
```

Key design decisions:

- **Dark purple gradient background** — calming yet serious tone
- **Glass-morphism cards** — `rgba` backgrounds with subtle borders
- **Color-coded buttons** — blue (Maps), amber (Call), green (WhatsApp), red (SOS)
- **Alert boxes** — red left-border for danger, green for safe
- **Inter font** loaded from Google Fonts for clean typography

---

### 3. Quick Action Buttons

Three side-by-side buttons rendered using Streamlit columns:

```python
col1, col2, col3 = st.columns(3)
```

| Button          | Action                                       |
| --------------- | -------------------------------------------- |
| 📍 Open Maps    | Opens `https://www.google.com/maps`          |
| 📞 Call 112     | Opens `tel:112` (triggers native dialer)     |
| 💬 WhatsApp SOS | Opens WhatsApp with a pre-filled SOS message |

Each button fires `webbrowser.open()` and shows a `st.toast()` notification on click.

---

### 4. Keyword-Based Danger Detection

The check-in section accepts free-text input and scans it against a keyword list:

```python
DANGER_KEYWORDS = [
    "unsafe", "help", "scared", "danger", "follow", "threat", "attack",
    "harass", "afraid", "emergency", "hurt", "fear", "alone", "stalking",
    "chase", "violence", "abuse", "trapped", "kidnap", "assault"
]

def safety_response(text):
    if any(kw in text.lower() for kw in DANGER_KEYWORDS):
        return "danger"
    return "safe"
```

- Match is case-insensitive substring search
- On danger detection: shows a red alert card + auto-opens Google Maps
- On safe detection: shows a green reassurance card

> **Limitation:** This is rule-based, not ML-based. It can produce false positives/negatives. A future improvement would be to integrate a sentiment/intent classification model.

---

### 5. Emergency SOS Button

A full-width panic button at the bottom of the page:

```python
if st.button("🆘 EMERGENCY SOS — PRESS FOR IMMEDIATE HELP"):
    webbrowser.open("https://www.google.com/maps")
    webbrowser.open("https://wa.me/?text=🚨 EMERGENCY! ...")
```

Simultaneously opens Maps and WhatsApp with a pre-filled emergency message, giving the user two channels to get help instantly.

---

### 6. Safety Tips Section

Three static tip cards rendered as raw HTML inside `st.columns(3)`. No logic — purely informational UI to reinforce safe habits.

---

## Running the App

```bash
pip install -r requirements.txt
streamlit run app.py
```

App runs at `http://localhost:8501` by default.

---

## Deployment

Can be deployed for free on [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Push the repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect the repo and set `app.py` as the entry point
4. Deploy — no server config needed

---

## Potential Improvements

- Integrate a real ML model (e.g. HuggingFace sentiment classifier) for smarter detection
- Add a trusted contacts manager with stored phone numbers
- Use browser Geolocation API via a custom Streamlit component for live location sharing
- Add SMS fallback via Twilio when internet is unavailable
- Offline PWA support for low-connectivity scenarios
