# Women Safety AI — Implementation Guide

## Project Structure

```
women_safety_AI/
├── amplify.yml           # Amplify build config (root level)
├── backend/
│   ├── app.py            # Flask API server
│   └── requirements.txt  # Python dependencies
└── frontend/
    ├── index.html        # Main UI
    ├── style.css         # Styling
    ├── app.js            # SOS fetch logic
    └── amplify.yml       # (unused, root one takes precedence)
```

---

## Tech Stack

| Layer    | Technology                               |
| -------- | ---------------------------------------- |
| Frontend | HTML, CSS, JS                            |
| Backend  | Python, Flask                            |
| CORS     | flask-cors                               |
| Server   | Gunicorn                                 |
| Hosting  | AWS Amplify (frontend), Render (backend) |

---

## Backend

### `backend/app.py`

Flask API with a single `/sos` POST endpoint.

```python
@app.route('/sos', methods=['POST'])
def sos():
    data = request.json
    message = data.get("message", "Help needed!")
    if analyze_risk():
        message = "🚨 HIGH RISK! " + message
    return jsonify({"status": "SOS sent", "message": message})
```

- `analyze_risk()` checks if current hour > 22 (night-time = high risk)
- CORS enabled via `flask_cors` so the frontend can call the API

### `backend/requirements.txt`

```
flask
flask-cors
gunicorn
```

### Run locally

```bash
pip install -r backend/requirements.txt
python3 backend/app.py
# API running at http://localhost:5001
```

### Test the endpoint

```bash
curl -X POST http://localhost:5001/sos \
  -H "Content-Type: application/json" \
  -d '{"message": "Help me!"}'
```

Expected response:

```json
{ "status": "SOS sent", "message": "Help me!" }
```

---

## Frontend

### `frontend/index.html`

Simple HTML page with an SOS button that calls the backend API.

### `frontend/app.js`

```js
function sendSOS() {
  fetch('https://your-app.onrender.com/sos', {
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

Replace `your-app.onrender.com` with your actual Render backend URL after deployment.

### Run locally

```bash
open frontend/index.html
```

---

## Deployment

### Frontend → AWS Amplify

1. Push repo to GitHub
2. Go to [console.aws.amazon.com/amplify](https://console.aws.amazon.com/amplify)
3. New app → Host web app → connect GitHub repo
4. In Build settings, set the build spec to:

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
  cache:
    paths: []
```

5. Deploy — app gets a public URL like `https://main.xxxxxx.amplifyapp.com`

### Backend → Render

1. Go to [render.com](https://render.com) → New → Web Service
2. Connect GitHub repo, configure:
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
3. Deploy — copy the public URL
4. Update `frontend/app.js` with the real Render URL
5. Redeploy frontend on Amplify

---

## Known Issues

- `webbrowser.open()` removed — app now uses fetch API instead
- `your-app.onrender.com` in `app.js` must be replaced with real URL before production
- Night-time risk detection is time-based only (hour > 22), no ML model
