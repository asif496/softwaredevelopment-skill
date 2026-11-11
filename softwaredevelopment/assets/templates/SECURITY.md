# Security: {{APP_NAME}}
Status: draft | Last updated: {{DATE}}

## Data we hold
| Data | Sensitivity | Where stored |
|---|---|---|
| <data> | <low / medium / high> | <where> |

Never stored: <e.g. card data, which stays with the payment provider>.

## Roles
| Role | Can do | Enforced by |
|---|---|---|
| anonymous | <what> | <where> |
| user | <what> | <where> |

## Auth and sessions
- Provider: <provider>. Sessions live in httpOnly, secure cookies.
- Every server route and action checks the session before doing anything.
- Authorization is decided on the server, never by hiding a button.

## Secrets
- Secrets live only in <gitignored env file> and <host settings>.
- Only <public variable pattern> reaches the browser. <Admin or service key> never does.
- If a secret is committed: rotate it first, then remove it.

## Input and output
- Every input is validated on the server with <shared schemas>.
- Parameterized queries only. No SQL built from strings.
- Uploads: <allowed types, max size, server-side type check, private storage; or "none in v1">.

## Abuse
- Rate limits: <endpoint: number per period>
- <Spending cap on paid APIs, if any>

## Dependencies
- No new package without approval. It must be maintained and widely used.
- <Audit command> runs in CI. High and critical findings are fixed before merging.

## Logging
- Errors are logged with a request id.
- Never log passwords, tokens, keys or full personal records.

## Abuse cases
- <F1>: what if a user <does something hostile>? <The rule that stops it.>

## Pre-merge checklist
- [ ] A01 Access control: can user A read or change user B's data?
- [ ] A02 Misconfiguration: no debug mode, default credentials or open storage.
- [ ] A03 Supply chain: new dependencies approved and audited.
- [ ] A04 Cryptography: no secrets in code, logs or client bundles.
- [ ] A05 Injection: all input validated server-side; no raw SQL.
- [ ] A06 Design: the feature's abuse case is written and handled.
- [ ] A07 Authentication: session checked in every new route or action.
- [ ] A08 Integrity: webhooks verify signatures.
- [ ] A09 Logging: failures logged with a request id and no secrets.
- [ ] A10 Errors: fail closed; no stack traces shown to users.

## Open questions
- [ ] <question>
