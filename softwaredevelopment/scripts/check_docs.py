#!/usr/bin/env python3
"""Check a project's docs against each other and against the code.

Usage:
    python3 check_docs.py [PROJECT_ROOT]            # human-readable report
    python3 check_docs.py PROJECT_ROOT --json       # machine-readable
    python3 check_docs.py PROJECT_ROOT --strict     # warnings also fail
    python3 check_docs.py PROJECT_ROOT --skip design_system
    python3 check_docs.py PROJECT_ROOT --no-code    # docs only

Exit code: 0 = no errors, 1 = errors found (or warnings with --strict), 2 = bad usage.

What it checks
  Docs:  every expected doc exists; expected sections are present; at most 5 P0
         features; every P0 feature has a story; every story has acceptance
         criteria and cites a real feature; vague words in criteria; every table
         has an access rule; AGENTS.md links every doc and stays short; leftover
         placeholders; IDs cited in other docs exist; the plan covers every P0.
  Code:  (when the folder has code) commands in AGENTS.md and TESTING.md exist in
         package.json; tables in SQL migrations match DATABASE.md; folders named
         in ARCHITECTURE.md exist; env files are gitignored.

It reads the layout written by the softwaredevelopment skill's templates. It is a
net for mechanical mistakes, not a judge of whether the decisions are good.
Standard library only.
"""

import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path

DOC_PATHS = {
    "PRD": "docs/PRD.md",
    "DESIGN_SYSTEM": "docs/DESIGN_SYSTEM.md",
    "ARCHITECTURE": "docs/ARCHITECTURE.md",
    "DATABASE": "docs/DATABASE.md",
    "SECURITY": "docs/SECURITY.md",
    "CODE_STYLE": "docs/CODE_STYLE.md",
    "TESTING": "docs/TESTING.md",
    "AGENTS": "AGENTS.md",
}
PLAN_PATH = "docs/PLAN.md"
NO_UI_TYPES = {"api", "cli", "library", "automation"}
LITE_REQUIRED = {"PRD", "AGENTS"}

# doc -> [(label shown to the user, regex matched against heading text)]
SECTIONS = {
    "PRD": [("Problem", r"\bproblem"), ("Users", r"\busers?\b"), ("Goals", r"\bgoals?\b"),
            ("Features", r"\bfeatures?\b"), ("User stories", r"\bstories\b"),
            ("Open questions", r"\bopen questions")],
    "DESIGN_SYSTEM": [("Colour tokens", r"\bcolou?r"), ("Typography", r"\btypograph"),
                      ("Spacing", r"\bspacing"), ("Components", r"\bcomponents?\b"),
                      ("Accessibility", r"\baccessib")],
    "ARCHITECTURE": [("Stack", r"\bstack\b"), ("Folder structure", r"\bfolder"),
                     ("Request flow", r"\bflow"), ("Environments", r"\benvironments?\b"),
                     ("Decision log", r"\bdecision"), ("Boundaries", r"\bboundar")],
    "DATABASE": [("Conventions", r"\bconventions?\b"), ("Tables", r"\btables?\b"),
                 ("Access rules", r"\baccess"), ("Migrations", r"\bmigrations?\b"),
                 ("Deletion and retention", r"\bdelet|\bretention")],
    "SECURITY": [("Data we hold", r"\bdata\b"), ("Roles", r"\broles?\b"), ("Auth", r"\bauth"),
                 ("Secrets", r"\bsecrets?\b"), ("Input and output", r"\binput"),
                 ("Abuse / rate limits", r"\babuse|\brate"), ("Dependencies", r"\bdependenc"),
                 ("Logging", r"\blogging|\blogs?\b"), ("Pre-merge checklist", r"\bchecklist")],
    "CODE_STYLE": [("Naming", r"\bnaming"), ("Structure", r"\bstructure"), ("Patterns", r"\bpatterns?\b"),
                   ("Avoid", r"\bavoid"), ("Comments", r"\bcomments?\b"), ("Git", r"\bgit\b")],
    "TESTING": [("Layers", r"\blayers?\b"), ("Must be tested", r"\bmust be tested"),
                ("Conventions", r"\bconventions?\b"), ("CI", r"\bci\b"),
                ("Definition of done", r"\bdefinition of done")],
    "AGENTS": [("Commands", r"\bcommands?\b"), ("Read before you work", r"\bread before"),
               ("Hard rules", r"\brules?\b"), ("How to work", r"\bhow to work")],
}
LITE_SECTIONS = {"PRD": [("Problem", r"\bproblem"), ("Features", r"\bfeatures?\b")],
                 "AGENTS": [("Commands", r"\bcommands?\b"), ("Rules", r"\brules?\b")]}

