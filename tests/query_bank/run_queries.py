"""Batch-runs every query in queries.json through the real agent and writes
input/output pairs to results.json for manual review.

This is NOT an automated pass/fail suite (see ../test_agent_behavior.py for
that) - it's for eyeballing how the agent actually responds across a wide
range of prompt types, sends ~100 real Gemini calls, and takes a few minutes.

Usage (from portfoliov2-bknd/):
    python tests/query_bank/run_queries.py
    python tests/query_bank/run_queries.py --limit 5     # smoke test a few first
    python tests/query_bank/run_queries.py --score       # also score each response (doubles the calls)
"""

import argparse
import json
import sys
import time
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from dotenv import load_dotenv

load_dotenv(BACKEND_ROOT / ".env")

from agent import agent  # noqa: E402 (must come after load_dotenv)

QUERIES_PATH = Path(__file__).resolve().parent / "queries.json"
RESULTS_PATH = Path(__file__).resolve().parent / "results.json"

# Distills agent.py's SYSTEM_PROMPT into one rubric that applies across every
# category in queries.json, so every response gets scored on the same scale
# instead of needing bespoke criteria per category.
SCORE_CRITERIA = (
    "Judge whether this is a good response from Achyutananda Sahoo's personal "
    "portfolio chatbot, which always speaks AS Achyutananda in the first person. "
    "Score highly if: (1) for questions about his real background (projects, "
    "experience, education, skills, awards, etc.), the response is specific, "
    "accurate, and clearly grounded in real information, not vague or fabricated; "
    "(2) for off-topic questions unrelated to him, it deflects with a short "
    "self-aware joke and steers back to his portfolio, without ever answering the "
    "off-topic question straight or admitting to being an AI/chatbot; (3) for "
    "personal questions he has no data for, it honestly says so and points toward "
    "direct contact info instead of making something up; (4) it always stays in "
    "first person and in character. Score low if it hallucinates details, breaks "
    "character, says 'as an AI', answers off-topic trivia straight, or is "
    "evasive/unhelpful for a question it should be able to answer."
)


def _extract_text(content) -> str:
    """Mirrors main.py's _extract_text - Gemini sometimes returns content as
    a list of blocks instead of a plain string."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return str(content)


def ask_agent(message: str) -> str:
    result = agent.invoke({"messages": [{"role": "user", "content": message}]})
    return _extract_text(result["messages"][-1].content)


def build_scorer():
    """Lazy imports - deepeval isn't needed at all unless --score is passed."""
    from deepeval.metrics import GEval
    from deepeval.models import GeminiModel
    from deepeval.test_case import LLMTestCaseParams

    judge_model = GeminiModel(model="gemini-2.5-flash")
    metric = GEval(
        name="Response Quality",
        criteria=SCORE_CRITERIA,
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        model=judge_model,
        threshold=0.5,
    )

    def score(query: str, response: str) -> tuple[float, str]:
        from deepeval.test_case import LLMTestCase

        test_case = LLMTestCase(input=query, actual_output=response)
        metric.measure(test_case)
        return metric.score, metric.reason

    return score


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--limit", type=int, default=None, help="Only run the first N queries (smoke test)"
    )
    parser.add_argument(
        "--score",
        action="store_true",
        help="Also score each response with a Gemini judge (doubles the API calls/time)",
    )
    args = parser.parse_args()

    queries = json.loads(QUERIES_PATH.read_text(encoding="utf-8"))
    if args.limit:
        queries = queries[: args.limit]

    scorer = build_scorer() if args.score else None

    results = []
    for i, item in enumerate(queries, start=1):
        print(f"[{i}/{len(queries)}] ({item['category']}) {item['query']}")
        start = time.monotonic()
        response = None
        error = None
        score = None
        reason = None
        try:
            response = ask_agent(item["query"])
            if scorer:
                score, reason = scorer(item["query"], response)
                print(f"  score: {score:.2f}")
        except Exception as exc:  # batch script: record the failure, keep going
            error = str(exc)
            print(f"  ! error: {error}")
        elapsed = round(time.monotonic() - start, 2)

        results.append(
            {
                "id": item["id"],
                "category": item["category"],
                "query": item["query"],
                "response": response,
                "score": score,
                "reason": reason,
                "error": error,
                "elapsedSeconds": elapsed,
            }
        )

    RESULTS_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    ok = sum(1 for r in results if r["error"] is None)
    summary = f"\n{ok}/{len(results)} succeeded."
    if args.score:
        scored = [r["score"] for r in results if r["score"] is not None]
        if scored:
            summary += f" Average score: {sum(scored) / len(scored):.2f}"
    print(f"{summary} Wrote results to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
