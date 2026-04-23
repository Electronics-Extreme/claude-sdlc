---
doc: template/02_design/README.md
status: template
required_for: ['phase-2-artifact-authoring', 'phase-3-slice']
cite_as: README
---

# Phase 2 — Design

> **IRON LAW: NO IMPLEMENTATION UNTIL DESIGN IS SIGNED.**

**Goal:** Translate requirements into *how* the system is built, without writing production code.

## Inputs
- `docs/sdlc/01_requirement/` — frozen and signed

## Documents

| File                   | Purpose                                              |
|------------------------|------------------------------------------------------|
| `architecture.md`      | High-level components, boundaries, data flow         |
| `database_design.md`   | Schemas, keys, indexes, retention                    |
| `api_design.md`        | Endpoints or message contracts                       |
| `ui_design.md`         | Screens, states, navigation                          |
| `data_model.md`        | Domain entities, relationships, invariants           |
| `sequence_diagrams.md` | Request/response and event flows                     |
| `trade_offs.md`        | Alternatives considered, why rejected               |

## Exit Criteria

- [ ] Every FR maps to ≥ 1 component or endpoint
- [ ] Every NFR has a design decision addressing it (performance, security, etc.)
- [ ] Interfaces are versioned and documented
- [ ] Non-trivial decisions have an ADR in `documentation-and-adrs` (or a row in `trade_offs.md`)
- [ ] Tech Lead + Architect sign-off

## Red Flags

- "Architecture fits in my head" — undocumented assumption
- API contract defined while coding — should precede impl
- Trade-offs captured verbally in meetings, not in `trade_offs.md`
- Diagrams shipped as screenshots (must be Mermaid per `references/mermaid-conventions.md`)
- Skipping `data_model.md` because "it's just CRUD"
- Designing around a favorite framework rather than the requirement
- Skipping the NFR → design mapping (then finding the system can't meet SLOs)
- "We'll figure out the schema later"
