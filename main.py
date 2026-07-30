from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import ToolMessage
from pydantic import BaseModel

load_dotenv()

from agent import agent
from stats import StatsNotFoundError, StatsUnavailableError, fetch_github_stats, fetch_leetcode_stats

CARD_TOOL_NAMES = {"get_projects", "get_experience", "get_certificates", "get_awards"}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
    print("-------------",result)
    messages = result["messages"]

    reply = _extract_text(messages[-1].content)

    cards = None
    for message in reversed(messages):
        if isinstance(message, ToolMessage) and message.name in CARD_TOOL_NAMES:
            cards = message.artifact
            break

    return ChatResponse(reply=reply, cards=cards)


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
