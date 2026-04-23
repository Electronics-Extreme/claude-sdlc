---
doc: template/06_maintenance/README.md
status: template
required_for: ['phase-6-CR-authoring', 'phase-6-CR-implementation', 'phase-6-routine-maintenance']
cite_as: README
---

# Phase 6 — Maintenance

> **IRON LAW: NO CODE CHANGE WITHOUT A SIGNED CR-### FIRST.**

**Goal:** Keep the system healthy, secure, and evolving without degrading earlier phases' guarantees.

## Inputs
- Everything signed in phases 1–5
- Production telemetry

## Documents

| File                   | Purpose                                              |
|------------------------|------------------------------------------------------|
| `maintenance_plan.md`  | Cadences: patching, reviews, reviews, capacity       |
| `incident_log.md`      | Production incidents + post-mortems                  |
| `change_requests.md`   | Formal CRs after requirements were frozen            |
| `sla_and_slo.md`       | Service level objectives + error budget              |
| `monitoring.md`        | What we watch, thresholds, escalation                |
| `eol_policy.md`        | Version support, deprecation, sunset                 |

## Operating principles

1. **Any change re-opens the relevant phase's doc** — never patch code without reflecting in the spec.
2. **Incidents feed post-mortems; post-mortems feed guardrails.** Never blame; always improve a system.
3. **Security patches are first-class work** — same discipline as features.
4. **Monitor the NFRs you signed** — if you can't see them, you aren't meeting them.

## Red Flags

- Letting tech debt compound silently
- "We'll upgrade that dependency next sprint" × 24 sprints
- Fixing a bug without a regression test
- Post-mortems that blame individuals
- "Just 2 lines, no CR" — scope creep starts at small (Core rule 10)
- Urgent-feature treated as hotfix (urgency ≠ incident)
- Incident log written after the fire, not during
- Monitoring dashboards "later" (NFRs unmeasured ≠ met)
- EOL only considered when a user complains
