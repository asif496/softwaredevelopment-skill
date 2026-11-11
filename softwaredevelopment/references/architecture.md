# Architecture guide (docs/ARCHITECTURE.md)

The architecture doc is the map of the code: the stack, the folders, how a request travels, and where things are allowed to live. An agent without it creates a second way of doing everything.

## Before writing

Read the PRD and the design system. Then propose the simplest architecture that ships the P0 features. Fewer moving parts wins; an app with ten users doesn't need microservices, a queue or a cache.

**Show the stack first and wait for the user's OK** before writing the rest. Present it as a small table with a one-line reason per choice, plus the main alternative you rejected and why. The stack is the hardest decision to reverse, and the user may have constraints they haven't mentioned: a host they already pay for, a language they know, a client requirement.

Ask if not already known: what they or their team already know; where it will be hosted; expected number of users in the first months; a budget for paid services.

## Sections

**Stack.** `Layer | Choice (version) | Why`. Layers: framework, language, UI, database, auth, storage, email, hosting, tests. Pin major versions; agents otherwise write code for whichever version they remember. The reasons matter: without them a later session swaps the library.

**System diagram.** Text arrows are enough:

```
Browser -> Next.js on Vercel (Server Components, Server Actions)
                |-> Supabase: Postgres (RLS), Auth, Storage
                |-> Resend: transactional email
```

**Folder structure.** One line per folder with its rule, written as full paths so each line stands alone:

```
src/app/            routes and pages only; no business logic
src/components/ui/  library primitives; never edited by hand
src/lib/db/         every database query lives here and nowhere else
src/lib/services/   business logic as pure functions
src/lib/validation/ schemas shared by client and server
```

**Request flow.** Take the most important user action and number the steps from click to database and back, naming real files. This one worked example teaches the pattern for every other feature.

**External services.** Each service, what it is used for, and what happens if it is down.

**Environments.** Local, preview (per pull request) and production: how each is created and how a deploy happens.

**Decision log.** `YYYY-MM-DD: <decision>, because <reason>`. Add a line whenever a choice is made that someone might later question. It stops settled questions being reopened every session.

**Boundaries.** What may call what: the UI never talks to the database directly; a new third-party service is added to this doc before the code.

## Self-check

- Every stack row has a version and a reason.
- Every PRD feature can be built with this stack with nothing added. If a feature needs something not listed (file upload, email, scheduled jobs), add it now.
- The folder rules say where a new query, a new component and a new piece of logic go.
- The request flow names files that match the folder structure.
- The decision log has at least the stack decision, dated.

## Common mistakes

- A stack with no reasons.
- Folders listed with no rule for what belongs in them.
- No decision log, so the agent re-argues the database choice in session 12.
- Architecture sized for a million users before there are ten.
- Two ways to do the same thing (two fetch helpers, two form libraries) with no rule for which wins.

## Larger projects

For several services or a contested decision, add decision records and an API contract; see `extra-docs.md`.
