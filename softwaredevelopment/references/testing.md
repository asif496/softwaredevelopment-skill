# Testing guide (docs/TESTING.md)

The testing doc says what gets tested, with which tools, where the tests live, and what "done" means. It turns the agent's "it should work now" into "the tests pass", and tests are how the agent catches its own mistakes before the user does.

## Before writing

Read the PRD (stories and acceptance criteria become tests), ARCHITECTURE.md (which layers exist), DATABASE.md (every access rule needs a test) and SECURITY.md (the checklist is part of "done"). Choose tools that fit the stack; see `project-types.md`.

## Sections

**Layers.** `Layer | Tool | What it covers | Command`:

- Unit: business logic and validation. Fast, no network, no database.
- Integration: database queries and access rules against a local database.
- End-to-end: the P0 user flows in a real browser or against the running API.

Every command must be one the project really has. If the test script doesn't exist yet, put it on the setup list.

**Must be tested.**
- Every function in the business-logic and validation layers.
- Every access rule: user A cannot read or change user B's rows.
- Every P0 flow end to end (for example: sign up, create a plan, complete a task, delete the account).
- Every bug fix: a test that failed before the fix.

**Not worth testing.** UI library primitives, plain layout, third-party internals. Saying this stops the agent padding the suite with tests that assert a button renders.

**Conventions.**
- Unit tests sit beside the file: `plan-utils.ts` and `plan-utils.test.ts`.
- End-to-end tests live in `e2e/`, one file per flow.
- Test names state the behaviour and cite the story: `US-2: rejects an empty title`. That makes it possible to see which stories have no test.
- No real network calls in unit tests; mock at the boundary.

**Test data.** Factories (`makeUser`, `makePlan`) instead of hand-written objects. End-to-end tests run against a local database reset from the seed.

**CI.** The order, and that each step blocks the merge: lint, typecheck, unit, integration, build, end-to-end on the preview deploy.

**Definition of done.** A checklist:

- [ ] The acceptance criteria in docs/PRD.md are met.
- [ ] New logic has tests, and all tests pass locally.
- [ ] Lint and typecheck are clean.
- [ ] The checklist in docs/SECURITY.md has been walked for what changed.
- [ ] Docs are updated if a decision changed.

**Bug fixes.** Write the failing test first, then the fix.

**Rule to include.** Never change a test just to make it pass. Fix the code. If the test itself is wrong, say so and get approval before changing it.

## Self-check

- Every P0 story maps to at least one named test or flow.
- Every table in DATABASE.md has an access test listed.
- Every command exists, or is on the setup list.
- The definition of done is short and every line is checkable.

## Common mistakes

- Letting the agent edit a test until it passes.
- No tests for access rules, which is where the worst bugs are.
- No definition of done, so "done" means whatever the agent says.
- Only end-to-end tests: slow, flaky, and they don't say what broke.
- A coverage percentage as the goal instead of the behaviours that matter.

## Setup after approval

Install the tools, one passing example test per layer, one access test per table, and the CI workflow.
