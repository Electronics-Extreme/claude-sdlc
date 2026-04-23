---
doc: docs/VERSIONING.md
status: signed
signed_by: Thanin Piromward on 2026-04-23
required_for: [phase-5-deploy-prep, phase-6-CR-implementation]
cite_as: VER
---

# Versioning policy

This kit follows **Semantic Versioning 2.0.0** (https://semver.org/spec/v2.0.0.html)
strictly. Canonical version lives in `VERSION` (single line, no `v` prefix).

## Change classification

For **this kit** — NOT for your projects bootstrapped from it (each adopter's
project versions itself independently):

| Bump | Trigger |
|---|---|
| **MAJOR** | Removes or renames a public path, flag, or file; changes a contract rule's semantics; raises a toolchain floor (Python / bash / OS version); changes reconciliation gate behavior; changes phase sign-off requirements. |
| **MINOR** | Adds functionality backward-compatibly — new scripts, new templates, new opt-in features, new phase-doc scaffolds, new CR-handled features, new harness adapters, added guidance. |
| **PATCH** | Bug fixes in scripts or docs; typo fixes; clarifications that don't change semantics. |

### Examples applied to the current CR pipeline

| CR | Bump | Why |
|---|---|---|
| CR-2026-001 metrics subsystem | MINOR | Additive — adds `tools/sdlc-metrics/` |
| CR-2026-004 rationalization tables | MINOR | Adds content; no removals |
| CR-2026-005 Iron Law + Red Flags | MINOR | Additive doc sections |
| CR-2026-006 two-pass reconciliation | **MAJOR** | Changes phase sign-off gate semantics |
| CR-2026-007 Mermaid diagrams | MINOR | Additive |
| CR-2026-008 model + delegation | MINOR | Additive guidance |
| CR-2026-009 doc lifecycle frontmatter | **MAJOR** | Adds required frontmatter; unsigned docs now fail |
| CR-2026-010 multi-harness | **MAJOR** | Moves `sdlc-contract.md` path; existing `.claude/settings.json` hooks break without migration |
| CR-2026-012 privacy | MINOR | Adds PRIVACY.md |
| CR-2026-013 this policy | MINOR | Adds policy doc |
| CR-2026-014 attribution | MINOR | Adds NOTICE.md |
| CR-2026-015 CHANGELOG | MINOR | Adds release discipline |
| CR-2026-016 Python runtime | **MAJOR** | Raises toolchain floor to Python 3.11+ |

**Aggregate bump for this release window: v1.0.0 → v2.0.0** (because CR-006, CR-009,
CR-010, CR-016 are all MAJOR — any one would suffice to bump MAJOR).

## Deprecation window

A deprecated path, flag, or file MUST continue working for at least **2 minor
versions** after deprecation is announced. Removal happens in the next MAJOR bump.

Example flow:
- v2.0.0 — ship new path; old path marked `deprecated` with a warning in output.
- v2.1.0 — deprecation still active; CHANGELOG reminds.
- v2.2.0 — deprecation still active.
- v3.0.0 — old path removed; `CHANGELOG.md [3.0.0] Removed` section.

## Bootstrap-pattern upgrade note

This kit creates new projects from scratch via `bootstrap.sh`, `npx claude-sdlc
init`, or `python scripts/bootstrap.py`. Existing projects that were bootstrapped
from an older kit version **stay on that version** — they aren't continuously
upgraded. Adopters who want a newer kit's behavior:

- Re-bootstrap into a fresh directory and migrate their phase docs over, or
- Overlay the newer `skill/`, `hooks/`, `scripts/`, `config/` on top of their
  existing project with a `--force` install, preserving their `docs/sdlc/`
  content.

No formal per-version migration guides are shipped. The `CHANGELOG.md` section
for each release describes what changed; git diffs are the upgrade spec.

## Release process (summary)

1. Bump `VERSION` via `python scripts/bump_version.py <major|minor|patch>`.
2. Promote `[Unreleased]` to `[X.Y.Z]` in `CHANGELOG.md`.
3. Commit with message `release: vX.Y.Z`.
4. Tag: `git tag vX.Y.Z && git push --tags`.
5. `release.yml` workflow: builds `dist.zip`, creates GitHub Release with CHANGELOG
   section as release notes.
6. `scripts/release_check.py` verifies VERSION ↔ CHANGELOG ↔ tag consistency.

## Change history

- 2026-04-23 — Initial draft, signed under CR-2026-013.
