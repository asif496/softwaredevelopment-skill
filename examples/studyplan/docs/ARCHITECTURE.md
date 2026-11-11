# Architecture: StudyPlan
Status: approved | Last updated: 2026-11-11

## Stack
| Layer | Choice (version) | Why |
|---|---|---|
| Framework | Next.js 15, App Router | Pages and server logic in one project; one deploy |
| Language | TypeScript 5, strict | Catches mistakes before they run |
| UI | Tailwind CSS 4 + shadcn/ui | Tokens map to CSS variables; accessible primitives |
| Database and auth | Supabase (Postgres 15, Auth) | Row Level Security and Google sign-in without a custom backend |
| Validation | Zod 3 | One schema shared by forms and server actions |
| Hosting | Vercel | A preview URL for every pull request |
| Tests | Vitest 3 + Playwright | Fast unit tests; real-browser flows |

## System diagram
```
Browser -> Next.js on Vercel (Server Components, Server Actions)
                |-> Supabase: Postgres (RLS), Auth
```

## Folder structure
```
src/app/              routes and pages only; no business logic
src/components/ui/    shadcn/ui primitives; never edited by hand
src/components/       app components, one per file
src/lib/db/           every Supabase query lives here and nowhere else
src/lib/services/     business logic as pure functions (overdue rules, sorting)
src/lib/validation/   Zod schemas shared by client and server
src/types/            shared TypeScript types
supabase/migrations/  SQL migrations; never edit the schema in the dashboard
e2e/                  Playwright tests, one file per flow
```

## Request flow: create a plan
1. The form in `src/components/PlanForm.tsx` validates with `planSchema` from `src/lib/validation/plan.ts`.
2. It calls the server action `createPlan` in `src/app/plans/actions.ts`.
3. The action checks the session, validates the input again, and calls `insertPlan` in `src/lib/db/plans.ts`.
4. Postgres applies the RLS policy, so the row is written only for the signed-in user.
5. The action returns `{ ok: true, data }` and revalidates the dashboard path, so the list updates without a reload.

## External services
- Supabase: database and sign-in. If it is down, pages show "We can't reach the server. Try again." and nothing is cached locally in v1.

## Environments
- Local: `npm run dev` against a local Supabase started with the Supabase CLI.
- Preview: Vercel creates one per pull request, pointed at the staging Supabase project.
- Production: merging to `main` deploys to Vercel; migrations run from CI before the deploy.

## Decision log
- 2026-11-11: Supabase instead of a custom API, because the app is CRUD with per-user data and RLS covers the access rules.
- 2026-11-11: Server Actions instead of REST routes, because nothing outside this app calls the backend.
- 2026-11-11: No client state library, because server components and URL state cover v1.

## Boundaries
- The UI never talks to Supabase directly; it goes through `src/lib/db/`.
- Server actions are the only place that writes data.
- A new third-party service is added to this doc before the code.

## Open questions
None.
