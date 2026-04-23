# CLAUDE.md

> Project-specific context for Claude. Replace every `{{PLACEHOLDER}}`; delete sections that don't apply.
>
> **The non-negotiable SDLC rules live in `.claude/sdlc-contract.md`** (auto-loaded via SessionStart hook in `.claude/settings.json`) and in `/sdlc-strict-waterfall` (Core rules 1-10, full workflows, protocols). Don't duplicate them here. This file is for project-specific facts only.

---

## 1. Project Snapshot

- **Name**: {{PROJECT_NAME}}
- **Purpose**: {{ONE_SENTENCE_WHAT_AND_WHY}}
- **Stage**: {{pre-v1 | v1.Y.Z shipped YYYY-MM-DD | maintenance}}
- **Primary users**: {{WHO_USES_THIS}}
- **Current phase**: {{docs/sdlc/01_requirement | docs/sdlc/02_design | docs/sdlc/03_implementation | docs/sdlc/04_testing | docs/sdlc/05_deployment | docs/sdlc/06_maintenance}} — {{open | signed off on YYYY-MM-DD}}
- **Active slice**: {{task_list.md → TO-### or "none — awaiting next spec"}}

## 2. Tech Stack

- **Language / runtime**: {{e.g. TypeScript 5.x / Node 20}}
- **Framework**: {{e.g. Next.js 15, FastAPI, Laravel 11, ...}}
- **Data**: {{db, cache, queue}}
- **Infra**: {{hosting, CI}}
- **Package manager**: {{pnpm | uv | cargo | composer | ...}} — do not mix managers.

Authorized by `docs/sdlc/02_design/architecture.md` + `docs/sdlc/03_implementation/module_breakdown.md`. Changes require doc amendment first (see `/sdlc-strict-waterfall`).

## 3. Entry Points & Layout

```
{{REPO_ROOT}}
├── docs/sdlc/01_requirement/  …  docs/sdlc/06_maintenance/   # 6-phase doc tree (see /sdlc-strict-waterfall)
├── .claude/                               # settings.json (SessionStart hook) + sdlc-contract.md
├── src/             # {{what lives here — must mirror module_breakdown.md}}
├── tests/           # {{unit | integration | e2e — must mirror test_cases.md}}
└── {{...}}
```

Authoritative file-to-doc map: `docs/sdlc/03_implementation/module_breakdown.md`.

Key files (project-specific):

- `{{path}}` — {{role, doc section that authorizes it}}
- `{{path}}` — {{role, doc section that authorizes it}}

## 4. Everyday Commands

| Intent        | Command   |
| ------------- | --------- |
| Install deps  | `{{CMD}}` |
| Run dev       | `{{CMD}}` |
| Run tests     | `{{CMD}}` |
| Lint / format | `{{CMD}}` |
| Typecheck     | `{{CMD}}` |
| Build         | `{{CMD}}` |
| Deploy        | `{{CMD}}` |

Full command reference: `docs/sdlc/03_implementation/build_and_run.md`.

## 5. Code Conventions

Authoritative source: `docs/sdlc/03_implementation/coding_standards.md`. Stack-specific summary:

- **Style**: enforced by {{linter/formatter}} — don't hand-format.
- **Naming**: {{camelCase | snake_case | ...}} per identifier kind.
- **Errors**: validate at boundaries per `docs/sdlc/02_design/api_design.md` error table; trust internal calls.
- **Tests**: TDD per `/sdlc-strict-waterfall` Core rule 7. Framework: {{vitest | pytest | pest | ...}}. Cataloged in `docs/sdlc/04_testing/test_cases.md`.

## 6. Project Guardrails

- **Never commit**: `.env*`, credentials, large binaries, generated artifacts.
- **Never run without asking**: `git push --force`, `reset --hard`, `rm -rf`, DB migrations on shared envs, destructive `gh`/cloud commands, revoking phase sign-offs.
- **Secrets** live in {{where}}; rotate via {{how}}.
- **Production access**: {{who/how}} — see `docs/sdlc/05_deployment/runbook.md`.

## 7. Branches, Commits, PRs

- **Branches**: `{{feat/ | fix/ | chore/}}<short-slug>` per `docs/sdlc/03_implementation/branching_and_commits.md`.
- **Commits**: {{Conventional Commits | project style}} — atomic; reference TO-### from `task_list.md`.
- **PRs**: {{size cap, required reviewers, CI gates}}. Self-review against `docs/sdlc/03_implementation/code_review_checklist.md`.

## 8. External References

- Spec: `docs/sdlc/01_requirement/srs.md` (and siblings)
- Design: `docs/sdlc/02_design/`
- Issue tracker: {{link}}
- Runbooks / oncall: `docs/sdlc/05_deployment/runbook.md`, {{external link}}
- Dashboards: {{link}}
- Upstream docs: {{framework / SDK / protocol specs}}

## 9. Known Quirks & Gotchas

- {{e.g. "Two-process DB access — only the web process writes"}}
- {{e.g. "Phase sign-off enforced in DB, not honor-system"}}
- {{e.g. "Migrations require downtime window — see runbook §4"}}
- {{e.g. "Auth middleware bypassed in /health — intentional, documented in api_design.md §7.2"}}
