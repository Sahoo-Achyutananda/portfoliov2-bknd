"""LangChain tools the agent can call, backed by data.py and stats.py."""

from langchain_core.tools import tool

from data import (
    certificates_to_cards,
    education_to_cards,
    experience_to_cards,
    get_profile,
    paintings_to_cards,
    projects_to_cards,
    resume_to_cards,
)
from stats import (
    StatsNotFoundError,
    StatsUnavailableError,
    fetch_github_stats,
    fetch_leetcode_stats,
)


def _describe_cards(cards: list[dict]) -> str:
    """Full per-item detail for the LLM to reason over (tech stack, description, links) —
    not just titles, so it can actually answer specific follow-up questions."""
    lines = []
    for c in cards:
        parts = [c["title"]]
        if c.get("subtitle"):
            parts.append(f"({c['subtitle']})")
        line = " ".join(parts)
        if c.get("description"):
            line += f": {c['description']}"
        if c.get("link"):
            line += f" [{c.get('linkLabel') or 'link'}: {c['link']}]"
        lines.append(f"- {line}")
    return "\n".join(lines)


def _filter_cards(cards: list[dict], query: str | None) -> list[dict]:
    """Narrow down to cards matching `query`, checked against title, subtitle, and
    description (not just title) so things like a category tucked into the subtitle —
    e.g. "Freelance" — are actually searchable. Falls back to the full list if nothing
    matches, so a slightly-off query doesn't return an empty result."""
    if not query:
        return cards
    q = query.lower()

    def matches(c: dict) -> bool:
        haystack = " ".join(
            str(c.get(field) or "") for field in ("title", "subtitle", "description")
        ).lower()
        return q in haystack

    matched = [c for c in cards if matches(c)]
    return matched or cards


@tool(response_format="content_and_artifact")
def get_projects(query: str | None = None) -> tuple[str, list[dict]]:
    """Get software projects: title, tech stack, description, and links.

    If the visitor asks about a SPECIFIC project by name (e.g. "tell me about mygit"),
    pass that name as `query` so only the matching project is returned instead of the
    whole list. Leave `query` unset for general "what projects have you built" questions.
    """
    cards = _filter_cards(projects_to_cards(), query)
    return _describe_cards(cards), cards


@tool(response_format="content_and_artifact")
def get_experience(query: str | None = None) -> tuple[str, list[dict]]:
    """Get work experience and internship history: category (Internships/Freelance), role,
    duration, location, and highlights.

    If the visitor asks about a SPECIFIC role/company (e.g. "Wells Fargo") or a CATEGORY
    of work (e.g. "freelance work", "graphic design", "internships"), pass that as `query`
    so only the matching entries are returned instead of the whole list. Leave `query`
    unset for general "what's your work experience" questions.
    """
    cards = _filter_cards(experience_to_cards(), query)
    return _describe_cards(cards), cards


@tool(response_format="content_and_artifact")
def get_education() -> tuple[str, list[dict]]:
    """Get education history: degree, institution, period, and honors for each."""
    cards = education_to_cards()
    return _describe_cards(cards), cards


@tool(response_format="content_and_artifact")
def get_certificates(query: str | None = None) -> tuple[str, list[dict]]:
    """Get certificates and certifications earned.

    If the visitor asks about a SPECIFIC certificate by name, pass it as `query` so only
    the matching one is returned instead of the whole list.
    """
    cards = _filter_cards(certificates_to_cards(), query)
    return _describe_cards(cards), cards


@tool(response_format="content_and_artifact")
def get_paintings(query: str | None = None) -> tuple[str, list[dict]]:
    """Get paintings - painting is one of my hobbies alongside graphic design.

    Use this whenever a visitor asks about hobbies, art, painting, or what I do outside of
    software (in addition to mentioning graphic design from get_profile_info). If asked about
    a SPECIFIC painting by name, pass it as `query` so only the matching one is returned.
    """
    cards = _filter_cards(paintings_to_cards(), query)
    return _describe_cards(cards), cards


@tool(response_format="content_and_artifact")
def get_resume() -> tuple[str, list[dict]]:
    """Get a link to view or download the resume (Resume.pdf).

    Use this whenever the visitor asks for a resume, CV, or asks to download/see one.
    """
    cards = resume_to_cards()
    return _describe_cards(cards), cards


@tool
def get_profile_info() -> dict:
    """Get personal profile info: name, age, contact details, current status, education, skills,
    and social/coding profiles (GitHub, LinkedIn, LeetCode, GeeksforGeeks, email), plus hobbies.

    Use this whenever a visitor asks for a specific social or coding profile link (e.g. "what's
    your GitHub", "do you have LeetCode", "how do I add you on LinkedIn"), or asks about hobbies
    or interests outside of work (mention painting and graphic design, and call get_paintings too
    if they want to actually see the paintings).
    """
    return get_profile()


@tool
async def get_leetcode_stats() -> dict:
    """Get LeetCode stats: total problems solved, easy/medium/hard breakdown, and submission activity."""
    try:
        return await fetch_leetcode_stats()
    except (StatsNotFoundError, StatsUnavailableError) as exc:
        return {"error": str(exc)}


@tool
async def get_github_stats() -> dict:
    """Get GitHub stats: public repo count, followers, total stars, and contribution activity."""
    try:
        return await fetch_github_stats()
    except (StatsNotFoundError, StatsUnavailableError) as exc:
        return {"error": str(exc)}


TOOLS = [
    get_projects,
    get_experience,
    get_education,
    get_certificates,
    get_paintings,
    get_resume,
    get_profile_info,
    get_leetcode_stats,
    get_github_stats,
]
