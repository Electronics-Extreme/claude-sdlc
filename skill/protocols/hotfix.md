---
doc: skill/protocols/hotfix.md
status: draft
required_for: ['phase-3-slice', 'phase-6-CR-implementation']
---

# The hotfix protocol (production incidents only)

> Read this only when a live system is broken or degraded against its SLO. Strict waterfall does not survive contact with a burning production. A narrow emergency lane exists for true incidents — but only for them.

## When this applies (ALL must be true)
- A live system is broken or degraded against its SLO.
- The fix is small (typically < 50 LoC) and scoped to **restoring documented behavior**.
- Waiting for a full requirements → design → impl → test cycle would extend user impact materially.

## When this does NOT apply
- New features, even small ones — full cycle.
- Refactors, cleanups, "drive-by" fixes co-located with the hotfix.
- Anything that changes the documented contract (API shape, schema, response codes) — those go through the change protocol, even mid-incident.
- Urgent feature requests. Urgency ≠ incident.

## The hotfix workflow
1. **Open `docs/sdlc/06_maintenance/incident_log.md`** entry: timestamp, severity, scope, oncall.
2. **Branch** `hotfix/inc-<incident-id>` from the deployed tag (not from `main` if `main` has un-released work).
3. **Reproduce locally** before fixing. If you can't reproduce, the fix is speculation — STOP.
4. **Failing regression test first.** Same TDD rule as Phase 3 — incidents are not an excuse to skip it. The test is what stops the bug recurring.
5. **Minimum fix.** No cleanup. No refactor. Restore documented behavior.
6. **Gate checks**: typecheck → lint → tests → smoke in staging.
7. **Deploy** per the abbreviated path in `runbook.md` (the hotfix lane).
8. **Post-hoc reconciliation within 24h.** Open a Bucket-A entry in `divergences.md` for the next reconciliation pass; if the incident revealed a doc-vs-reality gap, file the doc amendment via the change protocol then.
9. **Post-mortem** in the incident entry: timeline, root cause, fix, prevention, follow-up tasks (rolled forward as TO-### or CR-###).

## Anti-patterns
- "While I'm here, let me also fix X" — NO. Hotfix is surgical.
- Skipping the regression test "because we need to ship now" — NO.
- Skipping the post-hoc reconciliation "because the fix is in" — NO. Hotfixes are the highest-risk source of doc drift.
