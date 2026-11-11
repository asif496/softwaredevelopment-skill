# PRD: StudyPlan
Status: approved | Owner: Example | Last updated: 2026-11-11
Type: web | Size: standard

## 1. Problem
University students struggle to prepare for several exams at once because tasks live in notes apps, chats and memory, so deadlines get missed. Today they keep a messy notes file or a paper list.

## 2. Users
- Primary: university students with 3-6 exams in a term, mostly on phones.
- Secondary: none in v1.

## 3. Goals and non-goals
Goals (v1):
- A new user creates their first plan in under 2 minutes.
- A user sees all tasks due in the next 7 days on one screen.

Non-goals (v1):
- No native mobile app (responsive web only).
- No payments or paid tiers.
- No sharing or study groups.
- No AI features.

## 4. Features
| ID | Feature | Priority |
|----|---------|----------|
| F1 | Email + Google sign-in | P0 |
| F2 | Create, edit, delete a plan (title, exam date) | P0 |
| F3 | Add, complete, delete tasks inside a plan | P0 |
| F4 | Dashboard: plans list + tasks due in next 7 days | P0 |
| F5 | Email reminder the day before a task is due | P1 |
| F6 | Share a plan with a friend | P2 |

## 5. User stories
**US-1 (F1):** As a student, I want to sign in with Google so that I don't manage another password.
- [ ] Given I'm signed out, when I tap "Continue with Google" and approve, then I land on the dashboard.
- [ ] Given a wrong email/password, when I submit, then I see "Email or password is incorrect".

**US-2 (F2):** As a student, I want to create a plan for an exam so that my tasks are grouped.
- [ ] Given the plan form, when I submit an empty title, then I see "Title is required".
- [ ] Given a valid title, when I save, then the plan appears at the top of the list without a reload.
- [ ] Given a plan, when I delete it and confirm, then its tasks are deleted too.

**US-3 (F3):** As a student, I want to tick off tasks so that I see what is left.
- [ ] Given a task, when I tap its checkbox, then it shows as done and stays done after reload.
- [ ] Given a task with a due date earlier than today, then it shows an "Overdue" label.

**US-4 (F4):** As a student, I want one screen with what is due soon so that I know what to study today.
- [ ] Given tasks due in the next 7 days, when I open the dashboard, then they are listed soonest first.
- [ ] Given no plans, when I open the dashboard, then I see an empty state with one "Create plan" button.

## 6. User flows
Sign up: Landing -> Sign in -> Dashboard (empty state)
Core loop: Dashboard -> New plan -> Add tasks -> Back to Dashboard

## 7. Screens
Landing, Sign in, Dashboard, Plan detail, Settings (delete account).

## 8. Constraints
- Devices and browsers: the last two versions of Chrome, Safari and Firefox; phones from 360 px wide.
- Speed: the dashboard shows its content within 2 seconds on a 4G connection.
- Languages: English only in v1.

## 9. Open questions
- [ ] Do we need offline support in v1? (decides: owner)
- [ ] Which time zone do due dates use: the device's or a fixed one? (decides: owner)
