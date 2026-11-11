# Testing: StudyPlan
Status: approved | Last updated: 2026-11-11

## Layers
| Layer | Tool | What it covers | Command |
|---|---|---|---|
| Unit | Vitest | src/lib/services, src/lib/validation | npm test |
| Integration | Vitest + local Supabase | src/lib/db queries and RLS policies | npm run test:db |
| End-to-end | Playwright | The P0 user flows from docs/PRD.md | npm run test:e2e |

## Must be tested
- Every function in `src/lib/services/` and `src/lib/validation/`.
- Every RLS policy: user A cannot read or change user B's plans or tasks.
- Every P0 flow end to end: sign up (US-1), create a plan (US-2), complete a task (US-3), see the dashboard (US-4), delete the account.
- Every bug fix: a test that failed before the fix.

## Not worth testing
- shadcn/ui components, plain layout, third-party library internals.

## Conventions
- Unit tests sit next to the file: `plan-utils.ts` and `plan-utils.test.ts`.
- End-to-end tests live in `e2e/`, one file per flow: `e2e/create-plan.spec.ts`.
- Test names state the behaviour and cite the story: `US-2: rejects an empty title`.
- No real network calls in unit tests; mock at the boundary.
- Never change a test just to make it pass. Fix the code; if the test is wrong, say so and get approval.

## Test data
- Factories in `tests/factories.ts` (makeUser, makePlan, makeTask).
- End-to-end tests run against a local Supabase reset with `supabase/seed.sql`.

## CI (blocks merge)
lint -> typecheck -> unit -> integration -> build -> end-to-end on the preview deploy.

## Definition of done
- [ ] Acceptance criteria from docs/PRD.md are met.
- [ ] New logic has tests; all tests pass locally.
- [ ] Lint and typecheck are clean.
- [ ] The checklist in docs/SECURITY.md has been walked.
- [ ] Docs are updated if a decision changed.

## Open questions
None.
