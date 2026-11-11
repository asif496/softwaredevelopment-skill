# Security guide (docs/SECURITY.md)

The security doc lists what must never go wrong and the rules that prevent it. An agent produces code that works long before it produces code that is safe: the page loads, the demo passes, and any signed-in user can read every other user's rows. Broken access control is first in the OWASP Top 10:2025 for that reason.

Write this doc as a reviewer looking for ways in, not as the author defending the design.

## Before writing

Read the PRD (roles, sensitive data), ARCHITECTURE.md (services, where code runs) and DATABASE.md (tables, access rules). Ask if unclear: who are the admins and how are they made; whether there are legal duties (payments, health, children, EU or other privacy law); who gets told if something leaks.

## Sections

**Data we hold.** `Data | Sensitivity | Where stored`. Include what is never stored: card data stays with the payment provider; passwords stay with the auth provider.

**Roles.** Each role, what it can do, and where that is enforced (database policy, middleware, server check).

**Auth and sessions.** The provider. Sessions in httpOnly, secure cookies. Every server route and action checks the session before doing anything. Authorization is decided on the server; hiding a button is not access control. Session length and what sign-out clears.

**Secrets.** Only in a gitignored env file and the host's environment settings. Only explicitly public variables reach the browser; admin or service keys never do. If a secret is ever committed: rotate it first, then remove it from history.

**Input and output.** Validate every input on the server with the shared schemas, even when the client already did. Parameterized queries only; no SQL built from strings. Uploads: allowed types, maximum size, type checked on the server, stored privately. Escape or sanitize anything rendered as HTML.

**Abuse.** Rate limits, with numbers, on sign-in, sign-up, password reset, and anything that sends email or SMS or calls a paid API. A spending cap on paid APIs.

**Dependencies.** No new package without approval. It must be maintained and widely used. A dependency audit runs in CI; high and critical findings are fixed before merging. Lockfile committed.

**Logging and alerts.** Errors are logged with a request id. Never log passwords, tokens, keys, full card numbers or full personal records. Say who is alerted for repeated sign-in failures or server errors.

**Abuse cases.** One line per P0 feature, in the form "What if a user...": changes the id in the URL to someone else's plan; submits the form 1,000 times; uploads a 2 GB file; signs up with another person's email. Each gets the rule that stops it. This is where most real holes are found.

**Pre-merge checklist**, mapped to the OWASP Top 10:2025:

- [ ] A01 Broken Access Control: can user A read or change user B's data through any route, action or query?
- [ ] A02 Security Misconfiguration: no debug mode, default credentials, open storage buckets or permissive CORS.
- [ ] A03 Software Supply Chain Failures: new dependencies approved, audited and pinned in the lockfile.
- [ ] A04 Cryptographic Failures: HTTPS everywhere; no secrets in code, logs or client bundles; no home-made crypto.
- [ ] A05 Injection: all input validated server-side; no string-built SQL, shell commands or HTML.
- [ ] A06 Insecure Design: the feature's abuse case is written above and handled.
- [ ] A07 Authentication Failures: session checked in every new route or action; sign-in is rate limited.
- [ ] A08 Software or Data Integrity Failures: webhooks verify signatures; nothing is deserialized from an untrusted source.
- [ ] A09 Security Logging and Alerting Failures: failures are logged with a request id and contain no secrets.
- [ ] A10 Mishandling of Exceptional Conditions: errors fail closed, and users never see a stack trace.

## Reviewing existing code

When code exists, check it against this doc and list every violation as `rule | file:line | what is wrong | fix`. Look first at: queries with no owner filter, routes with no session check, env variables exposed to the client, secrets in the repository history, raw SQL, and upload handlers.

## Self-check

- Every table in DATABASE.md is covered by a role rule here.
- Every P0 feature has an abuse case.
- Every rate limit has a number.
- The checklist is short enough to actually walk on each change.
- No rule depends on the client behaving well.

## Common mistakes

- Checking permissions only in the UI.
- A service or admin key in a client file.
- "We'll add security before launch."
- Rules with no enforcement point ("data must be protected").
- A 60-item checklist nobody reads.

## AI features

If the product calls a language model, add: content fetched from users, files or the web is untrusted and can carry instructions, so the model's output never triggers a privileged action without a server-side check; no secrets in prompts; model output is validated before it is stored or rendered; personal data sent to the provider is listed under "Data we hold"; per-user rate and spend limits.
