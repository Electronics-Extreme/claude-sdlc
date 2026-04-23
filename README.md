# SDLC Strict Waterfall Kit

Doc-first Software Development Lifecycle methodology for AI coding agents.
Works natively on six harnesses — **Claude Code** (CLI + VS Code + Cursor
extension + JetBrains + `claude.ai/code` web), **Cursor Agent**, **GitHub
Copilot CLI**, **OpenAI Codex CLI/App**, **Google Gemini CLI**, and **OpenCode**.

**v2.0.0** · Released 2026-04-23 · MIT · Python 3.11+ only

## What this kit is

A scaffolded 6-phase waterfall SDLC tree (`docs/sdlc/01_requirement/` … `docs/sdlc/06_maintenance/`)
plus a runtime that keeps AI coding agents honest about it.

At session start, a **5-rule contract** is auto-injected as `IMPORTANT` context.
At phase sign-off, a **two-pass reconciliation gate** blocks drift between
signed docs and shipped code. Throughout, an **on-demand skill**
(`/sdlc-strict-waterfall`) provides the full protocol: Core rules 1-10,
per-phase workflows, change/migration/hotfix/removal procedures, and a
traceability matrix from requirement to commit.

Everything is **measurement-backed**: every NFR carries a numeric target; a
metrics subsystem (`tools/sdlc_metrics/`) reports token cost per phase; a
residue guard refuses to sign docs with placeholder content; a SHA-pinned hook
script refuses to inject a tampered contract.

## Quick start

```bash
# Prerequisites: Python 3.11+ (runtime). Node.js ≥18 only if using npm/npx.

# Option 1 — npx (no install, after publish)
npx claude-sdlc init ~/Projects/MyProject --harness claude

# Option 2 — npm global
npm install -g claude-sdlc
claude-sdlc init ~/Projects/MyProject --harness claude

# Option 3 — shell bootstrap (after git clone)
./bootstrap.sh ~/Projects/MyProject --harness claude        # Unix / macOS
bootstrap.bat C:\Projects\MyProject --harness claude        # Windows cmd
.\bootstrap.ps1 C:\Projects\MyProject --harness claude      # PowerShell

# Then
cd ~/Projects/MyProject
# Start your AI agent (claude, cursor, codex, gemini, copilot, opencode).
# The SessionStart hook auto-loads the contract.
```

Available harness values: `claude` · `cursor` · `codex` · `gemini` ·
`copilot` · `opencode` · `all` (default).

Per-harness install detail: `docs/INSTALL.claude-code.md`,
`docs/INSTALL.cursor.md`, `docs/INSTALL.gemini.md`, `docs/INSTALL.codex.md`,
`docs/INSTALL.copilot.md`, `docs/INSTALL.opencode.md`.
npm CLI: `docs/INSTALL.npm.md`. Windows setup: `docs/INSTALL.windows.md`.

## The methodology

Six phases, strictly ordered. No phase skips. Every phase gates on four checks
plus two-pass reconciliation before sign-off:

```
docs/sdlc/01_requirement  →  docs/sdlc/02_design  →  docs/sdlc/03_implementation  →  docs/sdlc/04_testing  →  docs/sdlc/05_deployment  →  docs/sdlc/06_maintenance
     SRS            Architecture      Source code        Test report      Release         Change requests
   signed off     + DB + API         + unit tests      + defects log     + runbook     + incident log
```

**Five non-negotiable rules** (always-loaded via SessionStart hook):

1. REFUSE direct code edits — route via CR + doc amendment
2. No code without a doc parent in signed 01/02/03
3. No phase skipping — N+1 requires N sign-off
4. Signed docs are frozen — amend via Post-vX.Y.Z sections
5. Reconciliation gate before every phase sign-off (two ordered passes)

Each rule ships with an **Excuse / Reality rationalization table** that
anticipates the specific rationalizations an agent (or human) invents to skip
the rule.

**Core rule 7 — TDD inside every slice.** RED-GREEN-REFACTOR per TO-###.
Tests derive from AC-### / TC-### in the signed docs — never invent behavior.

**Core rule 9 — Four gates + two-pass reconciliation**:
- typecheck + lint + full test suite + reconciliation Pass 1 (spec) before Pass 2 (quality) before sign-off

See `skill/sdlc-contract.md` for the 5 rules in full; `skill/SKILL.md` for
Core rules 1-10, per-phase workflows, and protocols.

## What's in the kit

