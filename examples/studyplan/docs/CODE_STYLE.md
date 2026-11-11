# Code style: StudyPlan
Status: approved | Last updated: 2026-11-11

## Tooling
- TypeScript strict. No `any`; use `unknown` and narrow it.
- Prettier and ESLint run on save and in CI. Fix lint errors; never disable the rule.

## Naming
| Thing | Style | Example |
|---|---|---|
| Component file | PascalCase.tsx | PlanCard.tsx |
| Other files | kebab-case.ts | date-utils.ts |
| Functions, variables | camelCase, verbs for functions | getPlans, isOverdue |
| Constants | UPPER_SNAKE_CASE | MAX_PLANS_PER_USER |
| Types | PascalCase, no I- prefix | Plan, PlanInput |
| Booleans | is/has/can prefix | isDone, hasAccess |

## Structure
- One component per file. Files under about 200 lines; split when bigger.
- Functions do one thing and stay under about 40 lines.
- Server components by default; add "use client" only when a component needs state or browser APIs.
- Database access only through `src/lib/db/` (see docs/ARCHITECTURE.md).

## Patterns
Data fetching happens in server components through the db layer:

```tsx
export default async function DashboardPage() {
  const user = await requireUser();
  const plans = await getPlans(user.id);
  return <PlanList plans={plans} />;
}
```

Forms use react-hook-form with the Zod schema from `src/lib/validation/`:

```tsx
const form = useForm<PlanInput>({ resolver: zodResolver(planSchema) });
const onSubmit = form.handleSubmit(async (values) => {
  const result = await createPlan(values);
  if (!result.ok) form.setError("root", { message: result.error });
});
```

Server actions return a result and never throw to the UI:

```ts
export async function createPlan(input: unknown): Promise<Result<Plan>> {
  const parsed = planSchema.safeParse(input);
  if (!parsed.success) return { ok: false, error: "Title is required" };
  const user = await requireUser();
  return { ok: true, data: await insertPlan(user.id, parsed.data) };
}
```

Dates: date-fns only. Store UTC, show in the user's time zone.

## Avoid
- A new state, CSS or date library: one of each is already chosen.
- Copy-pasted logic: search `src/lib/` for an existing helper first.
- Magic numbers: name them as constants.
- Commented-out code: Git remembers it.

## Errors
Show the user a friendly, specific message. Log the technical detail with the request id.

## Comments
Explain why, not what. A comment that repeats the code gets deleted.

## Git
- Branches: feat/plan-sharing, fix/login-redirect.
- Commits: Conventional Commits (feat:, fix:, refactor:, test:, docs:).
- One pull request is one change, ideally under 400 lines.

## Open questions
None.