VAGUE = ["fast", "quick", "quickly", "easy", "easily", "intuitive", "user-friendly", "nice", "clean",
         "seamless", "seamlessly", "smooth", "smoothly", "properly", "appropriately", "robust",
         "as expected", "etc"]
VAGUE_RE = re.compile(r"(?<![\w-])(" + "|".join(re.escape(w) for w in VAGUE) + r")(?![\w-])", re.I)

CODE_MARKERS = ["package.json", "pyproject.toml", "requirements.txt", "composer.json", "pubspec.yaml",
                "go.mod", "Cargo.toml", "Gemfile", "src", "app", "lib", "supabase"]
MIGRATION_DIRS = ["supabase/migrations", "migrations", "db/migrate", "db/migrations",
                  "database/migrations", "prisma/migrations", "drizzle", "sql"]
HTML_TAGS = {"br", "hr", "details", "summary", "kbd", "sub", "sup", "b", "i", "u", "em", "strong",
             "code", "pre", "a", "img", "p", "div", "span", "table", "tr", "td", "th", "ul", "ol", "li"}
PM_BUILTINS = {"install", "i", "add", "remove", "rm", "ci", "audit", "exec", "dlx", "x", "create", "init",
               "up", "update", "upgrade", "why", "link", "publish", "outdated", "dev-deps", "cache"}
NPM_SCRIPT_SHORTCUTS = {"test", "start", "stop", "restart"}

FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
CHECKBOX_RE = re.compile(r"^\s*[-*]\s*\[( |x|X)\]")


class Report:
    def __init__(self):
        self.items = []  # (level, doc, message)

    def add(self, level, doc, message):
        self.items.append((level, doc, message))

    def error(self, doc, message):
        self.add("error", doc, message)

    def warn(self, doc, message):
        self.add("warning", doc, message)

    def note(self, doc, message):
        self.add("note", doc, message)

    def of(self, level):
        return [(d, m) for lvl, d, m in self.items if lvl == level]


def read(path):
    return path.read_text(encoding="utf-8", errors="replace")


def strip_code(text):
    """Remove fenced code blocks and inline code, keeping line count stable."""
    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else re.sub(r"`[^`\n]*`", "", line))
    return "\n".join(out)


def headings(text):
    """[(level, title, line_index)] for headings outside code fences."""
    found, in_fence = [], False
    for index, line in enumerate(text.splitlines()):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            found.append((len(match.group(1)), match.group(2), index))
    return found


def has_heading(text, pattern):
    return any(re.search(pattern, title, re.I) for _, title, _ in headings(text))


def section(text, pattern):
    """Body of the first heading matching pattern, up to the next heading of the same or a higher level."""
    lines = text.splitlines()
    heads = headings(text)
    for position, (level, title, index) in enumerate(heads):
        if re.search(pattern, title, re.I):
            end = len(lines)
            for next_level, _, next_index in heads[position + 1:]:
                if next_level <= level:
                    end = next_index
                    break
            return "\n".join(lines[index + 1:end])
    return None


def fenced_lines(text):
    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            out.append(line)
    return out


def header_value(text, key):
    for line in text.splitlines()[:8]:
        match = re.search(r"\b" + key + r":\s*([^|\n]+)", line, re.I)
        if match:
            return match.group(1).strip()
    return None


def open_question_count(text):
    body = section(text, r"\bopen questions")
    if body is None:
        return 0
    return sum(1 for line in body.splitlines() if re.match(r"^\s*[-*]\s*\[ \]", line))


# ----------------------------------------------------------------- PRD

