# Database guide (docs/DATABASE.md)

The database doc is the schema in plain words, plus the rules for changing it and for who may read or write each table. Code can be rewritten; lost or leaked data can't be taken back. This is where an agent needs the strictest rules.

## Before writing

Read the PRD (features, roles, sensitive data) and the architecture doc (which database, which auth). Design only the tables the P0 features need. A column for a P2 feature is a guess that will be wrong by the time P2 arrives.

Ask if unclear: what happens to a user's data when they delete their account; whether anything must be kept for legal or audit reasons; whether any record is shared between users.

## Sections

**Entities.** Relationships in one line: `user 1--* plan 1--* task`.

**Conventions.**
- Table names: snake_case, plural.
- Every table has `id` (uuid primary key), `created_at` and `updated_at` (timestamp with time zone).
- Foreign keys are named `<table>_id`. Cascade deletes only where this doc says so.
- Money is an integer in the smallest unit (cents, paise, poisha), never a float. Store the currency code beside it if there can be more than one.
- Timestamps are stored in UTC and converted for display.
- Enumerated values are a check constraint or an enum type, with the allowed values listed.

**Tables.** One block per table under the heading `### Table: <name>` (the checker looks for that form):

```
### Table: plans
| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key, default gen_random_uuid() |
| user_id | uuid | no | references auth.users(id), on delete cascade |
| title | text | no | 1-80 characters |
| status | text | no | 'active' or 'archived', default 'active' |

Indexes: (user_id, created_at desc), serves the dashboard list.
```

Every index names the query it serves. An index nobody can justify is removed.

**Access rules.** A table of who may select, insert, update and delete each table. On Postgres with Row Level Security: RLS is on for every table; users touch only rows they own; child rows are allowed only through ownership of the parent; nothing is readable anonymously unless the PRD says so. On other stacks, state where the same check is enforced (see `project-types.md`), and make it one place, not every caller.

**Migrations.** Every schema change is a new migration file, never a manual edit in a dashboard, because then the files stop matching reality. Timestamped names (`202611111530_add_plans.sql`). Never drop or rename a column in one step: add the new one, backfill, switch the code, drop the old one later. Test with a local reset before pushing.

**Seed data.** What the local seed creates, so tests and screenshots have something to show: one test user, a few records in each state.

**Deletion and retention.** What is deleted when a user deletes their account, how quickly, and what (if anything) is kept and why. Soft delete only if a feature needs it; say which tables.

## Self-check

- Every table has a row in Access rules.
- Every foreign key says what happens on delete.
- Every piece of data a P0 story reads or writes has a column. List anything in the PRD the schema can't support yet.
- No float is used for money; no timestamp lacks a time zone.
- Sensitive columns named in the PRD are identified, so SECURITY.md can cover them.

## Common mistakes

- No access rules, so any signed-in user can read every row.
- Editing the schema by hand in a dashboard.
- Renaming a column in one step and breaking the running app.
- Tables for features nobody has asked for yet.
- A `status` text column with no list of allowed values.

## Setup after approval

The first migration file, the access policies, and the seed script.