| Area | Contents |
|---|---|
| Phase scaffolds | `docs/sdlc/01_requirement/` … `docs/sdlc/06_maintenance/` — 39 artifact templates per phase |
| Skill | `skill/sdlc-contract.md`, `skill/SKILL.md`, `skill/reconciliation.md`, `skill/traceability-matrix.md`, workflows × 4, protocols × 4, references × 2, required-reads manifest |
| Hooks | `hooks/session_start.py` (6-harness env-detect + SHA integrity + banner), `run-hook.cmd` / `.sh` launchers |
| Scripts | 12 Python 3.11+ stdlib scripts: bootstrap, build-archive, check_frontmatter, check_residue, check_task_types, update_contract_sha, sync_wrappers, reconcile, bump_version, release_check, add_frontmatter |
| Metrics subsystem | `tools/sdlc_metrics/` — phase-aware token analyzer with 6 adapter stubs, 4 report formats (text/JSON/markdown/HTML), SQLite history, budget gate, secrets pre-filter |
| Config | `config/pricing.yaml`, `budgets.yaml`, `phase-markers.yaml`, `task-types.yaml`, `harnesses.yaml`, `residue-exceptions.yaml` |
| Schemas | `schemas/doc-frontmatter.schema.yaml`, `task-types.schema.yaml` |
| Harness adapters | `.claude/`, `.claude-plugin/`, `.cursor-plugin/`, `.codex/`, `.opencode/`, `gemini-extension.json`, `AGENTS.md`, `GEMINI.md` |
| Policy docs | `PRIVACY.md`, `NOTICE.md`, `LICENSE`, `CHANGELOG.md`, `docs/VERSIONING.md` |
| CI workflows | `.github/workflows/sdlc-tests.yml`, `release.yml`, `airgap.yml` |

Total: ~290 files, ~830 KB `dist.zip`.

## Verifiable claims

Every claim in this README is backed by a measurement or CI gate:

| Claim | Verified by |
|---|---|
| Zero telemetry, zero analytics, zero remote fetch except user-invoked | `.github/workflows/airgap.yml` runs every script with network denied; exit 0 required |
| Works on Windows 11 natively | `.github/workflows/sdlc-tests.yml` matrix includes `windows-2022` |
| Python 3.11 stdlib only | Grep-check on `import` lines + airgap job |
| Every phase doc has valid frontmatter | `scripts/check_frontmatter.py` in CI |
| No placeholder residue in signed docs | `scripts/check_residue.py` in CI |
| Contract + hook integrity (SHA-pinned) | `scripts/update_contract_sha.py --check` in CI |
| Harness wrappers stay in sync | `scripts/sync_wrappers.py --check` in CI |
| SemVer correctness on release | `scripts/release_check.py --tag` in release workflow |
| HTML metrics report is self-contained ≤ 500 KiB | NFR-METRICS-OUT-1 asserted in tests |
| Metrics adapter ≤ 200 LOC for well-formed transcripts | NFR-METRICS-ADAPT-1 — Claude Code reference is 180 LOC |

## Token budget

Default per-phase budgets (from `config/budgets.yaml`, editable per adopter):

| Phase | Token hard-cap | Cost hard-cap | Cache floor |
|---|---|---|---|
| 01 requirement | 80K | $0.40 | 60% |
| 02 design | 100K | $0.55 | 65% |
| 03 implementation | 150K | $0.75 | 70% |
| 04 testing | 90K | $0.45 | 70% |
| 05 deployment | 60K | $0.30 | 55% |
| 06 maintenance | 70K | $0.35 | 60% |

Run `python3 tools/sdlc_metrics/analyze.py budget-check <session.jsonl>
--phase 3` to enforce. Exit 1 on breach.

## Versioning + stability

Strict **SemVer 2.0**. The kit follows a bootstrap pattern — existing
projects stay on the kit version they installed; new features land in new
bootstrapped projects. See `docs/VERSIONING.md`.

## Contributing

This kit is distributed as-is. Changes go through the kit's own SDLC:

1. File a CR in `docs/sdlc/06_maintenance/change_requests.md` (use the template)
2. Approve per class (minor = TL; major = TL + PO; breaking = TL + PO + Security)
3. Amend Phase 1/2/3 docs as declared in the CR
4. Implement per Core rule 7 (TDD)
5. Close reconciliation — Pass 1 spec compliance, then Pass 2 code quality
6. Bump VERSION, promote CHANGELOG, tag
7. `release.yml` publishes `dist.zip`

## License

MIT — see `LICENSE`.

## Privacy

Zero telemetry. Zero analytics. Zero remote fetch except user-invoked
`pricing-sync` and harness marketplace installs. See `PRIVACY.md`.