def parse_prd(text):
    features = {}  # id -> priority ("P0", "P1", "P2", "cut")
    for line in text.splitlines():
        match = re.match(r"^\|\s*(F\d+)\s*\|.*\|\s*(P[0-2]|cut)\s*\|\s*$", line.strip(), re.I)
        if match:
            features[match.group(1).upper()] = match.group(2).upper() if match.group(2).upper() != "CUT" else "cut"

    stories = []  # {id, features, criteria: [(line_no, text)]}
    lines = text.splitlines()
    current = None
    for index, line in enumerate(lines):
        start = re.match(r"^\W*(US-\d+)\b\s*(?:\(([^)]*)\))?", line)
        if start:
            current = {"id": start.group(1), "line": index + 1,
                       "features": [f.upper() for f in re.findall(r"F\d+", start.group(2) or "", re.I)],
                       "criteria": []}
            stories.append(current)
            continue
        if HEADING_RE.match(line):
            current = None
            continue
        if current is not None and CHECKBOX_RE.match(line):
            current["criteria"].append((index + 1, line.strip()))
    return features, stories


def check_prd(text, size, doc_type, report):
    doc = DOC_PATHS["PRD"]
    features, stories = parse_prd(text)
    p0 = [f for f, p in features.items() if p == "P0"]

    if not re.search(r"non-goals?", text, re.I):
        report.error(doc, "No non-goals. Say what v1 will not do, or the agent will add it.")
    if not features:
        report.error(doc, "No feature table found (rows like `| F1 | Feature | P0 |`).")
        return features, stories
    if not p0:
        report.error(doc, "No P0 feature. Mark what v1 cannot ship without.")
    if len(p0) > 5:
        report.warn(doc, f"{len(p0)} P0 features ({', '.join(p0)}). Keep v1 to 5 or fewer.")

    if size != "lite":
        cited = {f for s in stories for f in s["features"]}
        for feature in p0:
            if feature not in cited:
                report.error(doc, f"P0 feature {feature} has no user story.")
        for story in stories:
            if not story["features"]:
                report.warn(doc, f"{story['id']} (line {story['line']}) doesn't cite a feature, e.g. `US-1 (F1)`.")
            for feature in story["features"]:
                if feature not in features:
                    report.error(doc, f"{story['id']} cites {feature}, which is not in the feature table.")
            if not story["criteria"]:
                report.error(doc, f"{story['id']} has no acceptance criteria (checkbox lines).")
            for line_no, criterion in story["criteria"]:
                vague = VAGUE_RE.search(criterion)
                if vague:
                    report.warn(doc, f"Line {line_no}: \"{vague.group(1)}\" can't be tested. Say what is observed.")
    return features, stories


# ----------------------------------------------------------------- other docs

