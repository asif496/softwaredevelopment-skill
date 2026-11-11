# AGENTS.md and CLAUDE.md guide (repo root)

AGENTS.md is a README for AI agents: what the project is, the exact commands, the rules, and which doc to open for which task. Coding agents such as Codex, Cursor, Gemini CLI, GitHub Copilot's coding agent, Windsurf and Zed read it at the start of a session. None of them read `docs/` on their own, so AGENTS.md is the index that sends the agent to the right doc.

Write it last, because it links to all the others.

## Before writing

Read all the docs and the package manifest (package.json, pyproject.toml, composer.json, pubspec.yaml...). Take the commands from the manifest, not from memory; commands that don't run are the most common failure in this file.

## Rules for this file

- Under about 120 lines. Long instruction files are followed less reliably, and some tools cap how much they load.
- Link to the docs; don't copy them in. Two copies of a rule drift apart.
- Every line should be something the agent would otherwise get wrong. If the agent already does it by default, leave it out.

## Sections

**Project.** One line on what it is and for whom, plus a link to docs/PRD.md.

**Commands.** Install, run locally (with the URL), test, lint and typecheck, build. One line each, copy-pasteable.

**Read before you work.**

| Task | Read first |
|---|---|
| New feature or change in behaviour | docs/PRD.md |
| Any UI or styling | docs/DESIGN_SYSTEM.md |
| New module, route, service or folder | docs/ARCHITECTURE.md |
| Schema, queries or migrations | docs/DATABASE.md |
| Auth, payments, user data, uploads, any API | docs/SECURITY.md |
| Writing any code | docs/CODE_STYLE.md |
| Before saying a task is done | docs/TESTING.md |
| Choosing what to build next | docs/PLAN.md |

Leave out rows for docs the project doesn't have.

**Hard rules.** Five to eight rules taken from the docs, each checkable:
- Never commit secrets. Env variables live in `.env.local`, which is gitignored.
- No schema change without a migration file.
- No new dependency without asking.
- Never disable or delete a failing test to make a build pass.
- Every table has access rules; see docs/DATABASE.md.

**How to work.**
1. Restate the task and list the files you will change.
2. Make the smallest change that does the job.
3. Run lint, typecheck and tests. Fix what fails.
4. Report what changed and anything you could not finish.
5. If a decision changes a doc, update that doc in the same change.

## CLAUDE.md

Claude Code reads CLAUDE.md. Create one that imports AGENTS.md and holds anything that applies to Claude Code only:

```markdown
@AGENTS.md

## Claude Code only
- Use plan mode for any change touching more than 3 files.
```

Notes:
- `@path` imports load the whole file into every session. Don't import all the docs; AGENTS.md links them and the agent opens what a task needs. Importing a short PRD is fine for a small app.
- Some newer Claude Code versions read AGENTS.md by themselves when no CLAUDE.md exists. The import works on every version, so use it.
- For bigger projects, if the user's version supports path-scoped rules in `.claude/rules/`, offer one file per risky area. For example `.claude/rules/database.md`, scoped to the migration and database folders, saying: before changing anything here, read docs/DATABASE.md and docs/SECURITY.md.

## Other tools

- Codex reads `~/.codex/AGENTS.md` (personal rules), then each AGENTS.md from the repo root down to the current folder. Nearer files win. The combined size is capped (32 KiB by default).
- In a monorepo, a nested AGENTS.md inside a package can hold that package's commands and rules.

## Self-check

- Run every command in the Commands section, or confirm it exists in the manifest.
- Every doc in `docs/` is linked at least once.
- No paragraph here duplicates a doc.
- Under 120 lines.

Then verify with the user: start a fresh session and ask "Which docs should you read before adding a new table?" The answer should name docs/DATABASE.md and docs/SECURITY.md.

## Common mistakes

- A 600-line file the agent stops following halfway.
- Vague rules like "write clean code".
- Commands that no longer work.
- Pasting whole docs in instead of linking.

## Lite size

AGENTS.md carries everything: project line, commands, 5-10 rules (naming, where code goes, what never to do), and the definition of done. No "Read before you work" table beyond the PRD.
