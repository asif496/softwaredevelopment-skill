#!/usr/bin/env python3
"""Copy doc templates into a project without overwriting anything.

Usage:
    python3 init_docs.py PROJECT_ROOT --doc prd
    python3 init_docs.py PROJECT_ROOT --doc database --doc security --name "StudyPlan"
    python3 init_docs.py PROJECT_ROOT --all --name "StudyPlan" --type web --size standard
    python3 init_docs.py --list

Create one doc at a time while planning: an unfilled skeleton looks like a
decision to the next agent that reads it. Standard library only.
"""

import argparse
import datetime
import sys
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "assets" / "templates"

# name -> (template file, destination relative to the project root)
DOCS = {
    "prd": ("PRD.md", "docs/PRD.md"),
    "design_system": ("DESIGN_SYSTEM.md", "docs/DESIGN_SYSTEM.md"),
    "architecture": ("ARCHITECTURE.md", "docs/ARCHITECTURE.md"),
    "database": ("DATABASE.md", "docs/DATABASE.md"),
    "security": ("SECURITY.md", "docs/SECURITY.md"),
    "code_style": ("CODE_STYLE.md", "docs/CODE_STYLE.md"),
    "testing": ("TESTING.md", "docs/TESTING.md"),
    "agents": ("AGENTS.md", "AGENTS.md"),
    "claude": ("CLAUDE.md", "CLAUDE.md"),
    "plan": ("PLAN.md", "docs/PLAN.md"),
}

ALIASES = {"design": "design_system", "style": "code_style", "tests": "testing", "db": "database"}


def normalise(name):
    key = name.strip().lower().replace("-", "_").replace(" ", "_")
    if key.endswith(".md"):
        key = key[:-3]
    return ALIASES.get(key, key)


def main():
    parser = argparse.ArgumentParser(description="Copy doc templates into a project (never overwrites).")
    parser.add_argument("root", nargs="?", help="project root folder")
    parser.add_argument("--doc", action="append", default=[], help="doc to create; repeatable")
    parser.add_argument("--all", action="store_true", help="create every doc that is missing")
    parser.add_argument("--name", default="<App name>", help="app name")
    parser.add_argument("--owner", default="<owner>", help="owner shown in the PRD header")
    parser.add_argument("--type", default="web", help="web, mobile, api, cli, automation or ai")
    parser.add_argument("--size", default="standard", help="lite, standard or large")
    parser.add_argument("--list", action="store_true", help="list the available docs and exit")
    args = parser.parse_args()

    if args.list:
        for key, (_, dest) in DOCS.items():
            print(f"{key:<14} -> {dest}")
        return 0

    if not args.root:
        parser.error("PROJECT_ROOT is required")
    if not args.doc and not args.all:
        parser.error("say which doc to create with --doc NAME, or use --all")

    wanted = list(DOCS) if args.all else [normalise(d) for d in args.doc]
    unknown = [d for d in wanted if d not in DOCS]
    if unknown:
        print(f"Unknown doc name: {', '.join(unknown)}. Known: {', '.join(DOCS)}", file=sys.stderr)
        return 2

    root = Path(args.root).expanduser()
    values = {
        "{{APP_NAME}}": args.name,
        "{{OWNER}}": args.owner,
        "{{TYPE}}": args.type,
        "{{SIZE}}": args.size,
        "{{DATE}}": datetime.date.today().isoformat(),
    }

    for key in wanted:
        template_name, dest_rel = DOCS[key]
        template = TEMPLATES / template_name
        dest = root / dest_rel
        if not template.exists():
            print(f"missing template: {template}", file=sys.stderr)
            return 2
        if dest.exists():
            print(f"skipped  {dest_rel} (already exists)")
            continue
        text = template.read_text(encoding="utf-8")
        for placeholder, value in values.items():
            text = text.replace(placeholder, value)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        print(f"created  {dest_rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
