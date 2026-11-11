# Database: StudyPlan
Status: approved | Last updated: 2026-11-11

## Entities
auth.users 1--* plans 1--* tasks

Users are managed by Supabase Auth; there is no users table of our own in v1.

## Conventions
- Table names are snake_case and plural.
- Every table has `id` (uuid, primary key), `created_at` and `updated_at` (timestamp with time zone).
- Foreign keys are named `<table>_id`. Cascade deletes only where stated below.
- Timestamps are stored in UTC. Due dates and exam dates are plain dates with no time.

## Tables

### Table: plans
| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key, default gen_random_uuid() |
| user_id | uuid | no | references auth.users(id), on delete cascade |
| title | text | no | 1-80 characters (check constraint) |
| exam_date | date | yes | |
| created_at | timestamptz | no | default now() |
| updated_at | timestamptz | no | default now(), set by trigger |

Indexes: (user_id, created_at desc), serves the dashboard's plan list.

### Table: tasks
| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key, default gen_random_uuid() |
| plan_id | uuid | no | references plans(id), on delete cascade |
| title | text | no | 1-120 characters (check constraint) |
| due_date | date | yes | |
| is_done | boolean | no | default false |
| completed_at | timestamptz | yes | set when is_done becomes true |
| created_at | timestamptz | no | default now() |
| updated_at | timestamptz | no | default now(), set by trigger |

Indexes: (plan_id, due_date), serves the plan page and the "due in the next 7 days" list.

## Access rules
Row Level Security is on for every table.

| Table | Select | Insert | Update | Delete |
|---|---|---|---|---|
| plans | owner (user_id = auth.uid()) | owner | owner | owner |
| tasks | owner of the parent plan | owner of the parent plan | owner of the parent plan | owner of the parent plan |

Nothing is readable by anonymous users.

## Migrations
- Every schema change is a new file in `supabase/migrations/`. Never edit the schema by hand in the dashboard.
- File names: `YYYYMMDDHHMM_short_description.sql`.
- Never drop or rename a column in one step: add the new one, backfill, switch the code, drop the old one later.
- Test with `npx supabase db reset` before pushing.

## Seed data
`supabase/seed.sql` creates one test user with 2 plans and 6 tasks: 2 done, 1 overdue, 3 due this week.

## Deletion and retention
Deleting an account deletes the auth user; plans and tasks go with it through the cascades, immediately. Nothing is kept. There is no soft delete in v1.

## Open questions
None.
