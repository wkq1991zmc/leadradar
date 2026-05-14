from __future__ import annotations

import argparse
import sys

from .exporters import write_leads
from .sources.github import GitHubError, search_repositories


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="leadradar",
        description="Find and score potential RouterLink leads from public signals.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    github = subparsers.add_parser("github", help="Search GitHub repositories")
    github.add_argument("--query", required=True, help="GitHub repository search query")
    github.add_argument("--limit", type=int, default=25, help="Maximum leads to return")
    github.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Output format",
    )
    github.add_argument("--output", default="leads.csv", help="Output file path")

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "github":
        run_github(args)
        return

    parser.error(f"Unknown command: {args.command}")


def run_github(args: argparse.Namespace) -> None:
    try:
        leads = search_repositories(args.query, limit=args.limit)
    except GitHubError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1) from error

    write_leads(leads, args.output, args.format)
    print(f"Wrote {len(leads)} leads to {args.output}")
