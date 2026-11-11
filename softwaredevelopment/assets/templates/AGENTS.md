# AGENTS.md

## Project
{{APP_NAME}} is a <one line: what it does> for <who>. Full spec: docs/PRD.md

## Commands
- Install: <command>
- Run locally: <command> (<URL>)
- Test: <command>
- Lint + types: <command>
- Build: <command>

## Read before you work
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

## Hard rules
- Never commit secrets. Env variables live in <gitignored env file>.
- No schema change without a migration file.
- No new dependency without asking.
- Never disable or delete a failing test to make a build pass.
- <Another checkable rule taken from the docs>

## How to work
1. Restate the task and list the files you will change.
2. Make the smallest change that does the job.
3. Run lint, typecheck and tests. Fix what fails.
4. Report what changed and anything you could not finish.
5. If a decision changes a doc, update that doc in the same change.
