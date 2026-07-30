"""Live stats fetchers for LeetCode and GitHub.

Plain async functions (not FastAPI route handlers) so both the /leetcode/stats
and /github/stats routes in main.py and the agent's tools in tools.py can share
one implementation.
"""

import json
import re

import httpx


class StatsUnavailableError(Exception):
    """The upstream provider (LeetCode/GitHub) could not be reached."""


class StatsNotFoundError(Exception):
    """The requested username was not found."""


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
  userContestRanking(username: $username) {
    attendedContestsCount
    rating
    globalRanking
    totalParticipants
    topPercentage
  }
  userContestRankingHistory(username: $username) {
    attended
    trendDirection
    problemsSolved
    totalProblems
    rating
    ranking
    contest {
      title
      startTime
    }
  }
}
"""


async def fetch_leetcode_stats(username: str = "achyutananda_sahoo") -> dict:
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
            raise StatsUnavailableError("Failed to reach LeetCode") from exc

    matched_user = payload.get("data", {}).get("matchedUser")
    if matched_user is None:
        raise StatsNotFoundError(f"LeetCode user '{username}' not found")

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

    contest_ranking = payload.get("data", {}).get("userContestRanking") or {}
    contest_history_raw = payload.get("data", {}).get("userContestRankingHistory") or []
    attended = [c for c in contest_history_raw if c.get("attended")]
    recent_contests = [
        {
            "title": c["contest"]["title"],
            "rating": round(c["rating"], 1),
            "ranking": c["ranking"],
            "problemsSolved": c["problemsSolved"],
            "totalProblems": c["totalProblems"],
            "trendDirection": c["trendDirection"],
        }
        for c in list(reversed(attended))[:10]
    ]

    return {
        "username": matched_user["username"],
        "totalSolved": counts.get("All", 0),
        "easySolved": counts.get("Easy", 0),
        "mediumSolved": counts.get("Medium", 0),
        "hardSolved": counts.get("Hard", 0),
        "easyTotal": totals.get("Easy", 0),
        "mediumTotal": totals.get("Medium", 0),
        "hardTotal": totals.get("Hard", 0),
        "totalActiveDays": matched_user["userCalendar"]["totalActiveDays"],
        "streak": matched_user["userCalendar"]["streak"],
        "submissionCalendar": submission_calendar,
        "contestRating": round(contest_ranking["rating"], 1)
        if contest_ranking.get("rating") is not None
        else None,
        "contestAttended": contest_ranking.get("attendedContestsCount", 0),
        "contestGlobalRanking": contest_ranking.get("globalRanking"),
        "contestTopPercentage": contest_ranking.get("topPercentage"),
        "contestHistory": recent_contests,
    }


GITHUB_HEADERS = {"User-Agent": "Mozilla/5.0"}

CONTRIB_DAY_RE = re.compile(r'<td\b[^>]*\bclass="ContributionCalendar-day"[^>]*>')
DATE_RE = re.compile(r'data-date="([\d-]+)"')
LEVEL_RE = re.compile(r'data-level="(\d+)"')


async def fetch_github_stats(username: str = "Sahoo-Achyutananda") -> dict:
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
            raise StatsUnavailableError("Failed to reach GitHub") from exc

    if profile_res.status_code == 404:
        raise StatsNotFoundError(f"GitHub user '{username}' not found")
    if not profile_res.is_success or not repos_res.is_success or not contrib_res.is_success:
        raise StatsUnavailableError("Failed to reach GitHub")

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

    return {
        "username": profile.get("login", username),
        "publicRepos": profile.get("public_repos", 0),
        "followers": profile.get("followers", 0),
        "following": profile.get("following", 0),
        "totalStars": total_stars,
        "contributionCalendar": calendar,
    }
