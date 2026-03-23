# Building a Women Safety AI App with Flask & Vanilla JS

> A zero-friction safety tool that anyone can open in a browser — no login, no app install, no waiting.

---

## Why I Built This

Every woman has had that moment — walking to the car at night, feeling like someone's following her, being in an unfamiliar place and not knowing who to call. Most safety apps are buried behind sign-ups, paywalls, or require a smartphone with a specific OS.

I wanted to build something different. Open a browser, tap a button, get help. That's it.

The result is Women Safety AI — a lightweight web app with a Flask backend and a plain HTML/CSS/JS frontend, deployed on AWS Amplify and Render.

---

## What It Does

At its core, the app does one thing really well: **send an SOS with a single tap**.

- User hits the SOS button
- Frontend sends a POST request to the Flask backend
- Backend checks the time — if it's after 10 PM, it flags the message as high risk
- Response is shown instantly on screen

Simple. Fast. No friction.

---

## Tech Stack

| Layer    | Technology                  |
| -------- | --------------------------- |
| Frontend | HTML, CSS, JavaScript       |
| Backend  | Python + Flask              |
| CORS     | flask-cors                  |
| Server   | Gunicorn                    |
| Hosting  | AWS Amplify + Render (free) |

No React. No Node. No build pipeline. Just files that work.

---

## The Backend

The entire backend is ~25 lines of Python.

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

def analyze_risk():
    hour = datetime.datetime.now().hour
    return hour > 22

@app.route('/sos', methods=['POST'])
def sos():
    data = request.json
    message = data.get("message", "Help needed!")
    if analyze_risk():
        message = "🚨 HIGH RISK! " + message
    return jsonify({"status": "SOS sent", "message": message})
```

The `analyze_risk()` function is intentionally simple — time-based risk detection. After 10 PM, any SOS is flagged as high risk. No ML model, no API calls, just a clock check. Fast and reliable.

CORS is enabled so the frontend hosted on Amplify can talk to the backend on Render without browser security errors.

---

## The Frontend

Three files. That's the whole frontend.

**index.html** — the UI

```html
<h1>🚨 Women Safety AI</h1>
<button onclick="sendSOS()">Send SOS</button>
<p id="status"></p>
```

**app.js** — the logic

```js
function sendSOS() {
  fetch('https://your-backend.onrender.com/sos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: 'Help me!' }),
  })
    .then((res) => res.json())
    .then((data) => {
      document.getElementById('status').innerText = data.status;
    });
}
```

**style.css** — the look

```css
body {
  text-align: center;
  background: #ffe6f0;
  font-family: Arial;
}
button {
  padding: 15px;
  background: #e91e63;
  color: white;
  border-radius: 10px;
}
```

Pink background, red button, centered layout. Instantly recognizable as a safety tool.

---

## Deployment

### Frontend on AWS Amplify

Amplify is perfect for static sites. Connect your GitHub repo, set the build spec to serve the `frontend` folder, and you get a public HTTPS URL in under 2 minutes.

The key build spec that makes it work:

```yaml
version: 1
frontend:
  phases:
    build:
      commands:
        - echo "Static site"
  artifacts:
    baseDirectory: frontend
    files:
      - '**/*'
```

No npm, no webpack, no nonsense.

### Backend on Render

Render's free tier is great for Flask apps. Point it at the `backend` folder, set the start command to `gunicorn app:app`, and it handles the rest.

---

## What I'd Build Next

- **Trusted contacts** — save phone numbers, auto-send WhatsApp on SOS
- **Live location** — embed a shareable Google Maps link in the SOS message
- **Smarter risk detection** — replace the time check with a text classifier
- **Offline mode** — PWA so it works without internet

---

## Final Thoughts

The best safety tool is the one you actually use. That means it has to be fast, obvious, and always available. No login screens. No loading spinners. No confusion.

This app is intentionally minimal. In an emergency, every second counts — and every extra tap is a second wasted.

---

_Built with Python 🐍 Flask ⚡ and deployed on AWS Amplify + Render_
