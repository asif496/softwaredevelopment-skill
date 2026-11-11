# Architecture: {{APP_NAME}}
Status: draft | Last updated: {{DATE}}

## Stack
| Layer | Choice (version) | Why |
|---|---|---|
| Framework | <choice> | <one line> |
| Language | <choice> | <one line> |
| UI | <choice> | <one line> |
| Database and auth | <choice> | <one line> |
| Hosting | <choice> | <one line> |
| Tests | <choice> | <one line> |

## System diagram
<Replace the diagram below.>

```
Client -> Server
            |-> Database / Auth / Storage
            |-> Email service
```

## Folder structure
<Replace the paths below. One line per folder: what belongs there and what doesn't.>

```
src/app/            routes and pages only; no business logic
src/components/     shared components
src/lib/db/         every database query lives here and nowhere else
src/lib/services/   business logic as pure functions
src/lib/validation/ schemas shared by client and server
```

## Request flow: <main user action>
1. <Step, naming the file>
2. <Step>
3. <Step>

## External services
- <Service>: <what it is used for; what happens if it is down>

## Environments
- Local: <how it runs>
- Preview: <how it is created>
- Production: <how a deploy happens>

## Decision log
- {{DATE}}: <decision>, because <reason>.

## Boundaries
- <What may call what, e.g. "the UI never talks to the database directly">
- A new third-party service is added to this doc before the code.

## Open questions
- [ ] <question>
