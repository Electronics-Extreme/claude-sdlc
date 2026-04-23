---
doc: template/01_requirement/README.md
status: template
required_for: ['phase-1-artifact-authoring']
cite_as: README
---

# Phase 1 — Requirements

> **IRON LAW: NO DESIGN WORK UNTIL SRS IS SIGNED.**

**Goal:** Capture *what* the system must do and *why*, with no solution details.

## Documents in this phase

| File                             | Purpose                                              |
|----------------------------------|------------------------------------------------------|
| `srs.md`                         | Software Requirements Specification (master doc)     |
| `stakeholders.md`                | Who cares, what they need, how they sign off         |
| `use_cases.md`                   | Actor-goal scenarios                                 |
| `functional_requirements.md`     | Numbered FR-### items, testable                      |
| `non_functional_requirements.md` | Performance, security, usability, compliance         |
| `acceptance_criteria.md`         | Pass/fail conditions that trigger phase exit         |
| `assumptions_and_constraints.md` | What we assume true; what limits us                  |
| `glossary.md`                    | Domain terms — one definition, used everywhere       |

## Exit Criteria

- [ ] Every requirement has a unique ID (FR-### / NFR-###)
- [ ] Every requirement is testable (no "fast", "user-friendly" without metrics)
- [ ] Stakeholders have signed `acceptance_criteria.md`
- [ ] Glossary covers every domain term used in the SRS
- [ ] Baseline snapshot tagged: `req-v1.0`

## Red Flags

- Solution language ("use Redis", "React component") — belongs in Design
- Vague requirements ("system should be secure") with no numeric target
- Undocumented assumptions hiding in FR prose
- "We discussed it in chat" — conversation ≠ signed artifact
- NFR targets pushed to Phase 2 or later ("we'll measure once it's built")
- Skipping glossary because "terms are obvious"
- Stakeholder sign-off treated as bureaucracy
