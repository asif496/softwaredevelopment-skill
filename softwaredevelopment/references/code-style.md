# Code style guide (docs/CODE_STYLE.md)

The code style doc is the house rules: naming, file layout, patterns to use and patterns to avoid. It makes code from session 30 read like code from session 1, and stops the agent mixing three ways of doing the same thing.

Write only rules a linter or formatter can't enforce. Spaces, quotes and semicolons belong to the tools; this doc says "run them" and moves on.

## Before writing

Read ARCHITECTURE.md. If code exists, read a few representative files first and write down the conventions already in use; a style doc that contradicts the codebase gets ignored. Where the code is inconsistent, pick one way, say so, and list the files that need to change.

## Sections

**Tooling.** The strictest type settings the language offers (TypeScript `strict`, no `any`; use `unknown` and narrow it). Formatter and linter run on save and in CI. Fix lint errors; never disable the rule without a comment saying why.

**Naming.** `Thing | Style | Example` for component files, other files, functions and variables (verbs for functions), constants, types, booleans (`is`/`has`/`can` prefix), database names.

**Structure.** One component per file. Files under about 200 lines and functions under about 40; split when bigger. Functions do one thing. Framework defaults (for example, server components unless client-side code is needed). Database access only through the database layer named in ARCHITECTURE.md.

**Patterns.** One approved way for each recurring job, each with a 3-5 line example. A rule with no example is read differently every session.

- Data fetching
- Forms (form library plus the shared validation schema)
- Server actions or endpoints: one result shape, such as `{ ok: true, data } | { ok: false, error }`, instead of throwing to the UI
- Error handling
- Dates (one library; store UTC, display in the user's time zone)

```ts
// Server action: validate, check session, call the db layer, return a result
export async function createPlan(input: unknown): Promise<Result<Plan>> {
  const parsed = planSchema.safeParse(input);
  if (!parsed.success) return { ok: false, error: "Title is required" };
  const user = await requireUser();
  return { ok: true, data: await insertPlan(user.id, parsed.data) };
}
```

**Avoid.** Each with its reason:
- A new state, CSS or date library: one of each is already chosen.
- Copy-pasted logic: search for an existing helper first.
- Magic numbers: name them as constants.
- Commented-out code: Git remembers it.

**Errors.** The user sees a friendly, specific message. The technical detail is logged with the request id.

**Comments.** Explain why, not what. A comment that repeats the code is deleted.

**Git.** Branch names (`feat/plan-sharing`, `fix/login-redirect`). Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`). One pull request is one change, ideally under 400 lines.

## Self-check

- Every pattern has a code example in the project's real language and libraries.
- Every "avoid" has a reason.
- No rule duplicates what the formatter or linter already enforces.
- The naming table covers files, since file names are where agents drift first.
- Nothing contradicts ARCHITECTURE.md's folder rules.

## Common mistakes

- 300 lines of formatting rules a tool already enforces.
- Rules with no example.
- "Write clean, maintainable code": nobody can check it.
- Style rules copied from another project's stack.

## Setup after approval

Formatter config, linter config, strict type-check settings, and a pre-commit or CI step that runs all three.
