# Test Plan

## 1. Scope

- **In scope**: All `MUST` FRs, all NFRs, all critical UI flows.
- **Out of scope**: {{deferred features}}, third-party services internals (mocked or verified via contract tests).

## 2. Strategy

| Level        | What it proves                        | When run                 |
|--------------|---------------------------------------|--------------------------|
| Unit         | Logic correctness                     | Every commit (CI)        |
| Integration  | Wiring between modules + DB           | Every commit (CI)        |
| Contract     | API shape stable                      | Every commit             |
| E2E          | User flow end-to-end                  | Every merge to main      |
| Performance  | Meets NFR-PRF-*                       | Nightly + before release |
| Security     | No critical CVEs, OWASP top-10 clean  | Weekly + before release  |
| Accessibility| WCAG 2.2 AA                           | Before release           |
| UAT          | Stakeholder acceptance                | Before release           |

## 3. Environments

| Env     | Purpose            | Data                    |
|---------|--------------------|-------------------------|
| local   | Dev-driven         | Seed fixtures           |
| CI      | Automated suites   | Ephemeral DB per job    |
| staging | Pre-prod mirror    | Anonymized snapshot     |
| prod    | Smoke tests only   | Live (read-only checks) |

## 4. Entry Criteria

- Code frozen for the release candidate
- Baseline build passes unit + integration in CI
- Test environment provisioned with required fixtures
- Test cases reviewed

## 5. Exit Criteria

See `README.md` exit checklist.

## 6. Schedule

| Stage            | Start        | End          | Owner  |
|------------------|--------------|--------------|--------|
| System testing   | {{date}}     | {{date}}     | QA     |
| Performance      | {{date}}     | {{date}}     | SRE    |
| Security         | {{date}}     | {{date}}     | Sec    |
| UAT              | {{date}}     | {{date}}     | PO     |

## 7. Risks

| Risk                                | Mitigation                   |
|-------------------------------------|------------------------------|
| Flaky E2E                           | Retry once; quarantine; owner assigned |
| Data skew between staging and prod  | Weekly anonymized refresh    |
| Late-discovered NFR miss            | Early perf baseline in M1    |

## 8. Deliverables

- `test_cases.md`
- `test_report.md` (updated per run)
- `defect_log.md`
- UAT sign-off document
