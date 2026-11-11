# Project sizes, types and stacks

The eight docs describe a web app with accounts and a database. Real projects vary. This file says how to shrink, reshape and translate the docs so they fit the project instead of the other way round.

Contents: Sizes · Types · Stack translation · Choosing a stack

## Sizes

| Size | Signals | What to write |
|---|---|---|
| lite | One person, 1-3 features, days of work, no accounts | A one-page PRD and an AGENTS.md that carries the rules inline. Add SECURITY.md if it handles personal data, secrets or other people's systems. Add DATABASE.md if it has its own tables. |
| standard | Accounts, a database, weeks of work | All 8 docs and PLAN.md, about a page each. |
| large | A team, payments or regulated data, several services, or a public API | All 8 and PLAN.md, plus the extras in `extra-docs.md` that apply. Docs run longer; AGENTS.md still stays under 120 lines. |

When unsure between two sizes, choose the smaller. Docs can grow with the app; a pile of unread docs helps nobody.

## Types

Record the type in the PRD header. Docs not mentioned stay as they are.

### web

The default. All docs as written.

### mobile

- PRD: add supported OS versions, offline behaviour, push notifications, and app-store requirements (privacy labels, account deletion inside the app).
- DESIGN_SYSTEM: follow the platform's conventions (navigation patterns, safe areas, system font sizes); tap targets at least 44x44 pt on iOS and 48x48 dp on Android.
- ARCHITECTURE: state management, navigation, local storage and sync, how releases and over-the-air updates work.
- SECURITY: tokens in the platform's secure storage (Keychain, Keystore), never in plain preferences; nothing secret is shipped inside the app binary.
- TESTING: widget or component tests, integration tests on an emulator, and a short manual checklist per release for real devices.

### api (backend service with no screens)

- Skip DESIGN_SYSTEM. Add `docs/API.md` (see `extra-docs.md`); it plays the role the design system plays for a UI.
- PRD: "Screens" becomes "Interfaces": the endpoints or events, and who the consumers are.
- SECURITY: authentication method per endpoint (API key, OAuth, JWT), per-key rate limits, and how keys are issued and revoked.
- TESTING: contract tests for every endpoint, including the error responses.

### cli (command-line tool or library)

- Skip DESIGN_SYSTEM and usually DATABASE.
- PRD: "Screens" becomes the commands or the public functions, each with an example call and its output.
- ARCHITECTURE: supported runtime versions, how it is packaged and published, and the versioning policy (what counts as a breaking change).
- CODE_STYLE: the public API naming rules, and that nothing public changes without a changelog entry.
- TESTING: examples in the README are run as tests.

### automation (workflows between systems: CRM, forms, email, spreadsheets, n8n, Make, Zapier, custom scripts)

- Skip DESIGN_SYSTEM unless there is a UI.
- PRD: features are workflows. Each story names the trigger, the systems touched and the result: "When a deal moves to Closed Won in the CRM, an invoice draft is created in the billing tool within 5 minutes."
- ARCHITECTURE: a diagram of the systems; for each workflow the trigger, steps and failure path; how retries work; how duplicates are prevented when a trigger fires twice (a dedupe key); where failed runs go and who is told.
- DATABASE becomes a data map: for each object (contact, deal, invoice) which system is the source of truth, the field-by-field mapping between systems, required fields, and the key used to match records. Keep the file name so other docs' links still work.
- SECURITY: one credential per integration with the least access it needs; where credentials are stored; webhook signatures are verified; which personal data crosses between systems.
- CODE_STYLE: naming for workflows, steps and custom fields; every workflow is exported to Git; no logic hidden in a tool's UI without a note in the docs.
- TESTING: a sandbox or test account for each system, a set of test records, how to replay a failed run, and a checklist to run before switching a workflow on in production.

### ai (the product is built around a language model)

- PRD: say what the model does and what it must never do; how wrong it is allowed to be; what the user sees when it fails or is slow.
- ARCHITECTURE: provider and model; where prompts live (in the repo, versioned); what context the model gets and from where; budgets for cost per request and response time.
- SECURITY: add the AI section from `security.md`.
- TESTING: a set of example inputs with the expected behaviour, run whenever a prompt or model changes. Prompts are code: they are reviewed and tested like code.

## Stack translation

The templates use the first column. Translate the idea, not the wording.

| Idea | Next.js + Supabase | Django / DRF | FastAPI + SQLAlchemy | Laravel | Express + MongoDB | Flutter + Firebase |
|---|---|---|---|---|---|---|
| Per-row access rules | Row Level Security policies | `get_queryset()` filtered by `request.user`, plus permission classes | A current-user dependency, and every query filtered by owner | Policies and Gates; global scopes | Auth middleware, and every query includes the owner id | Firestore Security Rules |
| Schema changes | SQL files in `supabase/migrations` | `makemigrations` / `migrate` | Alembic revisions | `php artisan make:migration` | A migration tool such as migrate-mongo, or versioned documents | No migrations; document the shape and version each collection |
| Input validation | Zod schemas shared by client and server | Serializers / forms | Pydantic models | Form Requests | Zod or Joi in the route layer | Validation in the app, enforced again in Security Rules |
| Unit / integration tests | Vitest | pytest-django | pytest + httpx | Pest or PHPUnit | Vitest or Jest + Supertest | `flutter_test`; rules tested on the Firebase emulator |
| End-to-end tests | Playwright | Playwright | Playwright, or contract tests for an API | Laravel Dusk or Playwright | Playwright | `integration_test` |
| Lint and format | ESLint + Prettier | Ruff | Ruff | Pint + Larastan | ESLint + Prettier | `dart analyze` + `dart format` |
| Strict types | TypeScript `strict` | mypy or pyright | mypy or pyright | PHPStan level, typed properties | TypeScript `strict` | Dart sound null safety |
| Secrets | `.env.local` + host settings; only `NEXT_PUBLIC_*` reach the browser | `.env` + host settings | `.env` + host settings | `.env`; never commit it | `.env` + host settings | Server-side keys in Cloud Functions config; nothing secret in the app |

Whatever the stack, the rule behind "per-row access rules" is the same: the check lives in one enforced place, and a test proves user A can't reach user B's data.

## Choosing a stack

When the user has no preference, propose one and give the reason in a line. In order of weight:

1. What the user or their team already knows. A familiar stack beats a better one they can't debug.
2. What the P0 features need (real-time, offline, heavy background jobs, native device features).
3. What the host and budget allow.
4. How well coding agents know it. Widely used stacks get more reliable code.

Then pin the major versions in ARCHITECTURE.md.
