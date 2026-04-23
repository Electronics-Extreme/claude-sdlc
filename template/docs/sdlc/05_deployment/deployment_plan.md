# Deployment Plan

## Release Identity

- **Version**: `v{{MAJOR.MINOR.PATCH}}`
- **Artifact**: {{container image / binary}} `{{registry/repo@sha256:...}}`
- **Build provenance**: {{CI job URL}}
- **Target env**: production
- **Window**: {{YYYY-MM-DD HH:MM}} – {{HH:MM}} ({{timezone}})

## Strategy

- **Type**: {{blue-green | canary | rolling | recreate}}
- **Canary ramp**: {{5% → 25% → 50% → 100% with X-min bake at each step}}
- **Feature flags**: {{list flags default-off vs default-on}}
- **Traffic routing**: {{load balancer / service mesh rule}}

## Pre-deployment

- [ ] `docs/sdlc/04_testing/` exit criteria met
- [ ] Release notes drafted
- [ ] Rollback plan reviewed and dry-run in staging
- [ ] DB migrations applied in staging, verified reversible
- [ ] Secrets / config rotated if required
- [ ] On-call briefed, extra coverage scheduled
- [ ] Stakeholder comms queued

## Deployment Steps

1. Freeze merges to `main`.
2. Tag release: `git tag v{{...}} && git push --tags`.
3. CI builds and publishes artifact → registry.
4. Apply DB migrations (expand step) — verify.
5. Deploy new version to canary.
6. Observe: error rate, latency, business metrics. Bake {{X}} minutes.
7. Promote to {{next ramp step}}. Repeat observe.
8. Promote to 100%.
9. Run post-deploy smoke tests (see `smoke_tests.md`).
10. Apply contract step of migrations (drop old columns, etc.) — next window if needed.
11. Unfreeze `main`.
12. Notify stakeholders.

## Observability during rollout

| Signal                | Threshold to abort              |
|-----------------------|---------------------------------|
| 5xx rate              | > 1% sustained 2 min            |
| p95 latency           | > 2× baseline sustained 5 min   |
| Error logs            | new unique error signature       |
| Business KPI (e.g. signup success) | drop > 20% vs baseline |

## Stakeholders & Comms

| When                 | Channel          | Audience          |
|----------------------|------------------|-------------------|
| T-24h                | Email / Slack    | All teams         |
| T-0 (start)          | Incident channel | Eng + SRE + PO    |
| Rollout milestones   | Incident channel | Eng + SRE         |
| Complete / aborted   | Email / Slack    | All teams + users |