def check_design_system(text, report):
    doc = DOC_PATHS["DESIGN_SYSTEM"]
    if len(re.findall(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", text)) < 5:
        report.warn(doc, "Fewer than 5 hex colour values. Tokens need exact values.")
    if not re.search(r"\bdark\b", text, re.I):
        report.warn(doc, "No dark-mode values.")
    missing = [s for s in ("disabled", "loading", "error", "empty", "focus") if not re.search(r"\b" + s, text, re.I)]
    if missing:
        report.warn(doc, f"Component states never mentioned: {', '.join(missing)}.")
    if "4.5" not in text:
        report.warn(doc, "No contrast rule (text contrast at least 4.5:1).")


def check_architecture(text, report):
    doc = DOC_PATHS["ARCHITECTURE"]
    log = section(text, r"\bdecision")
    if log is not None and not re.search(r"\b\d{4}-\d{2}-\d{2}\b", log):
        report.warn(doc, "Decision log has no dated entry (`YYYY-MM-DD: decision, because reason`).")


def documented_tables(text):
    return [m.group(1) for m in re.finditer(r"(?m)^#{2,4}\s*Table:\s*`?([A-Za-z_][\w.]*)`?", text)]


def check_database(text, report):
    doc = DOC_PATHS["DATABASE"]
    tables = documented_tables(text)
    if not tables:
        report.warn(doc, "No `### Table: <name>` blocks found, so tables can't be cross-checked.")
        return tables
    access = section(text, r"\baccess")
    if access is None:
        report.error(doc, "No access rules section. Every table needs a rule for who may read and write it.")
        return tables
    for table in tables:
        if not re.search(r"(?<![\w.])" + re.escape(table) + r"(?![\w])", access):
            report.error(doc, f"Table `{table}` has no access rule.")
    return tables


def check_security(text, p0, size, report):
    doc = DOC_PATHS["SECURITY"]
    checklist = section(text, r"\bchecklist")
    if checklist is not None:
        if sum(1 for line in checklist.splitlines() if CHECKBOX_RE.match(line)) < 4:
            report.warn(doc, "Pre-merge checklist has fewer than 4 checkbox items.")
        if "A01" not in checklist:
            report.warn(doc, "Checklist doesn't cover A01 (access control), the top OWASP risk.")
    cases = section(text, r"\babuse cases")
    if cases is None:
        if size != "lite":
            report.warn(doc, "No abuse cases section (one \"what if a user...\" line per P0 feature).")
    else:
        for feature in p0:
            if not re.search(r"\b" + feature + r"\b", cases):
                report.warn(doc, f"No abuse case for P0 feature {feature}.")


def check_code_style(text, report):
    doc = DOC_PATHS["CODE_STYLE"]
    if not fenced_lines(text):
        report.warn(doc, "No code examples. A pattern with no example is read differently every time.")


def check_testing(text, report):
    doc = DOC_PATHS["TESTING"]
    done = section(text, r"\bdefinition of done")
    if done is not None and sum(1 for line in done.splitlines() if CHECKBOX_RE.match(line)) < 3:
        report.warn(doc, "Definition of done has fewer than 3 checkbox items.")
    if not re.search(r"never (change|edit|modify|weaken|delete)[^.\n]*test", text, re.I):
        report.warn(doc, "Missing the rule that a test is never changed just to make it pass.")


def check_agents(root, text, expected_docs, has_plan, report):
    doc = DOC_PATHS["AGENTS"]
    line_count = len(text.splitlines())
    if line_count > 120:
        report.warn(doc, f"{line_count} lines. Keep it under about 120 and link to the docs instead.")
    for name in expected_docs:
        if name != "AGENTS" and DOC_PATHS[name] not in text:
            report.error(doc, f"Doesn't link {DOC_PATHS[name]}. Agents won't know to read it.")
    if has_plan and PLAN_PATH not in text:
        report.warn(doc, f"Doesn't link {PLAN_PATH}.")
    claude = root / "CLAUDE.md"
    if not claude.exists():
        report.note("CLAUDE.md", "Not found. Claude Code users need one that imports AGENTS.md (`@AGENTS.md`).")
    elif "@AGENTS.md" not in read(claude):
        report.warn("CLAUDE.md", "Doesn't import AGENTS.md (`@AGENTS.md`), so the two can drift apart.")


def check_placeholders(name, path, text, report):
    stripped = strip_code(text)
    seen = []
    for index, line in enumerate(stripped.splitlines(), start=1):
        for match in re.finditer(r"<([A-Za-z][^<>\n]{0,80})>", line):
            inner = match.group(1).strip()
            tag = inner.split()[0].strip("/").lower()
            if tag in HTML_TAGS or inner.lower().startswith(("http://", "https://", "mailto:")):
                continue
            seen.append(index)
        if re.search(r"\{\{[A-Z_]+\}\}", line):
            seen.append(index)
    if seen:
        lines = sorted(set(seen))
        shown = ", ".join(str(n) for n in lines[:8]) + (" and more" if len(lines) > 8 else "")
        approved = (header_value(text, "Status") or "").lower().startswith("approved")
        if approved:
            report.error(path, f"Marked approved but has unfilled placeholder text on line(s) {shown}.")
        else:
            report.warn(path, f"Unfilled placeholder text on line(s) {shown}.")

    open_q = section(stripped, r"\bopen questions") or ""
    body = stripped.replace(open_q, "") if open_q else stripped
    for index, line in enumerate(body.splitlines(), start=1):
        if re.search(r"\b(TBD|TODO|FIXME)\b|\?\?\?", line):
            report.warn(path, f"Line {index}: undecided item outside \"Open questions\". Move it there.")
            break


# ----------------------------------------------------------------- plan

def parse_plan(text):
    tasks = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and re.fullmatch(r"T\d+", cells[0], re.I):
            tasks.append({"id": cells[0].upper(), "task": cells[1], "feature": cells[2],
                          "depends": cells[3], "status": cells[4].lower()})
    return tasks


def check_plan(text, features, report):
    tasks = parse_plan(text)
    if not tasks:
        report.warn(PLAN_PATH, "No task rows found (`| T1 | Task | F1 | - | todo |`).")
        return tasks
    ids = {t["id"] for t in tasks}
    covered = set()
    for task in tasks:
        for feature in re.findall(r"\bF\d+\b", task["feature"], re.I):
            feature = feature.upper()
            covered.add(feature)
            if features and feature not in features:
                report.error(PLAN_PATH, f"{task['id']} is for {feature}, which is not in the PRD.")
        for dep in re.findall(r"\bT\d+\b", task["depends"], re.I):
            if dep.upper() not in ids:
                report.warn(PLAN_PATH, f"{task['id']} depends on {dep.upper()}, which doesn't exist.")
        if task["status"] not in ("todo", "doing", "done", "cut"):
            report.warn(PLAN_PATH, f"{task['id']} has status \"{task['status']}\". Use todo, doing, done or cut.")
    for feature, priority in features.items():
        if priority == "P0" and feature not in covered:
            report.warn(PLAN_PATH, f"No task builds P0 feature {feature}.")
    return tasks


def task_sort_key(task):
    return int(task["id"][1:])


def plan_summary(tasks):
    live = [t for t in tasks if t["status"] != "cut"]
    done = {t["id"] for t in live if t["status"] == "done"}
    next_task = None
    for task in sorted(live, key=task_sort_key):
        if task["status"] in ("todo", "doing"):
            deps = {d.upper() for d in re.findall(r"\bT\d+\b", task["depends"], re.I)}
            if deps <= done or task["status"] == "doing":
                next_task = task
                break
    return {"total": len(live), "done": len(done), "next": next_task["id"] if next_task else None,
            "next_task": next_task["task"] if next_task else None}


# ----------------------------------------------------------------- code

def has_code(root):
    return any((root / marker).exists() for marker in CODE_MARKERS)


def check_commands(root, texts, report):
    manifest = root / "package.json"
    if not manifest.exists():
        return
    try:
        scripts = set((json.loads(read(manifest)).get("scripts") or {}).keys())
    except (ValueError, AttributeError):
        report.warn("package.json", "Couldn't be parsed, so commands weren't checked.")
        return
    flagged = set()
    for path, text in texts.items():
        for match in re.finditer(r"\b(npm|pnpm|yarn|bun)\s+(run\s+)?([A-Za-z][\w:.-]*)", text):
            manager, run, name = match.group(1), bool(match.group(2)), match.group(3).rstrip(".:-")
            if not run:
                if manager == "npm" and name not in NPM_SCRIPT_SHORTCUTS:
                    continue
                if name in PM_BUILTINS or name == "run":
                    continue
            if name not in scripts and (path, name) not in flagged:
                flagged.add((path, name))
                command = f"{manager} {'run ' if run else ''}{name}"
                report.warn(path, f"Command `{command}` has no \"{name}\" script in package.json.")


def migration_tables(root):
    found, any_sql = set(), False
    for rel in MIGRATION_DIRS:
        folder = root / rel
        if not folder.is_dir():
            continue
        for sql in folder.rglob("*.sql"):
            any_sql = True
            for match in re.finditer(
                    r"create\s+table\s+(?:if\s+not\s+exists\s+)?(?:\"?(\w+)\"?\.)?\"?(\w+)\"?", read(sql), re.I):
                schema, table = match.group(1), match.group(2)
                if schema and schema.lower() != "public":
                    continue
                found.add(table)
    return found, any_sql


def check_tables_against_code(root, tables, report):
    in_code, any_sql = migration_tables(root)
    if not any_sql:
        return
    documented = {t.split(".")[-1] for t in tables}
    for table in sorted(in_code - documented):
        report.warn(DOC_PATHS["DATABASE"], f"Table `{table}` exists in the migrations but not in this doc.")
    for table in sorted(documented - in_code):
        report.note(DOC_PATHS["DATABASE"], f"Table `{table}` is documented but no SQL migration creates it yet.")


def check_folders(root, text, report):
    body = section(text, r"\bfolder")
    if body is None:
        return
    missing = []
    for line in fenced_lines(body):
        words = line.strip().lstrip("├└│─ ").split()
        token = words[0] if words else ""
        if "/" not in token or not re.fullmatch(r"[\w.@()\[\]-]+(?:/[\w.@()\[\]-]+)*/?", token):
            continue
        if not (root / token).exists():
            missing.append(token)
    if missing:
        report.note(DOC_PATHS["ARCHITECTURE"],
                    f"Listed folders that don't exist (fine if not built yet): {', '.join(missing)}.")


def check_env_files(root, report):
    examples = (".example", ".sample", ".template", ".dist")
    env_files = [p.name for p in root.iterdir()
                 if p.is_file() and (p.name == ".env" or p.name.startswith(".env.")) and not p.name.endswith(examples)]
    if not env_files:
        return
    ignore = root / ".gitignore"
    patterns = []
    if ignore.exists():
        patterns = [ln.strip().lstrip("/") for ln in read(ignore).splitlines()
                    if ln.strip() and not ln.strip().startswith(("#", "!"))]
    for name in env_files:
        if not any(fnmatch.fnmatch(name, pattern) for pattern in patterns):
            report.error(name, "Env file is not covered by .gitignore. Secrets could be committed.")


# ----------------------------------------------------------------- main

def run(root, skip, check_code):
    report = Report()
    present = {name: root / rel for name, rel in DOC_PATHS.items() if (root / rel).exists()}
    texts = {name: read(path) for name, path in present.items()}

    prd_text = texts.get("PRD", "")
    doc_type = (header_value(prd_text, "Type") or "web").lower().split()[0] if prd_text else "web"
    size = (header_value(prd_text, "Size") or "standard").lower().split()[0] if prd_text else "standard"
    if size not in ("lite", "standard", "large"):
        size = "standard"

    expected = set(DOC_PATHS)
    if size == "lite":
        expected = set(LITE_REQUIRED)
    if doc_type in NO_UI_TYPES:
        expected.discard("DESIGN_SYSTEM")
    expected -= skip

    order = list(DOC_PATHS)
    for name in order:
        if name in expected and name not in present:
            report.error(DOC_PATHS[name], "Missing.")

    section_rules = LITE_SECTIONS if size == "lite" else SECTIONS
    for name in order:
        if name not in present:
            continue
        for label, pattern in section_rules.get(name, []):
            if not has_heading(texts[name], pattern):
                report.warn(DOC_PATHS[name], f"No \"{label}\" section.")
        check_placeholders(name, DOC_PATHS[name], texts[name], report)
        if name != "AGENTS":
            status = (header_value(texts[name], "Status") or "").lower()
            if not status:
                report.warn(DOC_PATHS[name], "No `Status: draft | approved` line at the top.")
            elif status.split()[0] not in ("draft", "approved"):
                report.warn(DOC_PATHS[name], f"Status is \"{status}\". Use draft or approved.")

    features, stories = ({}, [])
    if "PRD" in present:
        features, stories = check_prd(prd_text, size, doc_type, report)
    p0 = [f for f, p in features.items() if p == "P0"]
    story_ids = {s["id"] for s in stories}

    if "DESIGN_SYSTEM" in present:
        check_design_system(texts["DESIGN_SYSTEM"], report)
    if "ARCHITECTURE" in present:
        check_architecture(texts["ARCHITECTURE"], report)
    tables = check_database(texts["DATABASE"], report) if "DATABASE" in present else []
    if "SECURITY" in present:
        check_security(texts["SECURITY"], p0, size, report)
    if "CODE_STYLE" in present:
        check_code_style(texts["CODE_STYLE"], report)
    if "TESTING" in present:
        check_testing(texts["TESTING"], report)

    plan_file = root / PLAN_PATH
    tasks = []
    if plan_file.exists():
        plan_text = read(plan_file)
        check_placeholders("PLAN", PLAN_PATH, plan_text, report)
        tasks = check_plan(plan_text, features, report)

    if "AGENTS" in present:
        linked = [n for n in order if n in present]
        check_agents(root, texts["AGENTS"], linked, plan_file.exists(), report)

    # IDs cited outside the PRD must exist in it.
    if features:
        for name in ("SECURITY", "TESTING"):
            if name not in present:
                continue
            stripped = strip_code(texts[name])
            for feature in sorted(set(re.findall(r"\bF\d+\b", stripped))):
                if feature not in features:
                    report.warn(DOC_PATHS[name], f"Cites {feature}, which is not in the PRD feature table.")
            for story in sorted(set(re.findall(r"\bUS-\d+\b", stripped))):
                if story_ids and story not in story_ids:
                    report.warn(DOC_PATHS[name], f"Cites {story}, which is not in the PRD.")

    code_checked = False
    if check_code and has_code(root):
        code_checked = True
        command_texts = {DOC_PATHS[n]: texts[n] for n in ("AGENTS", "TESTING") if n in present}
        check_commands(root, command_texts, report)
        if tables:
            check_tables_against_code(root, tables, report)
        if "ARCHITECTURE" in present:
            check_folders(root, texts["ARCHITECTURE"], report)
        check_env_files(root, report)

    rows = []
    for name in order:
        rel = DOC_PATHS[name]
        if name in present:
            text = texts[name]
            rows.append({"doc": rel,
                         "status": "-" if name == "AGENTS" else (header_value(text, "Status") or "?").split()[0].lower(),
                         "updated": header_value(text, "Last updated") or "-",
                         "lines": len(text.splitlines()),
                         "open_questions": open_question_count(text)})
        elif name in expected:
            rows.append({"doc": rel, "status": "missing", "updated": "-", "lines": 0, "open_questions": 0})
        else:
            rows.append({"doc": rel, "status": "not needed", "updated": "-", "lines": 0, "open_questions": 0})
    if plan_file.exists():
        text = read(plan_file)
        rows.append({"doc": PLAN_PATH, "status": (header_value(text, "Status") or "?").split()[0].lower(),
                     "updated": header_value(text, "Last updated") or "-",
                     "lines": len(text.splitlines()), "open_questions": 0})

    return {
        "root": str(root),
        "type": doc_type,
        "size": size,
        "docs": rows,
        "errors": [{"doc": d, "message": m} for d, m in report.of("error")],
        "warnings": [{"doc": d, "message": m} for d, m in report.of("warning")],
        "notes": [{"doc": d, "message": m} for d, m in report.of("note")],
        "plan": plan_summary(tasks) if tasks else None,
        "code_checked": code_checked,
    }


def print_report(result):
    print(f"Docs check: {result['root']}")
    print(f"Type: {result['type']} | Size: {result['size']} | "
          f"Code checks: {'yes' if result['code_checked'] else 'no'}")
    print()
    print(f"{'Doc':<24} {'Status':<11} {'Updated':<12} {'Lines':>5}  Open questions")
    for row in result["docs"]:
        print(f"{row['doc']:<24} {row['status']:<11} {row['updated']:<12} {row['lines']:>5}  {row['open_questions']}")
    for title, key in (("ERRORS", "errors"), ("WARNINGS", "warnings"), ("NOTES", "notes")):
        if result[key]:
            print(f"\n{title} ({len(result[key])})")
            for item in result[key]:
                print(f"  {item['doc']}: {item['message']}")
    plan = result["plan"]
    if plan:
        tail = f"; next: {plan['next']} {plan['next_task']}" if plan["next"] else ""
        print(f"\nPlan: {plan['done']}/{plan['total']} tasks done{tail}")
    print(f"\nResult: {len(result['errors'])} error(s), {len(result['warnings'])} warning(s), "
          f"{len(result['notes'])} note(s).")


def main():
    parser = argparse.ArgumentParser(description="Check project docs against each other and the code.")
    parser.add_argument("root", nargs="?", default=".", help="project root (default: current folder)")
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    parser.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    parser.add_argument("--no-code", action="store_true", help="skip the checks against the code")
    parser.add_argument("--skip", action="append", default=[],
                        help="a doc this project deliberately doesn't have, e.g. design_system; repeatable")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"Not a folder: {root}", file=sys.stderr)
        return 2
    skip = {s.strip().upper().replace("-", "_").removesuffix(".MD") for s in args.skip}
    unknown = skip - set(DOC_PATHS)
    if unknown:
        print(f"Unknown doc in --skip: {', '.join(sorted(unknown))}. Known: {', '.join(DOC_PATHS)}", file=sys.stderr)
        return 2

    result = run(root, skip, not args.no_code)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)
    failed = bool(result["errors"]) or (args.strict and bool(result["warnings"]))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
