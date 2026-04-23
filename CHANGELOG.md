# Changelog

All notable changes to this kit are documented here.

Format: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).
Versioning: [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) per
`docs/VERSIONING.md`.

This CHANGELOG covers the **kit itself**. Projects bootstrapped from this kit
maintain their own `05_deployment/release_notes.md` — do not conflate them.

## [Unreleased]

### Removed
- `docs/migrations/` directory and all v1→v2 upgrade guides. Kit follows a
  bootstrap pattern — existing projects stay on the kit version they were
  installed with; new features land in new bootstrapped projects. Adopters
  who want newer kit behavior re-bootstrap or overlay with `--force`.
- `NFR-MIGRATION-GUIDE-1` requirement removed from
  `docs/sdlc/01_requirement/non_functional_requirements.md`.
- Migration-guide enforcement in `scripts/release_check.py --tag`.

### Changed
- `docs/VERSIONING.md`: replaced the "Migration guide requirement" section
  with a "Bootstrap-pattern upgrade note" explaining the new approach.
- `README.md`: versioning section no longer references `docs/migrations/`.

## [2.0.0] - 2026-04-23

Queued for v2.0.0 release. All 13 CRs approved 2026-04-23 under the CR pipeline.
Any items landing before tag are added here.

### Added
- **CR-2026-001** — SDLC Metrics Subsystem: `tools/sdlc-metrics/` with Claude Code
  transcript adapter, pricing/budgets/phase-markers config, per-phase budget gate
  as optional 5th phase-sign-off gate, text/json/markdown/html report formats,
  trend history, secrets pre-filter, multi-harness adapter stubs.
- **CR-2026-004** — Excuse / Reality rationalization tables under each of the 5
  rules in `sdlc-contract.md` (always-loaded behavioral lever).
- **CR-2026-005** — Iron Law opening line + Red Flags section in every phase
  README (`01_requirement/` … `06_maintenance/`), live + template.
- **CR-2026-006** — Two-stage reconciliation gate (spec-compliance pass → code-
  quality pass) with ordered enforcement via `scripts/reconcile.py`. Spec self-
  review 4-question checklist required before sign-off ask.
- **CR-2026-007** — Mermaid decision flowcharts in `skill/reconciliation.md`,
  `skill/traceability-matrix.md`, `skill/SKILL.md`.
- **CR-2026-008** — Per-phase model-selection table (capability tiers) in
  `skill/SKILL.md`. Controller-extracts-text delegation pattern in
  `skill/workflows/phase3-implementation.md`.
- **CR-2026-009** — Doc lifecycle frontmatter (`status`, `signed_by`,
  `required_for`, `cite_as`) with formal JSON Schema. Canonical
  `config/task-types.yaml`. Expanded placeholder residue guard
  (`scripts/check_residue.py`) catching `{{...}}`, `TODO`, `FIXME`, `XXX`,
  `<TBD>`, `[to-be-filled]`.
- **CR-2026-010** — Multi-harness support: single Python hook script serving
  Claude Code (5 surfaces: CLI, VS Code, Cursor-ext, JetBrains, web), Cursor
  Agent, Copilot CLI. File-based Layer-2 for Codex CLI + Gemini CLI. Separate JS
  plugin for OpenCode. SHA-pinned script integrity.
- **CR-2026-012** — PRIVACY.md with zero-telemetry guarantee + CI airgap job.
- **CR-2026-013** — docs/VERSIONING.md defining SemVer policy + deprecation
  window + migration guide requirement. `scripts/release_check.py` enforces.
- **CR-2026-014** — Added NOTICE.md for third-party attribution.
- **CR-2026-015** — This CHANGELOG.md + `.github/workflows/release.yml` + Keep-a-
  Changelog discipline.
- **CR-2026-016** — Python 3.11+ as canonical automation runtime. `bootstrap.sh`
  and `build-archive.sh` become one-line launchers over `bootstrap.py` and
  `build_archive.py`. Windows 11 native support (no WSL / Git Bash required).
  `.gitattributes` enforces LF line endings.

### Changed
- **CR-2026-010 (breaking)** — `sdlc-contract.md` moves from
  `skill/.claude/sdlc-contract.md` to `skill/sdlc-contract.md` (harness-neutral).
  See `docs/migrations/v1.0-to-v2.0-sdlc-contract-path.md`.
- **CR-2026-016 (breaking)** — Toolchain floor raised to Python 3.11+; bash is
  no longer sufficient on Windows. See `docs/migrations/v1.0-to-v2.0-python-runtime.md`.
- **CR-2026-006 (breaking)** — Phase sign-off requires Pass-1 (spec) closure
  before Pass-2 (quality) opens; previous procedure conflated both. Phases signed
  under the prior gate remain valid (stricter ⊃ laxer).
- **CR-2026-009 (breaking)** — Every phase doc now carries frontmatter; scripts
  enforce `status` transitions (`template → draft → signed → amended → deprecated`).

### Deprecated
- (none in this release)

### Removed
- (none in this release)

### Fixed
- **CR-2026-010** — Hook script now verifies SHA-256 of contract file and itself
  on every launch (supply-chain hardening); fails loud on mismatch.
- Register placeholder row (`CR-2026-001 | {{...}}`) in `template/06_maintenance/
  change_requests.md` replaced with a clearly-marked example row.

### Security
- **CR-2026-010** — SHA-pinned hook script prevents silent injection of tampered
  contract content.
- **CR-2026-001** — Metrics analyzer rejects transcripts containing credential
  patterns (AWS keys, GitHub tokens); `AC-M-012` asserts the behavior.

### Migration
- `docs/migrations/v1.0-to-v2.0-sdlc-contract-path.md` — sdlc-contract.md move.
- `docs/migrations/v1.0-to-v2.0-python-runtime.md` — Python 3.11+ prereq.
- `docs/migrations/v1.0-to-v2.0-reconciliation-two-pass.md` — gate semantics.
- `docs/migrations/v1.0-to-v2.0-doc-frontmatter.md` — frontmatter adoption.

## [1.0.0] - 2026-04-18

First tagged release. Commit `963e7ce`.

### Added
- 6-phase SDLC doc-tree scaffold (`01_requirement/` … `06_maintenance/`) with 39
  artifact templates.
- `.claude/settings.json` SessionStart hook injecting `sdlc-contract.md` as
  IMPORTANT context every session.
- `.claude/sdlc-contract.md` with 5 non-negotiable rules.
- `/sdlc-strict-waterfall` skill with 10 Core rules, per-phase workflows, and
  change/migration/hotfix/removal protocols.
- `bootstrap.sh` for initializing a new project from the template tree.
- `build-archive.sh` producing `dist.zip` for distribution.
- `CLAUDE.template.md` for project-specific facts.
- Mermaid-only diagram convention (`references/mermaid-conventions.md`).
- Reconciliation gate with five-bucket triage (`reconciliation.md`).
- Traceability matrix (`traceability-matrix.md`).

---

[Unreleased]: https://github.com/Electronics-Extreme/claude-sdlc/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Electronics-Extreme/claude-sdlc/releases/tag/v1.0.0
