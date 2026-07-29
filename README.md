# portfoliov2-bknd

Backend for the portfolio site. FastAPI.

Routes so far: `/health`, `/chat` (currently a dummy echo — see Implementation Order below),
`/leetcode/stats`, `/github/stats`.

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

## Implementation Order

Plan for replacing the dummy `/chat` response with a real LangGraph + Anthropic agent that can
answer visitor questions using this portfolio's own data (projects, experience, LeetCode/GitHub
stats) as tools. First time using LangGraph — so this starts with the prebuilt agent before
hand-building a graph.

1. **Install the agent stack**
   ```bash
   pip install langgraph langchain-anthropic langchain-core
   ```
   Add the same three lines to `requirements.txt` so a fresh `pip install -r requirements.txt`
   picks them up.

2. **Load the API key at startup**
   `python-dotenv` is already a dependency but nothing calls it yet. Add
   `from dotenv import load_dotenv` + `load_dotenv()` near the top of `main.py`, before anything
   reads `ANTHROPIC_API_KEY` from the environment. Confirm your local `.env` (copied from
   `.env.example`) actually has a real key in it.

3. **Mirror the portfolio data as Python tools**
   The frontend's `projects.ts` / `experience.ts` content needs a Python-side equivalent so the
   agent can read it — duplicate the static data (title/description/links for projects,
   duration/highlights for experience) as plain Python constants in a new `tools.py`. Wrap each
   as a LangChain tool with `@tool`, e.g. `get_projects()`, `get_experience()`.

4. **Turn the existing stats fetchers into tools too**
   `leetcode_stats()` and `github_stats()` in `main.py` already do the real work — pull their
   core logic into plain async functions in `tools.py` (not FastAPI route handlers) and wrap
   *those* with `@tool` as `get_leetcode_stats()` / `get_github_stats()`. The existing
   `/leetcode/stats` and `/github/stats` routes can just call the same underlying functions, so
   there's one source of truth instead of the agent hitting its own HTTP API.

5. **Build the first agent with the prebuilt ReAct constructor**
   Don't hand-build a graph yet. Use `langgraph.prebuilt.create_react_agent`, bound to
   `ChatAnthropic(model="claude-...")` and the tool list from steps 3–4. This is already a real
   LangGraph `StateGraph` under the hood — it's the standard on-ramp before writing custom nodes.

6. **Test the agent standalone, outside FastAPI**
   A throwaway script (`python -c "..."` or a `scratch.py`) that imports the agent and calls
   `.invoke({"messages": [...]})` directly. Get tool-calling working and verify the answers
   before wiring it into a route — much faster to debug than through the browser.

7. **Wire the agent into `POST /chat`**
   Replace the dummy `f'This is a dummy response...'` line with a call into the agent, keeping
   the existing `ChatRequest`/`ChatResponse` models unchanged so the frontend needs zero changes.

8. **Test end-to-end from the actual chat window**
   Run both servers, open the site, ask it something that requires a tool call (e.g. "what are
   your LeetCode stats?") and confirm the round trip works with real data, not a hallucinated
   guess.

9. **(Stretch) Add multi-turn memory**
   Right now the frontend sends only the latest message per request — no conversation history.
   Add a LangGraph checkpointer (e.g. `MemorySaver`) keyed by a session id, or have the frontend
   send the full message history and pass it into the agent's message list. Needed for
   "what did I just ask you" type follow-ups to work.

10. **(Stretch) Replace the prebuilt with a hand-built `StateGraph`**
    Once the ReAct agent works, rebuild it as an explicit graph with real nodes/edges — this is
    where LangGraph concepts (state, conditional routing, e.g. a router node choosing between
    "needs a tool" vs "just answer") actually get learned, rather than hidden behind the
    prebuilt helper.
