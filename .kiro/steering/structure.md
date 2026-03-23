# Project Structure

Intentionally minimal — the entire app lives in two files.

```
/
├── app.py            # All application logic, UI, and styling
├── requirements.txt  # Single dependency: streamlit
└── IMPLEMENTATION.md # Developer notes and architecture deep-dive
```

## Conventions

- All UI, logic, and CSS lives in `app.py` — no separate modules or folders
- No build step, no `src/` directory, no config files
- CSS is written inline inside `st.markdown()` blocks at the top of `app.py`
- Constants (e.g., `DANGER_KEYWORDS`) are defined at module level in `app.py`
- Helper functions (e.g., `safety_response()`) are defined before the UI code that uses them

## Key Patterns

- Use `st.columns()` for side-by-side button layouts
- Use `st.markdown(..., unsafe_allow_html=True)` for custom HTML/CSS cards and alerts
- Use `st.toast()` for non-blocking feedback after button actions
- Use `webbrowser.open()` for all external URL/dialer actions
- Alert states are driven by string returns (`"danger"` / `"safe"`) from `safety_response()`

## Adding Features

Keep the flat structure — add new sections to `app.py` with a `st.markdown("---")` divider and a clear `#### Section Title` heading. Avoid splitting into multiple files unless the app grows significantly beyond its current scope.
