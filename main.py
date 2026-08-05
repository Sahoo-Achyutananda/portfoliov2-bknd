from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import ToolMessage
from pydantic import BaseModel

load_dotenv()

from agent import agent
from mailer import is_rate_limited, send_notification_email
from stats import StatsNotFoundError, StatsUnavailableError, fetch_github_stats, fetch_leetcode_stats

CARD_TOOL_NAMES = {
    "get_projects",
    "get_experience",
    "get_education",
    "get_certificates",
    "get_paintings",
    "get_resume",
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://iamsahoo.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatCard(BaseModel):
    title: str
    subtitle: str | None = None
    description: str | None = None
    link: str | None = None
    linkLabel: str | None = None
    image: str | None = None


class ChatResponse(BaseModel):
    reply: str
    cards: list[ChatCard] | None = None
    showQuickActions: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


def _extract_text(content) -> str:
    """Gemini sometimes returns message.content as a list of content blocks
    instead of a plain string; pull just the text parts out either way."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return str(content)


@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    result = await agent.ainvoke({"messages": [{"role": "user", "content": payload.message}]})
    # print("-------------",result)
    messages = result["messages"]

    reply = _extract_text(messages[-1].content)

    cards = None
    for message in reversed(messages):
        if isinstance(message, ToolMessage) and message.name in CARD_TOOL_NAMES:
            cards = message.artifact
            break

    # If the agent answered without looking anything up, it's almost certainly an
    # off-topic deflection or a generic/corporate-style answer (per its system prompt,
    # real questions about me always go through a tool) - surface quick-action buttons
    # so the visitor can tap their way to actual content instead of typing again.
    used_tools = any(isinstance(message, ToolMessage) for message in messages)

    return ChatResponse(reply=reply, cards=cards, showQuickActions=not used_tools)


class MessageRequest(BaseModel):
    message: str


class MessageResponse(BaseModel):
    ok: bool


@app.post("/message", response_model=MessageResponse)
def send_message(payload: MessageRequest, request: Request):
    text = payload.message.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Message is empty")
    if len(text) > 2000:
        raise HTTPException(status_code=400, detail="Message is too long")

    client_ip = request.client.host if request.client else "unknown"
    if is_rate_limited(client_ip):
        raise HTTPException(status_code=429, detail="Too many messages sent, try again later")

    try:
        send_notification_email(text)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Failed to send message") from exc

    return MessageResponse(ok=True)


class ContestHistoryEntry(BaseModel):
    title: str
    rating: float
    ranking: int
    problemsSolved: int
    totalProblems: int
    trendDirection: str


class LeetCodeStats(BaseModel):
    username: str
    totalSolved: int
    easySolved: int
    mediumSolved: int
    hardSolved: int
    easyTotal: int
    mediumTotal: int
    hardTotal: int
    totalActiveDays: int
    streak: int
    submissionCalendar: dict[str, int]
    contestRating: float | None
    contestAttended: int
    contestGlobalRanking: int | None
    contestTopPercentage: float | None
    contestHistory: list[ContestHistoryEntry]


@app.get("/leetcode/stats", response_model=LeetCodeStats)
async def leetcode_stats(username: str = "achyutananda_sahoo"):
    try:
        data = await fetch_leetcode_stats(username)
    except StatsNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except StatsUnavailableError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return LeetCodeStats(**data)


class GitHubStats(BaseModel):
    username: str
    publicRepos: int
    followers: int
    following: int
    totalStars: int
    contributionCalendar: dict[str, int]


@app.get("/github/stats", response_model=GitHubStats)
async def github_stats(username: str = "Sahoo-Achyutananda"):
    try:
        data = await fetch_github_stats(username)
    except StatsNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except StatsUnavailableError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return GitHubStats(**data)
