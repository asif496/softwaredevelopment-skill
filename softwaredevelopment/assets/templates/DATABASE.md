# Database: {{APP_NAME}}
Status: draft | Last updated: {{DATE}}

## Entities
<user 1--* thing 1--* child>

## Conventions
- Table names are snake_case and plural.
- Every table has `id` (uuid, primary key), `created_at` and `updated_at` (timestamp with time zone).
- Foreign keys are named `<table>_id`. Cascade deletes only where stated below.
- Money is an integer in the smallest currency unit, never a float.
- Timestamps are stored in UTC.

## Tables

### Table: <table_name>
| Column | Type | Null | Notes |
|---|---|---|---|
| id | uuid | no | primary key, generated |
| <column> | <type> | <yes/no> | <constraint, default, reference and on-delete behaviour> |
| created_at | timestamptz | no | default now() |
| updated_at | timestamptz | no | default now() |

Indexes: <columns>, serves <which query>.

## Access rules
| Table | Select | Insert | Update | Delete |
|---|---|---|---|---|
| <table_name> | <who> | <who> | <who> | <who> |

Nothing is readable by anonymous users.

## Migrations
- Every schema change is a new migration file in <folder>. Never edit the schema by hand in a dashboard.
- File names: <pattern, e.g. YYYYMMDDHHMM_short_description.sql>
- Never drop or rename a column in one step: add the new one, backfill, switch the code, drop the old one later.
- Test with <local reset command> before pushing.

## Seed data
<What the local seed creates.>

## Deletion and retention
<What is deleted when a user deletes their account, how quickly, and what is kept.>

## Open questions
- [ ] <question>
