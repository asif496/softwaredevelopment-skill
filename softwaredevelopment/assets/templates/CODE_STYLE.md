# Code style: {{APP_NAME}}
Status: draft | Last updated: {{DATE}}

## Tooling
- <Strict type settings, e.g. TypeScript strict; no `any`, use `unknown` and narrow it.>
- <Formatter> and <linter> run on save and in CI. Fix lint errors; never disable the rule.

## Naming
| Thing | Style | Example |
|---|---|---|
| Component file | <style> | <example> |
| Other files | <style> | <example> |
| Functions, variables | <style; verbs for functions> | <example> |
| Constants | <style> | <example> |
| Types | <style> | <example> |
| Booleans | is/has/can prefix | <example> |

## Structure
- One component per file. Files under about 200 lines; split when bigger.
- Functions do one thing and stay under about 40 lines.
- Database access only through <the database layer; see docs/ARCHITECTURE.md>.

## Patterns
<Replace each block with a 3-5 line example in this project's real code.>

Data fetching:

```
example
```

Forms:

```
example
```

Server actions or endpoints return one result shape:

```
example
```

Dates: <one library; store UTC, show in the user's time zone>.

## Avoid
- A new state, CSS or date library: one of each is already chosen.
- Copy-pasted logic: search for an existing helper first.
- Magic numbers: name them as constants.
- Commented-out code: Git remembers it.

## Errors
Show the user a friendly, specific message. Log the technical detail with the request id.

## Comments
Explain why, not what. A comment that repeats the code gets deleted.

## Git
- Branches: <pattern, e.g. feat/plan-sharing, fix/login-redirect>
- Commits: Conventional Commits (feat:, fix:, refactor:, test:, docs:).
- One pull request is one change, ideally under 400 lines.

## Open questions
- [ ] <question>
