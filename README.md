# Lead Radar

Lead Radar finds potential customers for RouterLink by scanning public developer signals, scoring fit, and exporting leads for human review.

The first MVP focuses on GitHub repositories that mention LLM and AI API tooling. It produces a CSV or JSON file with:

- repository and owner details
- a fit score
- evidence for why the lead may be relevant
- a suggested outreach angle

## Quick Start

```powershell
python -m leadradar github --query "openai anthropic fallback" --limit 20 --format csv --output leads.csv
```

Using a GitHub token is recommended because unauthenticated API limits are low:

```powershell
$env:GITHUB_TOKEN="ghp_your_token_here"
python -m leadradar github --query "langchain openai" --limit 50 --output leads.csv
```

## Example Queries

```powershell
python -m leadradar github --query "openai anthropic"
python -m leadradar github --query "litellm fallback"
python -m leadradar github --query "vercel ai sdk openai"
python -m leadradar github --query "llm gateway"
```

## Output Fields

- `source`: where the lead came from
- `name`: repository name
- `url`: public URL
- `owner`: repository owner or organization
- `description`: public repository description
- `score`: lead-fit score
- `signals`: concise evidence used for scoring
- `outreach_angle`: suggested reason to contact them

## Roadmap

- Add company enrichment from repository owner websites
- Add Hacker News and Product Hunt sources
- Add deduplication across sources
- Add a small review UI
- Add CRM export
