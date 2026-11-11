# Modes

Steps for every command other than the full flow.

Contents: existing · status · audit · plan · build · change · review

## existing

For a project that already has code and few or no docs. The goal is docs that describe what is there, plus a list of where the code falls short of its own rules.

1. Explore before asking anything: the manifest and lockfile, folder tree, routes, migrations or models, auth code, tests, CI config, the README, and recent commit messages.
2. Tell the user what you found in a few lines (stack, size, what it seems to do) and ask only what the code can't answer: who the users are, what is in progress, what is known to be broken, what must not change.
3. Write the docs in the usual order, one at a time with review. Derive each from the code:
   - PRD: features that exist (mark them `shipped`), in progress, and wanted. Non-goals come from the user.
   - DESIGN_SYSTEM: the tokens and components actually in use. Where the code is inconsistent, list the variants and ask which one wins.
   - ARCHITECTURE: the real stack with versions from the lockfile, the real folders, and a request traced through real files.
   - DATABASE: the schema as it is in the migrations or models, and the access rules that exist. A table with no rule is a finding, not something to paper over.
   - SECURITY, CODE_STYLE, TESTING: the rules the project should follow, then how the code measures up.
4. Mark anything you inferred but couldn't confirm as an open question.
5. After each doc, add a "Gaps" list: places the code breaks the doc, with file and line. Don't fix them yet.
6. At the end, turn the gaps into tasks in docs/PLAN.md, ordered by risk: access control and leaked secrets first.

## status

Read-only. Show:

1. A table of `Doc | Status | Last updated | Open questions`.
2. If PLAN.md exists: tasks done, in progress and remaining, and the next task.
3. One line saying what to do next ("Approve DATABASE.md, then I'll write SECURITY.md").

`check_docs.py` prints the first table.

## audit

Read-only. Answers "are these docs good enough to build from?"

1. Run `python3 <skill-dir>/scripts/check_docs.py <project-root>` and include its errors and warnings.
2. Then read the docs for what a script can't see:
   - Rules nobody could check ("handle errors gracefully").
   - Contradictions between docs: a feature in the PRD with no table to store it; a library in CODE_STYLE that isn't in the ARCHITECTURE stack; a role in SECURITY that the PRD never mentions.
   - Acceptance criteria that can't be tested.
   - P0 features with no abuse case in SECURITY.md.
   - AGENTS.md commands that don't exist in the manifest.
   - Decisions with no reason given.
3. Report by doc: a one-word verdict (`ready`, `needs work`, `missing`) and the findings, each with the exact fix. Most serious first.
4. Offer to apply the fixes. Change nothing until the user says so.

## plan

Writes or refreshes docs/PLAN.md. Needs an approved PRD and architecture at least.

1. Milestones: M0 setup, then one milestone per group of P0 features that makes something usable, then P1.
2. Tasks: `| ID | Task | Feature | Depends on | Status |`. Status is `todo`, `doing` or `done`.
3. Slice vertically. A task delivers a thin piece that works end to end (the migration, the query, the logic, the UI, the tests) and not "all the tables" then "all the screens". Vertical slices can be shown and tested after each task; horizontal layers can't be tested until the last one lands.
4. Size: one sitting, one reviewable change, roughly under 400 changed lines. Split anything bigger.
5. The first tasks are always the setup list: project scaffold, lint and type config, test tools with one passing test per layer, first migration with access policies, CI.
6. When refreshing, keep existing IDs and statuses; append new tasks; never renumber.

## build

`build F2` builds every remaining task for that feature in order, stopping after each. `build T7` builds one task. `build next` takes the first `todo` task whose dependencies are done.

Before starting, check the docs it depends on are `approved`. If one is still `draft`, say so and ask whether to proceed.

1. Read AGENTS.md, the task, the stories for its feature, and the docs AGENTS.md lists for that kind of work.
2. Restate the task and list the files you'll change. For changes touching more than about 3 files, wait for a yes.
3. Set the task to `doing`.
4. Write tests that express the acceptance criteria, named with the story ID. Then write the smallest change that passes them.
5. Run lint, typecheck and tests. Fix failures in the code. If a test is wrong, say so and ask.
6. Walk the SECURITY.md checklist for what you touched.
7. Set the task to `done`; tick the acceptance criteria it satisfies in the PRD.
8. Report: what changed, what you ran and the result, what you couldn't finish. If you made a decision the docs don't cover, add it to the relevant doc and the decision log in the same change.

If the task turns out to need something the docs forbid or don't mention (a new dependency, a schema change, a new service), stop and ask. That is a `change`.

## change

For a new feature, a changed requirement or a reversed decision after the docs are approved. Docs first, then code.

1. Restate the change in one or two lines.
2. Impact table: `Doc | Section | What changes`. Walk every doc: a new feature usually touches the PRD (feature, stories), DATABASE (tables, access rules), SECURITY (abuse case), TESTING (what must be tested), and sometimes DESIGN_SYSTEM and ARCHITECTURE.
3. Point out conflicts with non-goals, the P0 limit or earlier decisions, and what it costs: migrations, rework, new dependencies.
4. On approval, update the docs. New features get the next free ID. Add a decision-log line with today's date and the reason.
5. Update PLAN.md: new tasks, and any existing tasks that are now obsolete marked `cut`.
6. Run the checker.
7. Build through the normal loop.

For a reversed decision, find everything built on the old one (search the code and the docs) and list it before changing anything.

## review

The weekly drift check. Read-only until the user decides.

1. Run `python3 <skill-dir>/scripts/check_docs.py <project-root>`; with code present it also compares commands, tables and folders against the repository.
2. Then compare by reading, doc by doc:
   - PRD: features in the code that aren't in the PRD, and the reverse.
   - DESIGN_SYSTEM: hard-coded colours or spacing; components with missing states.
   - ARCHITECTURE: dependencies not in the stack table; code in the wrong folder; database calls outside the database layer.
   - DATABASE: tables or columns in the migrations that the doc doesn't have; tables with no access rule.
   - SECURITY: routes with no session check; secrets or service keys reachable from client code.
   - CODE_STYLE: a second library for a job that already has one; files far over the size limit.
   - TESTING: P0 stories with no test; skipped or deleted tests.
3. Report as a table: `Doc | What it says | What the code does | Where (file:line) | Fix the doc or the code?` with your recommendation for each.
4. Wait for the user's choice per row, then apply the fixes. Doc fixes update `Last updated`; code fixes go through the build loop.
5. If the same kind of drift shows up twice, propose a one-line rule for the right doc or for AGENTS.md's hard rules.
