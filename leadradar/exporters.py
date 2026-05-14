from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import Lead


FIELDNAMES = [
    "status",
    "source",
    "name",
    "url",
    "owner",
    "description",
    "score",
    "signals",
    "outreach_angle",
    "notes",
    "contacted_at",
]


def write_leads(leads: list[Lead], output: str, output_format: str) -> None:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)

    if output_format == "json":
        write_json(leads, path)
        return

    write_csv(leads, path)


def write_csv(leads: list[Lead], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for lead in leads:
            writer.writerow(serialize_lead(lead))


def write_json(leads: list[Lead], path: Path) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump([serialize_lead(lead) for lead in leads], handle, indent=2)


def serialize_lead(lead: Lead) -> dict[str, object]:
    return {
        "status": lead.status,
        "source": lead.source,
        "name": lead.name,
        "url": lead.url,
        "owner": lead.owner,
        "description": lead.description,
        "score": lead.score,
        "signals": "; ".join(lead.signals),
        "outreach_angle": lead.outreach_angle,
        "notes": lead.notes,
        "contacted_at": lead.contacted_at,
    }
