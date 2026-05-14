from dataclasses import dataclass, field


@dataclass(frozen=True)
class Lead:
    source: str
    name: str
    url: str
    owner: str
    description: str
    score: int
    signals: list[str] = field(default_factory=list)
    outreach_angle: str = ""
    status: str = "new"
    notes: str = ""
    contacted_at: str = ""
