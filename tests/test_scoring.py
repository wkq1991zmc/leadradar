from leadradar.scoring import score_repository


def test_scores_multi_provider_gateway_signal() -> None:
    result = score_repository(
        "OpenAI Anthropic gateway with fallback and observability",
        stars=120,
        pushed_recently=True,
    )

    assert result.score >= 15
    assert "mentions model fallback" in result.signals
    assert "RouterLink could help" in result.outreach_angle


def test_low_signal_repo_still_gets_review_reason() -> None:
    result = score_repository("small todo app")

    assert result.score == 0
    assert result.signals == ["matched the search query but needs manual review"]
