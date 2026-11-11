---
name: softwaredevelopment
description: Use to start, plan, document, audit or build a software project. Writes 8 reviewed project docs and a build plan, then keeps docs and code in agreement.
---

# Software Development: decide on paper, then build

An AI coding agent starts every session with an empty memory. Without written decisions it drifts: features nobody asked for, a new button style on every screen, a second API client that differs from the first, a column renamed in one place only, tables any logged-in user can read, keys committed to Git, and "done" that was never tested. This skill writes the decisions down once, in files the agent rereads every session, then builds against them and keeps them true.

Rule of thumb to share with the user: if you've had to explain something to the AI twice, it belongs in one of these files.

## What gets produced

```
project-root/
├── AGENTS.md              map for every AI agent: commands, rules, which doc to read when
├── CLAUDE.md              imports AGENTS.md (for Claude Code)
└── docs/
    ├── PRD.md             what we build, for whom, and what we don't
    ├── DESIGN_SYSTEM.md   how it looks
    ├── ARCHITECTURE.md    how the parts fit
    ├── DATABASE.md        what data we store and who may touch it
    ├── SECURITY.md        what must never go wrong
    ├── CODE_STYLE.md      how code is written here
    ├── TESTING.md         how we prove it works
    └── PLAN.md            the build order, one small task at a time
```

Write them in that order, with AGENTS.md after TESTING.md and PLAN.md last. Each doc builds on the ones before it, and AGENTS.md links to all of them.

## Bundled files

| File | Read it when |
|---|---|
| `references/prd.md`, `design-system.md`, `architecture.md`, `database.md`, `security.md`, `code-style.md`, `testing.md`, `agents.md` | You are about to write that doc. Each has the questions to ask, section detail, a self-check and the common mistakes. |
| `references/project-types.md` | At the start of a full run, and whenever the project isn't a plain web app or uses a stack other than the example one. |
| `references/modes.md` | The user asks for `existing`, `status`, `audit`, `plan`, `build`, `change` or `review`. |
| `references/extra-docs.md` | A large project, a public API, or a deployment the user must run themselves. |
| `assets/templates/` | Starting any doc. One skeleton per doc. |
| `scripts/init_docs.py` | Copying a template into the project without overwriting anything. |
| `scripts/check_docs.py` | Checking the docs against each other and against the code. |

If these files aren't there (the skill was installed as a single file), this file has everything the core flow needs. Skip the script steps and do their checks by hand.

## Commands

