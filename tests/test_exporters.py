import csv

from leadradar.exporters import write_leads
from leadradar.models import Lead


def test_csv_export_has_excel_friendly_columns(tmp_path) -> None:
    output = tmp_path / "leads.csv"
    lead = Lead(
        source="github",
        name="example/router",
        url="https://github.com/example/router",
        owner="example",
        description="Claude and OpenAI fallback router",
        score=10,
        signals=["mentions Claude", "uses or discusses OpenAI"],
        outreach_angle="RouterLink could help with routing.",
    )

    write_leads([lead], str(output), "csv")

    assert output.read_bytes().startswith(b"\xef\xbb\xbf")
    with output.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert rows[0]["status"] == "new"
    assert rows[0]["notes"] == ""
    assert rows[0]["contacted_at"] == ""
    assert rows[0]["signals"] == "mentions Claude; uses or discusses OpenAI"
