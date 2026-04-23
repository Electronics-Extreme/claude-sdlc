# Rollback Plan

A rollback plan that has never been exercised is a hope, not a plan.

## Trigger Conditions

Execute rollback if **any** of the following within {{window}} of deployment:

- 5xx rate > 1% sustained 2 min
- p95 latency > 2× baseline for 5 min
- New unique error signature at high volume
- Business KPI regresses > 20% vs baseline
- Security alert on the new version
- On-call judgment call (document reason)

## Pre-requisites

- [ ] Previous version's artifact still in registry
- [ ] DB migrations follow expand/contract — expand applied before deploy, contract deferred
- [ ] Feature flags default to **off** for new behavior — instant kill switch
- [ ] Rollback procedure tested in staging within last {{N}} days

## Procedure

### Code rollback (no schema change)

1. Announce rollback in incident channel.
2. `{{deploy cmd}} --version {{previous}}`.
3. Watch 5xx + latency return to baseline (≤ 5 min).
4. Run smoke tests against previous version.
5. Post-mortem scheduled within {{48h}}.

### Code + schema rollback

**Only if migrations are reversible (designed that way).** Prefer code rollback + leave schema expanded.

1. Disable new features via flag (instant).
2. Deploy previous version.
3. If schema must revert: run `{{migrate down}}` and verify.
4. Smoke tests.
5. Post-mortem.

### Catastrophic recovery (data corruption)

1. Page SRE lead + DBA.
2. Stop writes (put app in maintenance mode).
3. Restore from most recent backup (RPO ≤ {{minutes}}).
4. Reconcile writes between backup and incident start from event log / WAL.
5. Resume writes; run data integrity checks.
6. Full post-mortem and customer comms.

## Communication

| Time                 | Channel          | Message                                   |
|----------------------|------------------|-------------------------------------------|
| T-0 (decision)       | Incident channel | "Rolling back {{version}} due to {{...}}" |
| T+5 min              | Incident channel | Progress update                           |
| On completion        | Incident + email | Status + root cause investigation ETA     |
| After post-mortem    | Email / blog     | Public summary if user-visible impact     |

## RTO budget

- Detection → decision: ≤ {{N}} min
- Decision → rolled back: ≤ {{N}} min
- Total service impact: ≤ NFR-AVL-03 RTO
