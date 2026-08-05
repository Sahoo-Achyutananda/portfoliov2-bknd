"""Test-only helper for invoking the real agent - mirrors the reply-extraction
logic in main.py's /chat handler, minus the FastAPI wrapper."""

from agent import agent


def ask_agent(message: str) -> str:
    result = agent.invoke({"messages": [{"role": "user", "content": message}]})
    content = result["messages"][-1].content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return str(content)
