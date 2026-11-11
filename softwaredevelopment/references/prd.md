# PRD guide (docs/PRD.md)

The PRD says what gets built, for whom, and what is deliberately left out. Every other doc reads it, so a mistake here is copied into all of them. It is also what stops an agent inventing features: anything not in the PRD is out of scope until the user adds it.

## Before writing

Interview the user. One message, at most 10 short questions, skipping anything they already told you. Choose from:

1. Who exactly uses this, and what do they do today instead?
2. What is the one thing a user must manage in their first session?
3. Which features must exist on day one, and which can wait?
4. What should v1 definitely not do?
5. How will you know it works? Ask for a number: time to first result, tasks completed, sign-ups.
6. Web, mobile or both? Which devices matter most?
7. How do people sign in: email, Google, phone code, or no accounts?
8. Does it store anything sensitive: personal data, payments, health, documents?
9. Are there roles (admin, member, guest), and what differs between them?
10. Any deadline, budget, hosting or tech constraint?
11. Languages, currency, time zones? Ask when the audience isn't clearly one locale.
12. Does it connect to anything: payments, email or SMS, a CRM, an AI model?

If the user says "you decide", pick sensible defaults and list each one under "Assumptions" when you present the doc.

## Sections

**Header.** `Status`, `Owner`, `Last updated`, then `Type` and `Size`.

**1. Problem.** Two or three sentences: who struggles with what, why, and what they do today. If you can't name today's workaround, the problem isn't understood yet; ask.

**2. Users.** Primary persona and their main job. A secondary one only if v1 serves them.

**3. Goals and non-goals.** Goals are measurable ("a new user creates their first plan in under 2 minutes"). Non-goals name things someone might reasonably expect and won't get: no native app, no payments, no sharing. Non-goals do more work than goals, because they are what an agent would otherwise add.

**4. Features.** Table of `ID | Feature | Priority`. P0 = v1 doesn't ship without it. P1 = soon after. P2 = later. At most 5 P0. If the user wants more, ask which five they'd keep if they had one week.

**5. User stories.** One or more per P0 feature:

```
**US-2 (F2):** As a student, I want to create a plan for an exam so that my tasks are grouped.
- [ ] Given the plan form, when I submit an empty title, then I see "Title is required".
- [ ] Given a valid title, when I save, then the plan appears at the top of the list without a reload.
```

Each criterion is one observable result. Cover the success case, the main failure case, and the empty state.

**6. User flows.** Arrows between screens for sign-up and the core loop.

**7. Screens.** The list of screens. Types with no UI replace this with "Interfaces": endpoints, commands or triggers.

**8. Constraints.** Only what is decided: supported devices and browsers, a speed budget with a number, languages, offline or not, deadline.

**9. Open questions.** Checkbox list. Each names who decides.

## Self-check

- Non-goals exist and are specific.
- At most 5 P0 features, and each has at least one story.
- Every story cites a feature ID that exists in the table.
- Every acceptance criterion could be checked by a tester who has never met the user. Words that fail this test: fast, easy, intuitive, clean, nice, seamless, properly, user-friendly.
- Nothing in Features contradicts Non-goals.
- Sensitive data and roles are named here, because SECURITY.md and DATABASE.md are built from them.

## Common mistakes

- A wish list with no priorities, so the agent builds P2 features first because they sounded interesting.
- No non-goals.
- Criteria like "works well on mobile". Write the breakpoint and what must be visible.
- Describing the solution's tech ("uses Redis") instead of the behaviour. Tech belongs in ARCHITECTURE.md.
- Renumbering features after a cut. Mark the row `cut` and keep the ID.

## Lite size

One page: Problem, Features (P0 only), Non-goals, three to six acceptance criteria, Open questions.
