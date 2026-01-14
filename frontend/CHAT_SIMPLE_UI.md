# Simple Chat UI (HTML/CSS/JS)

This is a minimal static UI that queries the FastAPI search endpoint.

- Page: `public/chat.html`
- Default API base: `http://localhost:8000`

## Run locally

```bash
cd frontend
npm install
npm run dev
```

Then open: http://localhost:5173/chat.html

Notes:
- Ensure the backend is running and accessible (FastAPI default port 8000).
- If using a different host/port, change the API base in the header of the page.
- When serving frontend and backend from different origins, enable CORS in the backend.
