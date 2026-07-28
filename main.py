import json
import re

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    return ChatResponse(
        reply=f'This is a dummy response. You asked: "{payload.message}"'
    )


LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"
LEETCODE_HEADERS = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com",
    "User-Agent": "Mozilla/5.0",
}

LEETCODE_STATS_QUERY = """
query userStats($username: String!) {
  allQuestionsCount {
    difficulty
    count
  }
  matchedUser(username: $username) {
    username
    submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
      }
    }
    userCalendar {
      streak
      totalActiveDays
      submissionCalendar
    }
  }
}
"""


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


@app.get("/leetcode/stats", response_model=LeetCodeStats)
async def leetcode_stats(username: str = "achyutananda_sahoo"):
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            res = await client.post(
                LEETCODE_GRAPHQL_URL,
                headers=LEETCODE_HEADERS,
                json={
                    "query": LEETCODE_STATS_QUERY,
                    "variables": {"username": username},
                },
            )
            res.raise_for_status()
            payload = res.json()
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=502, detail="Failed to reach LeetCode"
            ) from exc

    matched_user = payload.get("data", {}).get("matchedUser")
    if matched_user is None:
        raise HTTPException(
            status_code=404, detail=f"LeetCode user '{username}' not found"
        )

    counts = {
        entry["difficulty"]: entry["count"]
        for entry in matched_user["submitStatsGlobal"]["acSubmissionNum"]
    }
    totals = {
        entry["difficulty"]: entry["count"]
        for entry in payload.get("data", {}).get("allQuestionsCount", [])
    }
    calendar_raw = matched_user["userCalendar"]["submissionCalendar"] or "{}"
    submission_calendar = json.loads(calendar_raw)

    return LeetCodeStats(
        username=matched_user["username"],
        totalSolved=counts.get("All", 0),
        easySolved=counts.get("Easy", 0),
        mediumSolved=counts.get("Medium", 0),
        hardSolved=counts.get("Hard", 0),
        easyTotal=totals.get("Easy", 0),
        mediumTotal=totals.get("Medium", 0),
        hardTotal=totals.get("Hard", 0),
        totalActiveDays=matched_user["userCalendar"]["totalActiveDays"],
        streak=matched_user["userCalendar"]["streak"],
        submissionCalendar=submission_calendar,
    )


GITHUB_HEADERS = {"User-Agent": "Mozilla/5.0"}

CONTRIB_DAY_RE = re.compile(r'<td\b[^>]*\bclass="ContributionCalendar-day"[^>]*>')
DATE_RE = re.compile(r'data-date="([\d-]+)"')
LEVEL_RE = re.compile(r'data-level="(\d+)"')


class GitHubStats(BaseModel):
    username: str
    publicRepos: int
    followers: int
    following: int
    totalStars: int
    contributionCalendar: dict[str, int]


@app.get("/github/stats", response_model=GitHubStats)
async def github_stats(username: str = "Sahoo-Achyutananda"):
    async with httpx.AsyncClient(timeout=10, headers=GITHUB_HEADERS) as client:
        try:
            profile_res = await client.get(f"https://api.github.com/users/{username}")
            repos_res = await client.get(
                f"https://api.github.com/users/{username}/repos",
                params={"per_page": 100},
            )
            contrib_res = await client.get(
                f"https://github.com/users/{username}/contributions"
            )
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=502, detail="Failed to reach GitHub"
            ) from exc

    if profile_res.status_code == 404:
        raise HTTPException(
            status_code=404, detail=f"GitHub user '{username}' not found"
        )
    if not profile_res.is_success or not repos_res.is_success or not contrib_res.is_success:
        raise HTTPException(status_code=502, detail="Failed to reach GitHub")

    profile = profile_res.json()
    repos = repos_res.json()
    total_stars = sum(
        repo.get("stargazers_count", 0) for repo in repos if isinstance(repo, dict)
    )

    calendar: dict[str, int] = {}
    for td in CONTRIB_DAY_RE.findall(contrib_res.text):
        date_match = DATE_RE.search(td)
        level_match = LEVEL_RE.search(td)
        if date_match and level_match:
            calendar[date_match.group(1)] = int(level_match.group(1))

    return GitHubStats(
        username=profile.get("login", username),
        publicRepos=profile.get("public_repos", 0),
        followers=profile.get("followers", 0),
        following=profile.get("following", 0),
        totalStars=total_stars,
        contributionCalendar=calendar,
    )
