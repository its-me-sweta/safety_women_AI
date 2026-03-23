# Tech Stack

## Framework

- **Streamlit** — Python-to-web UI framework, no frontend code needed

## Language

- Python 3.8+

## Dependencies

- `streamlit` (only dependency, see `requirements.txt`)

## Styling

- Custom CSS injected via `st.markdown(..., unsafe_allow_html=True)`
- Glassmorphism design with `rgba` backgrounds and `backdrop-filter`
- Per-button styling via CSS `nth-child` selectors on Streamlit's `data-testid` attributes

## External Integrations

- `webbrowser` (stdlib) — opens URLs, `tel:` links, WhatsApp `wa.me` links
- Google Maps: `https://www.google.com/maps`
- WhatsApp SOS: `https://wa.me/?text=<pre-filled message>`
- Emergency call: `tel:112`

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (opens at http://localhost:8501)
streamlit run app.py

# Run in background on a server
nohup streamlit run app.py --server.port 8501 &
```

## Deployment

- Streamlit Community Cloud (recommended): connect GitHub repo at share.streamlit.io, set main file to `app.py`
- Self-hosted: run behind nginx/caddy reverse proxy on port 8501
