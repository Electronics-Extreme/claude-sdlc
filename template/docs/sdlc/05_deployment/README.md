---
doc: template/05_deployment/README.md
status: template
required_for: ['phase-5-deploy-prep', 'phase-5-release-cutting']
cite_as: README
---

# Phase 5 — Deployment

> **IRON LAW: NO DEPLOY WITHOUT ROLLBACK PLAN + SMOKE TESTS + SIGNED RUNBOOK.**

**Goal:** Ship the tested system to production safely, with a rollback plan that actually works.

## Inputs
- `docs/sdlc/03_implementation/` — signed artifacts
- `docs/sdlc/04_testing/` — passing results, UAT signed

## Documents

| File                   | Purpose                                            |
|------------------------|----------------------------------------------------|
| `deployment_plan.md`   | Who, what, when, how                               |
| `release_notes.md`     | User-facing + internal changelog                   |
| `rollback_plan.md`     | How to revert within RTO                           |
| `runbook.md`           | Operational procedures (start, stop, incident)     |
| `smoke_tests.md`       | Post-deploy verification script                    |
| `go_live_checklist.md` | Final sign-offs before flipping the switch         |

## Exit Criteria

- [ ] Production smoke tests green
- [ ] Monitoring & alerts confirmed firing correctly
- [ ] Rollback tested in staging within the window
- [ ] On-call engineer identified, paged-in, acknowledged
- [ ] Stakeholders notified of go-live

## Red Flags

- Friday afternoon deploys
- Untested rollback paths
- "It worked in staging" without a smoke test in prod
- Runbook is tribal knowledge, not a committed doc
- Rollback plan is just "git revert" — not tested
- Deploy without release notes ("users will figure it out")
- Quiet deploys with no comms
- Monitoring + alerting not verified firing before go-live
