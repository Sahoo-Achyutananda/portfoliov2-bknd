"""Shared pytest fixtures for the DeepEval suite. Adds the backend root to
sys.path (so `from agent import agent` etc. work regardless of where pytest
is invoked from) and loads .env before anything imports agent.py, which
needs GOOGLE_API_KEY at import time."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

load_dotenv()

import pytest
from deepeval.models import GeminiModel


@pytest.fixture(scope="session")
def judge_model() -> GeminiModel:
    """The LLM that scores each test case. Reuses GOOGLE_API_KEY - no
    separate API key/account needed."""
    return GeminiModel(model="gemini-2.5-flash")
