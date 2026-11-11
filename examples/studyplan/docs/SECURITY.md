# Security: StudyPlan
Status: approved | Last updated: 2026-11-11

## Data we hold
| Data | Sensitivity | Where stored |
|---|---|---|
| Email address, Google profile name | Medium (personal data) | Supabase Auth |
| Plans and tasks | Low, but private to the user | Supabase Postgres |

Never stored: passwords (Supabase Auth holds only hashes), payment data (there are no payments).

## Roles
| Role | Can do | Enforced by |
|---|---|---|
| anonymous | See the landing and sign-in pages | Middleware redirect + RLS |
| user | Read and write their own plans and tasks; delete their own account | RLS policies + session check in every server action |

There is no admin role in v1.

## Auth and sessions
- Provider: Supabase Auth with email + password and Google. Sessions live in httpOnly, secure cookies.
- Every server action and protected page calls `requireUser()` first.
- Authorization is decided on the server and in RLS, never by hiding a button.

## Secrets
- Secrets live only in `.env.local` (gitignored) and Vercel's environment settings.
- Only `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` reach the browser.
- `SUPABASE_SERVICE_ROLE_KEY` is used by one server action (delete account) and is never imported from a client file.
- If a secret is committed: rotate it first, then remove it.

## Input and output
- Every input is validated on the server with the Zod schemas in `src/lib/validation/`, even if the client already validated.
- Queries go through the Supabase client; no SQL is built from strings.
- Uploads: none in v1.

## Abuse
- Rate limits: sign-in and sign-up, 5 attempts per minute per IP; password reset, 3 per hour per email.
- Limits per user: 50 plans, 200 tasks per plan, enforced in the server actions.

## Dependencies
- No new package without approval. It must be maintained and widely used.
- `npm audit` runs in CI. High and critical findings are fixed before merging.

## Logging
- Errors are logged with a request id.
- Never log passwords, tokens, keys or full email addresses.

## Abuse cases
- F1: what if someone tries thousands of passwords? The sign-in rate limit, and the same error text for a wrong email and a wrong password.
- F2: what if a user changes the plan id in the URL to someone else's? RLS returns no row and the page shows "Plan not found".
- F3: what if a user posts a task with another user's plan id? The insert policy checks ownership of the parent plan and rejects it.
- F4: what if a user creates 100,000 tasks to slow the dashboard? The per-plan limit, and the dashboard query is capped at 50 rows.

## Pre-merge checklist
- [ ] A01 Access control: can user A read or change user B's data?
- [ ] A02 Misconfiguration: RLS is on for any new table; no debug output in production.
- [ ] A03 Supply chain: new dependencies approved and audited.
- [ ] A04 Cryptography: no secrets in code, logs or client bundles.
- [ ] A05 Injection: all input validated server-side; no raw SQL.
- [ ] A06 Design: the feature's abuse case is written above and handled.
- [ ] A07 Authentication: `requireUser()` is called in every new action and protected page.
- [ ] A09 Logging: failures are logged with a request id and no secrets.
- [ ] A10 Errors: fail closed; no stack traces shown to users.

## Open questions
None.
