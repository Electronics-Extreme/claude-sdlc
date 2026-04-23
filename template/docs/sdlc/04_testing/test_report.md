# Test Report

Append a new section per test run. Keep history — do not overwrite prior runs.

## Template

### Run {{YYYY-MM-DD HH:MM}} — {{build/tag}}

- **Environment**: {{staging / CI}}
- **Build**: {{commit SHA or tag}}
- **Executor**: {{name or CI job URL}}

#### Summary

| Level        | Total | Pass | Fail | Skipped | Coverage |
|--------------|-------|------|------|---------|----------|
| Unit         |       |      |      |         |          |
| Integration  |       |      |      |         |          |
| E2E          |       |      |      |         |          |
| Performance  |       |      |      |         | —        |
| Security     |       |      |      |         | —        |

#### Failures

| TC ID | Failure summary         | Defect ID  |
|-------|-------------------------|------------|
|       |                         |            |

#### NFR Verification Evidence

| NFR ID     | Target         | Measured | Pass? | Notes / artifact |
|------------|----------------|----------|-------|------------------|
| NFR-PRF-01 | p95 ≤ 200 ms   |          |       | k6 report link   |
| NFR-AVL-01 | ≥ 99.9%        |          |       | monitoring link  |

#### Notes
{{observations, anomalies, follow-ups}}

---

## Run 2026-04-17 13:00 — v0.1.0-rc.1

_{{fill in results}}_
