# AGENTS.md

## Project
StudyPlan is a study planner for university students preparing for several exams. Full spec: docs/PRD.md

## Commands
- Install: `npm install`
- Run locally: `npm run dev` (http://localhost:3000)
- Test: `npm test`
- Database tests: `npm run test:db`
- End-to-end tests: `npm run test:e2e`
- Lint + types: `npm run lint && npm run typecheck`
- Build: `npm run build`

## Read before you work
| Task | Read first |
|---|---|
| New feature or change in behaviour | docs/PRD.md |
| Any UI or styling | docs/DESIGN_SYSTEM.md |
| New module, route, service or folder | docs/ARCHITECTURE.md |
| Schema, queries or migrations | docs/DATABASE.md |
| Auth, user data, any server action | docs/SECURITY.md |
| Writing any code | docs/CODE_STYLE.md |
| Before saying a task is done | docs/TESTING.md |
| Choosing what to build next | docs/PLAN.md |

## Hard rules
- Never commit secrets. Env variables live in `.env.local`, which is gitignored.
- No schema change without a migration file in `supabase/migrations/`.
- No new dependency without asking.
- Never disable or delete a failing test to make a build pass.
- Every table has RLS policies; see docs/DATABASE.md.
- All Supabase queries go through `src/lib/db/`.
- Colours and spacing come from the tokens in docs/DESIGN_SYSTEM.md, never hard-coded.

## How to work
1. Restate the task and list the files you will change.
2. Make the smallest change that does the job.
3. Run lint, typecheck and tests. Fix what fails.
4. Report what changed and anything you could not finish.
5. If a decision changes a doc, update that doc in the same change.
