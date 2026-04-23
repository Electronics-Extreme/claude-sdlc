---
doc: template/04_testing/README.md
status: template
required_for: ['phase-4-test-authoring', 'phase-4-test-execution']
cite_as: README
---

# Phase 4 — Testing (Verification)

> **IRON LAW: NO PHASE-4 SIGN-OFF WITHOUT EVERY AC-### MAPPED TO A PASSING TC-###.**

**Goal:** Prove the built system meets the signed requirements.

## Inputs
- `docs/sdlc/01_requirement/` — requirements to verify
- `docs/sdlc/03_implementation/` — code to test

## Documents

| File              | Purpose                                                    |
|-------------------|------------------------------------------------------------|
| `test_plan.md`    | Scope, strategy, environments, entry/exit criteria         |
| `test_cases.md`   | Detailed cases (TC-###), mapped to FRs/NFRs                |
| `test_data.md`    | Fixtures, seed, PII-safe data                              |
| `test_report.md`  | Execution results, pass/fail, coverage                     |
| `defect_log.md`   | Bugs found, severity, status, owner                        |
| `uat_plan.md`     | User Acceptance Testing scenarios & sign-off               |

## Test Levels

| Level       | Scope                   | Tooling            | Owner     |
|-------------|-------------------------|--------------------|-----------|
| Unit        | Single fn/class         | {{Vitest/pytest}}  | Dev       |
| Integration | Module + deps           | {{...}}            | Dev       |
| System / E2E| Full stack              | {{Playwright}}     | QA        |
| Performance | Latency, throughput     | {{k6 / Locust}}    | QA / SRE  |
| Security    | Vuln scans, pen test    | {{OWASP ZAP}}      | Security  |
| Usability   | Real-user flows         | Observed sessions  | UX / PO   |
| UAT         | Stakeholder acceptance  | Scripted demos     | PO        |

## Exit Criteria

- [ ] 100% of `MUST` FRs have ≥ 1 passing test case
- [ ] All NFR targets verified with evidence
- [ ] 0 open Severity-1 defects, Severity-2 triaged with plan
- [ ] Test coverage meets NFR-MNT-01
- [ ] UAT signed by Product Owner

## Red Flags

- "Tested manually, LGTM" without a recorded case
- Disabling flaky tests instead of fixing them
- UAT during the deployment window
- "Tests pass, that's enough" — four gates still apply (typecheck + lint + tests + reconciliation)
- NFR targets "intuitively met" without measurement
- Defect log treated as optional paperwork
- Test data ad-hoc rather than in `test_data.md`
- No traceability from AC to TC to code
