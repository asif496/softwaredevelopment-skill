# Extra docs

The core eight cover most apps. Add one of these only when its trigger applies; an unneeded doc is one more thing to keep true. When you add one, link it from AGENTS.md's "Read before you work" table.

Contents: PLAN.md · API.md · DEPLOYMENT.md · Decision records · CHANGELOG.md

## docs/PLAN.md

**When:** every standard and large project, after the docs are approved. Template in `assets/templates/PLAN.md`; steps in `modes.md` under "plan".

```markdown
# Build plan: <App>
Status: draft | Last updated: <date>

## Milestones
- M0 Setup: the project runs, checks pass, CI is green.
- M1 <name>: <what a user can do at the end>.

## Tasks
| ID | Task | Feature | Depends on | Status |
|---|---|---|---|---|
| T1 | Scaffold the project; lint, types and CI | setup | - | todo |
| T2 | Sign-in with email and Google | F1 | T1 | todo |
```

## docs/API.md

**When:** the project exposes an API that something other than its own frontend calls, or the frontend and backend are built separately.

Sections:
- **Conventions:** base URL and versioning; authentication; date, id and money formats; pagination; one error format for every endpoint, for example `{ "error": { "code": "plan_not_found", "message": "..." } }`.
- **Endpoints:** a table of `Method | Path | Auth | Purpose`, then a block per endpoint with the request body, the success response, and each error code it can return.
- **Rate limits:** per key or per user, with numbers.
- **Changes:** what counts as breaking, and how consumers are warned.

Rule to include: the API changes in this doc first, then in code. A contract test per endpoint checks the two still agree.

## docs/DEPLOYMENT.md

**When:** the user runs their own servers, there is more than one environment to keep in step, or someone other than the author will have to deploy or recover the app.

Sections:
- **Environments:** `Name | URL | Branch | Database | Who can deploy`.
- **Environment variables:** `Name | Purpose | Where it is set | Reaches the browser?`. Names only; never values.
- **Deploy:** the exact steps or the pipeline that does them, including how migrations run.
- **Rollback:** how to return to the last good version, and what to do about a migration that has already run.
- **Backups:** what is backed up, how often, where, and when a restore was last tested.
- **Monitoring:** where errors and uptime are watched, and who gets alerted.
- **Runbook:** three to five likely incidents (the site is down, sign-in fails, the database is full, a secret leaked), each with first steps.

## Decision records (docs/adr/)

**When:** a decision is expensive to reverse, was argued over, or keeps being questioned. The one-line decision log in ARCHITECTURE.md is enough for everything else.

One file per decision, `docs/adr/0001-use-postgres.md`:

```markdown
# 1. Use Postgres on Supabase
Date: <date> | Status: accepted

## Context
What forced a choice, and the constraints.

## Options
Each option with its main advantage and cost.

## Decision
What was chosen and why.

## Consequences
What gets easier, what gets harder, and what would make us revisit this.
```

Records are never edited after acceptance. A reversed decision gets a new record that says which one it replaces.

## CHANGELOG.md

**When:** other people depend on releases: a library, a public API, or an app with users who need release notes.

Newest first; grouped as Added, Changed, Fixed, Removed; written for the user of the software, not the developer. Each release has a version and a date.
