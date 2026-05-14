from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from leadradar.models import Lead
from leadradar.scoring import score_repository


GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"


class GitHubError(RuntimeError):
    pass


def search_repositories(query: str, limit: int = 25) -> list[Lead]:
    params = urllib.parse.urlencode(
        {
            "q": query,
            "sort": "updated",
            "order": "desc",
            "per_page": min(limit, 100),
        }
    )
    payload = request_json(f"{GITHUB_SEARCH_URL}?{params}")
    items = payload.get("items", [])

    leads = [repository_to_lead(item) for item in items[:limit]]
    return sorted(leads, key=lambda lead: lead.score, reverse=True)


def request_json(url: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "routerlink-leadradar",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise GitHubError(f"GitHub API returned {error.code}: {details}") from error
    except urllib.error.URLError as error:
        raise GitHubError(f"Could not reach GitHub API: {error.reason}") from error


def repository_to_lead(item: dict) -> Lead:
    name = item.get("full_name", "")
    owner = item.get("owner", {}).get("login", "")
    description = item.get("description") or ""
    stars = int(item.get("stargazers_count") or 0)
    pushed_recently = is_recent(item.get("pushed_at"))

    text = " ".join(
        [
            name,
            description,
            item.get("language") or "",
            " ".join(item.get("topics") or []),
        ]
    )
    score = score_repository(text, stars=stars, pushed_recently=pushed_recently)

    return Lead(
        source="github",
        name=name,
        url=item.get("html_url", ""),
        owner=owner,
        description=description,
        score=score.score,
        signals=score.signals,
        outreach_angle=score.outreach_angle,
    )


def is_recent(value: str | None, days: int = 90) -> bool:
    if not value:
        return False

    pushed_at = datetime.fromisoformat(value.replace("Z", "+00:00"))
    age = datetime.now(timezone.utc) - pushed_at
    return age.days <= days
