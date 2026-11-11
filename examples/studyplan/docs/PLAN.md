# Build plan: StudyPlan
Status: approved | Last updated: 2026-11-11

## Milestones
- M0 Setup: the project runs locally, checks pass, CI is green.
- M1 Sign in and plans: a student can sign in and manage plans.
- M2 Tasks and dashboard: a student can track tasks and see what is due.

## Tasks
Status is todo, doing, done or cut. Never renumber; append new tasks.

| ID | Task | Feature | Depends on | Status |
|---|---|---|---|---|
| T1 | Scaffold Next.js; Prettier, ESLint, TypeScript strict; CI workflow | setup | - | todo |
| T2 | Tailwind tokens from the design system and a /styleguide page | setup | T1 | todo |
| T3 | Vitest and Playwright with one passing test per layer | setup | T1 | todo |
| T4 | First migration: plans and tasks with RLS policies; seed data | setup | T1 | todo |
| T5 | Sign-in page with email and Google; `requireUser()`; middleware redirect | F1 | T2, T3 | todo |
| T6 | Create a plan: schema, db query, server action, form, tests | F2 | T4, T5 | todo |
| T7 | Edit and delete a plan with a confirmation dialog | F2 | T6 | todo |
| T8 | Add, complete and delete tasks on the plan page; "Overdue" label | F3 | T6 | todo |
| T9 | Dashboard: plan list, tasks due in 7 days, empty state | F4 | T8 | todo |
| T10 | RLS tests: user A cannot read or change user B's plans or tasks | F2, F3 | T4, T3 | todo |
| T11 | Delete account from Settings | F1 | T5 | todo |

## Setup after approval
- [ ] /styleguide page (T2)
- [ ] First migration and policies (T4)
- [ ] Lint, type and test tooling (T1, T3)
