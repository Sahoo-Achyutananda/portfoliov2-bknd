# portfoliov2-bknd

Backend for the portfolio site. FastAPI.

Currently just the base scaffold: a single `/health` route. No LLM/agent logic yet.

## Run

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # macOS/Linux
pip install -r requirements.txt
cp .env.example .env       # then fill in ANTHROPIC_API_KEY when needed
uvicorn main:app --reload
```

Serves at http://localhost:8000 — check http://localhost:8000/health

CORS is configured to accept requests from the Vite dev server at http://localhost:5173.