| User says | Do |
|---|---|
| `/softwaredevelopment` with nothing else | Ask for the app in 3-5 lines (who it's for, the problem, the main thing users do, the look, any tech they already want). Then run the full flow. |
| `/softwaredevelopment <app idea>` | Run the full flow, starting at "Size the job". |
| `/softwaredevelopment <doc>` (`prd`, `security`, `agents`...) | Write or redo only that doc. Read the docs before it first; if they're missing, say which and offer to write them. |
| `/softwaredevelopment existing` (or the folder already has code) | Document the project as it is, then list where the code breaks its own docs. |
| `/softwaredevelopment status` | Show each doc's status, open questions and the next step. |
| `/softwaredevelopment audit` | Check the docs for gaps, vague rules and contradictions. Report; change nothing. |
| `/softwaredevelopment plan` | Write or refresh docs/PLAN.md. |
| `/softwaredevelopment build <F1 / T3 / next>` | Build one feature or task from the plan. |
| `/softwaredevelopment change <what>` | Work out which docs a change touches, update them first, then the code. |
| `/softwaredevelopment review` | Drift check: list every place docs and code disagree. |

Plain requests mean the same thing ("plan my app", "document this repo", "are my docs still right?"). Steps for the last seven are in `references/modes.md`; a short version is at the end of this file.

If `docs/` already has some docs, read them and resume at the first one that is missing or still `draft`. Never overwrite an existing doc without showing what would change and getting a yes.

## Size the job

Not every project needs eight docs. Decide two things before the PRD and tell the user in one line, so they can overrule you.

| Size | Signals | Doc set |
|---|---|---|
| lite | One person, 1-3 features, days of work, no accounts: a script, landing page, small tool or single automation | Short PRD + AGENTS.md with the rules inline. Add SECURITY.md if it holds personal data or secrets, DATABASE.md if it has its own tables. |
| standard | Accounts and a database, weeks of work | All 8 docs + PLAN.md |
| large | A team, payments or regulated data, several services, or a public API | All 8 + PLAN.md + the extras that apply (API.md, DEPLOYMENT.md, decision records) |

Type: `web`, `mobile`, `api`, `cli` (or library), `automation` (workflows between systems such as a CRM), `ai` (the product is built around a model). Types with no screens skip DESIGN_SYSTEM.md. Other types reshape some docs; `references/project-types.md` says how, and translates the stack-specific rules.

Record both in the PRD header: `Type: web | Size: standard`.

## Ground rules

- **Stop after each doc for review.** A wrong PRD produces seven wrong docs, so mistakes must be caught where they start. Don't begin the next doc until the user approves this one.
- **No app code until the docs are approved.** Setup work a doc implies (lint config, test tools, first migration, a styleguide page) goes on a "Setup after approval" list.
- **Specific, checkable values.** Numbers, names, hex values, file paths, commands. "Buttons use --accent" can be followed and checked; "make it look nice" can't.
- **Keep v1 small.** At most 5 P0 features. A small app gets about one page per doc.
- **Don't guess.** Undecided things go in an "Open questions" list at the end of the doc. When the user says "you decide", pick a default and list it under "Assumptions" in your summary so they can veto it.
- **Stable IDs.** Features are F1, F2; stories US-1, US-2; plan tasks T1, T2. Never renumber. A cut feature stays in the table marked `cut`, so nothing points at a missing ID.
- **Stay consistent.** If a later doc needs to change an earlier decision, say so, and update the earlier doc in the same step once the user agrees.
- **Fit the stack.** The examples use Next.js + TypeScript, Tailwind + shadcn/ui, Postgres on Supabase with Row Level Security, and Vercel. Use the user's stack if they have one and translate the stack-specific rules.
- **Status line.** Every doc in `docs/` starts with `Status: draft | Last updated: <date>`. Set it to `approved` when the user approves.
- **Language.** Talk to the user in their language. Write the docs in English unless they ask otherwise, since agents and tools read them.

## How to write each doc

1. Read the docs that come before it, and its guide in `references/`.
2. Ask what you still need to know, in one message. Skip anything already answered.
3. Start from the template: `python3 <skill-dir>/scripts/init_docs.py <project-root> --doc <name>`, or copy it from `assets/templates/`. Create one doc at a time; an unfilled skeleton looks like a decision to the next agent that reads it.
4. Write it, then run the guide's self-check and fix what fails.
5. Present it: 3-5 bullets on the key decisions, then assumptions, then open questions. Ask the user to approve or change it.
6. On approval, set `Status: approved` and today's date, then move on.

With a project folder (Claude Code, or a folder connected to the chat), write the files at the paths above. With no project folder, build the same structure in the working directory, show each doc for review, and deliver everything at the end as a zip that keeps the folder layout.

## The docs

Each entry is the minimum. The guide in `references/` has the detail.

### 1. docs/PRD.md

It stops the agent inventing features, and every other doc depends on it. Interview first: one message, at most 10 questions (users, core flow, must-have vs later, out of scope, success measure, platform, sign-in, sensitive data, roles, constraints).

Sections: Problem (who struggles with what, and today's workaround) · Users · Goals (measurable) and Non-goals · Features table `| ID | Feature | Priority |` with P0/P1/P2 · User stories, each as `**US-1 (F2):** As a <user>, I want <action> so that <benefit>.` followed by checkbox acceptance criteria in Given/When/Then form · User flows · Screens · Constraints (devices, speed, languages, deadline) · Open questions.

Check: non-goals exist; at most 5 P0; every P0 has a story; every criterion can be tested by a person or a script (the exact error text, not "handles errors well").

### 2. docs/DESIGN_SYSTEM.md

Without it every screen gets slightly different colours, spacing and fonts. Ask for a reference app, a few adjectives or a screenshot if the look is undecided.

Sections: Principles (3-4 lines) · Colour tokens table with light and dark hex values and what each is for, one accent only · Typography (font, sizes, weights) · Spacing scale, radius, shadow · Components with every state: default, hover, focus, disabled, loading, error, empty · Layout and breakpoints · Accessibility (contrast at least 4.5:1, visible focus ring, 44x44 px tap targets) · Voice (buttons are verbs).

Rule to include: components never hard-code a colour or spacing value; they use the token. Setup list: a `/styleguide` page showing every token and component.

### 3. docs/ARCHITECTURE.md

The map of the code. It stops the agent creating a second API client or putting database calls inside a button. Propose the simplest design that ships the P0 features. **Show the stack and wait for the user's OK before writing the rest**, because the stack is the hardest decision to reverse.

Sections: Stack table (layer, choice with version, one-line reason) · System diagram in text arrows · Folder structure, one line per folder saying what belongs there and what doesn't · Request flow: the main user action traced end to end through real file names · External services · Environments (local, preview, production) and how deploys happen · Decision log (`YYYY-MM-DD: decision, because reason`) · Boundaries (what may call what).

### 4. docs/DATABASE.md

Data is the one thing that can't be undone. Include only the tables the P0 features need.

Sections: Entities in one line · Conventions (naming; `id`, `created_at`, `updated_at` on every table; money as integer minor units; timestamps in UTC) · one `### Table: <name>` block per table with columns, types, nullability, constraints and indexes · Access rules: who may select, insert, update and delete each table · Migrations (every change is a new file; never drop or rename in one step) · Seed data · Deletion and retention.

Check: every table has an access rule, and no table is readable by anonymous users unless the PRD says so. Setup list: first migration and access policies.

### 5. docs/SECURITY.md

An agent produces working code long before it produces safe code. Act as a security reviewer.

Sections: Data we hold and its sensitivity · Roles and how each is enforced · Auth and sessions (every server route checks the session; authorization happens on the server, never by hiding a button) · Secrets (where they live, what never reaches the browser, rotate first if leaked) · Input and output (server-side validation, parameterized queries, upload limits) · Abuse (rate limits on sign-in and on anything that sends email or calls a paid API) · Dependencies (approval and audit) · Logging (request id; never passwords, tokens or keys) · Abuse cases: one "what if a user tries..." line per P0 feature · Pre-merge checklist mapped to the OWASP Top 10:2025.

If code exists, review it against this doc and list every violation with file and line.

### 6. docs/CODE_STYLE.md

It makes code from session 30 read like code from session 1. Write only rules a linter can't enforce; formatting belongs to the tools.

Sections: Tooling (strict types; formatter and linter in CI; fix errors, never disable the rule) · Naming table · Structure and size limits · Patterns, each with a 3-5 line code example (data fetching, forms, server actions, errors, dates) · Avoid, each with its reason · Errors · Comments (why, not what) · Git (branch names, Conventional Commits, small PRs).

### 7. docs/TESTING.md

It turns "it should work now" into "the tests pass".

Sections: Layers table (unit, integration, end-to-end: tool, coverage, command) · Must be tested (business logic, every access rule, every P0 flow, every bug fix) · Not worth testing · Conventions (file names; test names state the behaviour and cite the story, e.g. `US-2: rejects an empty title`) · Test data · CI order and what blocks a merge · Definition of done as a checklist.

Rule to include: never change a test just to make it pass. Fix the code; if the test is wrong, say so and get approval.

### 8. AGENTS.md and CLAUDE.md (repo root)

AGENTS.md is a README for AI agents. Most coding agents load it automatically but none load `docs/`, so it tells the agent which doc to open for which task. Keep it under about 120 lines and link to the docs instead of copying them.

Sections: Project (one line + link to the PRD) · Commands (the real ones from the package manifest) · "Read before you work" table mapping task type to doc · Hard rules (5-8 checkable rules) · How to work (restate the task, smallest change, run checks, report, update docs in the same change).

CLAUDE.md is two parts: the line `@AGENTS.md`, then any Claude Code-only notes. Don't import all the docs with `@`; imports load whole files into every session.

Verify: in a fresh session ask "Which docs should you read before adding a new table?" The answer should name DATABASE.md and SECURITY.md.

## After the docs are approved

1. **Check.** Run `python3 <skill-dir>/scripts/check_docs.py <project-root>` and fix every error. Without the script, check by hand: every P0 has a story, every story has criteria, every table has an access rule, AGENTS.md links every doc, and no placeholder text is left.
2. **Plan.** Write docs/PLAN.md: milestones, then a task table `| ID | Task | Feature | Depends on | Status |`. Each task is small enough for one sitting and one reviewable change. Order: setup, then one P0 feature at a time, each as a thin slice that works end to end (schema, logic, UI, tests) before the next starts.
3. **Set up.** Show the "Setup after approval" list and run it with the user's OK, since it adds dependencies and code.
4. **Build**, one task at a time.

## Build loop

For `build <F-id | T-id | next>`:

1. Read AGENTS.md, the task, its feature's stories, and the docs AGENTS.md lists for that kind of work.
2. Restate the task and list the files you will change. On anything touching more than about 3 files, wait for a yes.
3. Write the tests that express the acceptance criteria, then the smallest change that passes them.
4. Run lint, typecheck and tests. Fix failures in the code, not in the tests.
5. Walk the SECURITY.md checklist for what you touched.
6. Mark the task done in PLAN.md and tick the acceptance criteria in the PRD.
7. Report what changed, what you verified, and anything unfinished. If a decision changed, update the doc in the same change.

Stop after each task. Don't start the next one unasked.

## Other modes, in short

- **existing**: read the code first; write each doc from what is there, marking guesses as open questions; then list where the code breaks the doc.
- **status**: a table of doc, status, open questions; then the plan's progress and the next step.
- **audit**: run the checker, then read for what it can't see: vague rules, contradictions between docs, untestable criteria. Report findings by doc with the fix for each.
- **change**: list every doc and section the change touches; update the docs and get approval; add a decision-log line; update PLAN.md; then build.
- **review**: run the checker against the code, then compare by reading. Report as `doc | what it says | what the code does | file:line | fix the doc or the code?`. Change nothing until the user picks.

## Keeping docs alive

An out-of-date doc is worse than none: the agent trusts it and builds the wrong thing.

1. Docs change in the same commit as the code.
2. When the agent repeats a mistake, add one line to the right doc so there's no third time.
3. Specific beats long. Delete rules nobody follows.
4. Open questions stay visible; they don't turn into guesses.
5. Run `review` weekly. It takes ten minutes.
6. Commit the docs to Git so every teammate and every AI tool works from the same rules.
