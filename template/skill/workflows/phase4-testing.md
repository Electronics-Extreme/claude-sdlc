---
doc: skill/workflows/phase4-testing.md
status: draft
required_for: ['phase-3-slice', 'phase-6-CR-implementation']
---

# Phase 4 — Testing workflow + NFR validation

> Read this when Phase 3 is signed and you're moving to Phase 4. NOT for "rerun unit tests" — Phase 4 is system-level proof: end-to-end behavior, NFR validation, UAT, defect triage.

## Step 1 — Verify Phase 3 sign-off
Phase 4 cannot start until Phase 3 is signed AND its reconciliation gate is closed.

## Step 2 — Read the test plan
Open `docs/sdlc/04_testing/test_plan.md`. Confirm scope, test environments, pass criteria, defect-handling rules.

## Step 3 — Execute test cases
Run every TC-### in `test_cases.md`. For each:
- Record actual result (pass / fail / blocked) in `test_report.md` with a timestamped run section.
- Failures → file an entry in `defect_log.md` with TC-### + AC-### back-refs and severity.

## Step 4 — Validate NFRs (see "NFR validation" below)
Every NFR-### must have a validation entry. Unvalidated NFRs are aspirational, not requirements.

## Step 5 — UAT (if applicable)
Walk `uat_plan.md` with the user / stakeholder. Their sign-off is the user's, not yours.

## Step 6 — Reconciliation gate
Run `reconciliation.md` against Phase 4 artifacts: test cases vs ACs, test results vs NFRs, defect log open items.

## Step 7 — Phase sign-off
User signs `test_report.md` (or per-phase equivalent). Phase 5 opens.

## NFR validation (during Phase 4)

NFRs from `docs/sdlc/01_requirement/non_functional_requirements.md` must be validated, not just declared. Map each NFR-### to a validation method:

| NFR category | Typical validation | Evidence artifact |
| --- | --- | --- |
| **Performance** | Load test (k6 / JMeter / Vegeta), p50/p95/p99 latency budgets | `docs/sdlc/04_testing/perf_baseline.json` |
| **Security** | SAST scan (semgrep / Snyk), dep audit (`pnpm audit` / `cargo audit`), threat-model review | `docs/sdlc/04_testing/security_report.md` |
| **Accessibility** | axe / Lighthouse a11y, keyboard-nav walkthrough, screen-reader spot-check | `docs/sdlc/04_testing/a11y_report.md` |
| **Reliability** | Chaos / fault injection in non-prod, restore-from-backup drill | `docs/sdlc/04_testing/reliability_report.md` |
| **Observability** | Verify each documented log line / metric / trace appears where promised | `docs/sdlc/04_testing/observability_report.md` |

Rules:
1. Every NFR-### must have a validation entry. No exceptions.
2. Pass / fail recorded in `test_report.md` citing NFR-### + evidence artifact path.
3. **Fail → Bucket A in reconciliation** — code violating an NFR is the same as code violating any other documented rule.
4. If an NFR can't be measured (e.g., "fast" with no number), STOP and amend Phase 1 first. An unmeasurable NFR is a writing bug.
