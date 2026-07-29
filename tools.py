"""LangChain tools the agent can call, backed by data.py and stats.py."""

from langchain_core.tools import tool

from data import (
    awards_to_cards,
    certificates_to_cards,
    experience_to_cards,
    get_profile,
    projects_to_cards,
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
    """Narrow down to cards whose title mentions `query`. Falls back to the full
    list if nothing matches, so a slightly-off query doesn't return an empty result."""
    if not query:
        return cards
    q = query.lower()
    matched = [c for c in cards if q in c["title"].lower()]
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
    """Get work experience and internship history: role, duration, location, and highlights.

    If the visitor asks about a SPECIFIC role/company by name, pass it as `query` so only
    the matching entry is returned instead of the whole list. Leave `query` unset for
    general "what's your work experience" questions.
    """
    cards = _filter_cards(experience_to_cards(), query)
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
def get_awards(query: str | None = None) -> tuple[str, list[dict]]:
    """Get awards and achievements: competitive exam ranks, awards, DSA problem counts, etc.

    If the visitor asks about a SPECIFIC award by name, pass it as `query` so only the
    matching one is returned instead of the whole list.
    """
    cards = _filter_cards(awards_to_cards(), query)
    return _describe_cards(cards), cards


@tool
def get_profile_info() -> dict:
    """Get personal profile info: name, age, contact details, current status, education, and skills."""
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
    get_certificates,
    get_awards,
    get_profile_info,
    get_leetcode_stats,
    get_github_stats,
]
