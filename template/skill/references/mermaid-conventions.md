---
doc: skill/references/mermaid-conventions.md
status: draft
required_for: ['phase-3-slice', 'phase-6-CR-implementation']
---

# Diagram convention — Mermaid only (applies to ALL phase docs)

> Read this when authoring or reviewing any diagram in any phase doc.

Every diagram in every phase doc MUST be authored in **Mermaid**. No ASCII art, no PNG screenshots of hand-drawn boxes, no draw.io / Lucidchart / Whimsical exports, no embedded Excalidraw without its source.

## Why Mermaid
- Version-control friendly (plain text diff in PR review).
- Renders natively in GitHub, GitLab, VS Code, and the SDLC_Cowork platform.
- Forces structural thinking — if you can't express it in Mermaid, the diagram is probably trying to do too much.

## Pick the right Mermaid diagram type per artifact

| Doc | Recommended Mermaid type |
| --- | --- |
| `docs/sdlc/02_design/architecture.md` | `flowchart` (components / layers) or `C4Context` / `C4Container` |
| `docs/sdlc/02_design/data_model.md` | `erDiagram` (entities + relationships) |
| `docs/sdlc/02_design/database_design.md` | `erDiagram` (with column types in entity blocks) |
| `docs/sdlc/02_design/sequence_diagrams.md` | `sequenceDiagram` (one per SD-### flow) |
| `docs/sdlc/02_design/ui_design.md` | `flowchart` for navigation, `stateDiagram-v2` for component states |
| `docs/sdlc/03_implementation/development_plan.md` | `gantt` for milestones, `flowchart` for build order |
| `docs/sdlc/04_testing/test_plan.md` | `flowchart` for test strategy, `stateDiagram-v2` for defect lifecycle |
| `docs/sdlc/05_deployment/deployment_plan.md` | `flowchart` for environment topology, `sequenceDiagram` for release steps |
| `docs/sdlc/05_deployment/runbook.md` | `flowchart` for incident decision trees |
| `docs/sdlc/06_maintenance/monitoring.md` | `flowchart` for alert routing |
| `docs/sdlc/06_maintenance/incident_log.md` | `timeline` for incident chronology |

## Authoring rules
1. Wrap every diagram in a fenced code block with `mermaid` language tag — never just ` ``` `.
2. Title diagrams above the fence (e.g., `### SD-001 — User submits draft for review`).
3. If a diagram won't fit (>30 nodes / edges), decompose into multiple diagrams — don't shrink the font.
4. Use `<br/>` for multi-line node labels (not `\n`); quote labels with special characters in `["..."]`.
5. Diagrams are doc content — they're subject to the same sign-off and amendment protocols (Core rules 5-6). A diagram change requires the same change protocol as a prose change.

## Anti-patterns
- ASCII box-drawing in any phase doc — convert to Mermaid before the doc is signed.
- Embedding a screenshot of a Mermaid diagram instead of the Mermaid source — defeats version control.
- Hand-drawing in a graphics tool because "Mermaid can't do this" — usually means the diagram is too complex; decompose.
- Letting diagrams drift from prose — if the prose says "three layers" and the diagram shows four, that's a Bucket B in reconciliation.
