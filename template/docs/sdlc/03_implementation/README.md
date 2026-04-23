---
doc: template/03_implementation/README.md
status: template
required_for: ['phase-3-slice', 'phase-3-refactor']
cite_as: README
---

# Phase 3 — Implementation

> **IRON LAW: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**

**Goal:** Build the system per the signed design. No surprises, no scope creep.

## Inputs
- `docs/sdlc/01_requirement/` — frozen
- `docs/sdlc/02_design/` — signed

## Documents

| File                       | Purpose                                           |
|----------------------------|---------------------------------------------------|
| `coding_standards.md`      | Style, naming, review rules                       |
| `module_breakdown.md`      | Which module implements which FR/design component |
| `development_plan.md`      | Task order, owners, estimates, dependencies      |
| `branching_and_commits.md` | Git workflow, commit hygiene                      |
| `code_review_checklist.md` | Mandatory checks before merge                     |
| `build_and_run.md`         | Local dev setup, build commands                   |

## Exit Criteria

- [ ] All `MUST` FRs implemented
- [ ] Unit tests ≥ NFR-MNT-01 target
- [ ] Static analysis / linter clean
- [ ] All code reviewed and merged to `main`
- [ ] Build reproducible; artifact published to registry
- [ ] Module ↔ requirement trace matrix complete

## Red Flags

- Writing code before a failing test exists (Core rule 7)
- Implementing "extras" not in design
- Silently renaming design contracts
- Skipping reviews under deadline pressure
- Commenting out failing tests instead of fixing them
- "While I'm here" refactors — stay surgical
- Small helper functions "it's obvious" not in `module_breakdown.md`
- Test passes immediately on first run — means it didn't go RED, violates Core rule 7
