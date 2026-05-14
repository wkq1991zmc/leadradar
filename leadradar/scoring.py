from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreResult:
    score: int
    signals: list[str]
    outreach_angle: str


KEYWORD_RULES: tuple[tuple[str, int, str], ...] = (
    ("openai", 3, "uses or discusses OpenAI"),
    ("anthropic", 3, "uses or discusses Anthropic"),
    ("claude", 2, "mentions Claude"),
    ("gemini", 2, "mentions Gemini"),
    ("deepseek", 2, "mentions DeepSeek"),
    ("langchain", 2, "uses LangChain"),
    ("llamaindex", 2, "uses LlamaIndex"),
    ("litellm", 4, "uses LiteLLM or adjacent routing tooling"),
    ("fallback", 4, "mentions model fallback"),
    ("router", 2, "mentions routing"),
    ("gateway", 3, "mentions gateway patterns"),
    ("multi-model", 4, "mentions multi-model support"),
    ("rate limit", 2, "mentions rate limits"),
    ("cost", 2, "mentions cost concerns"),
    ("observability", 2, "mentions observability"),
)


def score_repository(text: str, stars: int = 0, pushed_recently: bool = False) -> ScoreResult:
    normalized = text.lower()
    score = 0
    signals: list[str] = []

    for keyword, points, signal in KEYWORD_RULES:
        if keyword in normalized:
            score += points
            signals.append(signal)

    if stars >= 100:
        score += 2
        signals.append("has meaningful public adoption")
    elif stars >= 20:
        score += 1
        signals.append("has early public adoption")

    if pushed_recently:
        score += 2
        signals.append("is actively maintained")

    if not signals:
        signals.append("matched the search query but needs manual review")

    return ScoreResult(
        score=score,
        signals=signals,
        outreach_angle=build_outreach_angle(signals),
    )


def build_outreach_angle(signals: list[str]) -> str:
    joined = ", ".join(signals[:3])
    return (
        "They appear to be building with LLM APIs"
        f" ({joined}). RouterLink could help with model routing, fallback, and cost control."
    )
