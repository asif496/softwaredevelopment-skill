# softwaredevelopment

A Claude skill that plans a software project on paper before any code is written, then builds against that plan and keeps the two in agreement.

AI coding agents start every session with an empty memory. Without written decisions they drift: features nobody asked for, a different button style on every screen, tables any signed-in user can read, and "done" that was never tested. This skill has Claude write the decisions down once, in files every agent rereads, and stop for your review after each one.

## What it writes

```
your-project/
├── AGENTS.md              map for every AI agent: commands, rules, which doc to read when
├── CLAUDE.md              imports AGENTS.md (for Claude Code)
└── docs/
    ├── PRD.md             what we build, for whom, and what we don't
    ├── DESIGN_SYSTEM.md   how it looks
    ├── ARCHITECTURE.md    how the parts fit
    ├── DATABASE.md        what data we store and who may touch it
    ├── SECURITY.md        what must never go wrong
    ├── CODE_STYLE.md      how code is written here
    ├── TESTING.md         how we prove it works
    └── PLAN.md            the build order, one small task at a time
```

A complete worked example is in [`examples/studyplan`](examples/studyplan).

## Commands

| You type | Claude does |
|---|---|
| `/softwaredevelopment` | Asks for your app idea, then runs the full flow |
| `/softwaredevelopment <app idea>` | Interviews you and writes the docs one at a time, stopping for approval after each |
| `/softwaredevelopment <doc>` | Writes or redoes one doc (`prd`, `security`, `agents`...) |
| `/softwaredevelopment existing` | Documents a project that already has code, then lists where the code breaks its own rules |
| `/softwaredevelopment status` | Shows each doc's status, open questions and the next step |
| `/softwaredevelopment audit` | Checks the docs for gaps, vague rules and contradictions |
| `/softwaredevelopment plan` | Writes the build plan |
| `/softwaredevelopment build next` | Builds the next task (or `build F1`, `build T3`) |
| `/softwaredevelopment change <what>` | Updates the affected docs first, then the code |
| `/softwaredevelopment review` | Lists every place docs and code disagree |

Plain requests work as well: "plan my app", "document this repo", "are my docs still right?"

## What's different from a prompt template

- **It sizes the job.** A weekend script gets a one-page PRD and an AGENTS.md. A product with payments gets all eight docs plus an API contract and a deployment runbook.
- **It fits the project type and stack.** Web, mobile, API, CLI, automation between systems (CRMs, forms, n8n), and AI products each reshape the docs. Stack-specific rules are translated for Django, FastAPI, Laravel, Express + MongoDB and Flutter + Firebase.
- **Everything has an ID.** Features (F1), stories (US-1) and tasks (T1) are cited across docs, tests and the plan, so gaps are visible.
- **It checks its own work.** A bundled script finds P0 features with no story, tables with no access rule, placeholders left in approved docs, commands that don't exist in `package.json`, and tables in the migrations that the docs don't mention.
- **It keeps going after the docs.** A build plan in thin end-to-end slices, a build loop with tests first, change requests that update docs before code, and a weekly drift review.

## Install

### Claude app

1. Download [`dist/softwaredevelopment.zip`](dist/softwaredevelopment.zip).
2. In Claude, open **Customize > Skills**, press **+**, choose **Create skill**, then **Upload a skill**.
3. Upload the zip and make sure the skill is switched on.

Skills need "Code execution and file creation" to be enabled under Settings > Capabilities. Menu names change from time to time; Anthropic's current steps are in [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

If you already have an older `softwaredevelopment` skill, remove it first so the two don't clash.

### Claude Code

Copy the `softwaredevelopment` folder into your skills folder:

```bash
# for every project
cp -r softwaredevelopment ~/.claude/skills/

# or for one project only
cp -r softwaredevelopment your-project/.claude/skills/
```

## Using the scripts yourself

Claude runs these for you, but they work on their own too. Python 3.9 or newer, no packages to install.

```bash
# copy one doc's template into a project (never overwrites)
python3 softwaredevelopment/scripts/init_docs.py path/to/project --doc prd --name "My App"

# check the docs against each other and against the code
python3 softwaredevelopment/scripts/check_docs.py path/to/project
python3 softwaredevelopment/scripts/check_docs.py path/to/project --json     # for CI
python3 softwaredevelopment/scripts/check_docs.py path/to/project --strict   # warnings fail too
```

The checker exits with 1 when it finds errors, so it can run in CI. Try it on the example:

```bash
python3 softwaredevelopment/scripts/check_docs.py examples/studyplan
```

It is a net for mechanical mistakes. It can't tell whether a decision is a good one; `audit` has Claude read for that.

## What's in this repository

```
softwaredevelopment/        the skill (this folder is what gets installed)
├── SKILL.md                the instructions Claude follows
├── references/             one guide per doc, plus project types, modes and extra docs
├── assets/templates/       a skeleton for every doc
└── scripts/                init_docs.py and check_docs.py
examples/studyplan/         a full set of docs for a sample app
dist/softwaredevelopment.zip  ready to upload
```

To rebuild the zip after changing the skill:

```bash
rm -f dist/softwaredevelopment.zip
zip -r dist/softwaredevelopment.zip softwaredevelopment -x "*/__pycache__/*" "*.pyc" "*.DS_Store"
```

## Credits

The eight-doc method follows the free guide "8 Docs Before You Vibe Code" by @kgtechtalks. This skill is an independent rewrite that adds project sizing, project types, stack translation, the build plan and loop, change requests, the checker and the worked example.

## License

MIT. See [LICENSE](LICENSE).
