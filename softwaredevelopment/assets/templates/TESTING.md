# Testing: {{APP_NAME}}
Status: draft | Last updated: {{DATE}}

## Layers
| Layer | Tool | What it covers | Command |
|---|---|---|---|
| Unit | <tool> | <business logic, validation, utilities> | <command> |
| Integration | <tool> | <database queries and access rules> | <command> |
| End-to-end | <tool> | The P0 user flows from docs/PRD.md | <command> |

## Must be tested
- Every function in <business logic and validation folders>.
- Every access rule: user A cannot read or change user B's rows.
- Every P0 flow end to end: <list the flows>.
- Every bug fix: a test that failed before the fix.

## Not worth testing
- <UI library primitives, plain layout, third-party internals>

## Conventions
- Unit tests sit next to the file: <example pair of file names>.
- End-to-end tests live in <folder>, one file per flow.
- Test names state the behaviour and cite the story: `US-2: rejects an empty title`.
- No real network calls in unit tests; mock at the boundary.
- Never change a test just to make it pass. Fix the code; if the test is wrong, say so and get approval.

## Test data
- Factories in <file> (<factory names>).
- End-to-end tests run against <a local database reset with the seed>.

## CI (blocks merge)
<lint -> typecheck -> unit -> integration -> build -> end-to-end on the preview deploy>

## Definition of done
- [ ] Acceptance criteria from docs/PRD.md are met.
- [ ] New logic has tests; all tests pass locally.
- [ ] Lint and typecheck are clean.
- [ ] The checklist in docs/SECURITY.md has been walked.
- [ ] Docs are updated if a decision changed.

## Open questions
- [ ] <question>
