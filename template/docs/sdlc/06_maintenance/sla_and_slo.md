# SLA, SLO, SLI

- **SLI** — what you measure
- **SLO** — internal target on the SLI
- **SLA** — external commitment (usually looser than SLO)

## Availability

| Item | Value                                    |
|------|------------------------------------------|
| SLI  | Successful request rate over total       |
| SLO  | ≥ 99.9% monthly                          |
| SLA  | ≥ 99.5% monthly (customer-facing commitment) |
| Error budget | 0.1% per month = {{43 min 49 s}}  |

## Latency

| Item | Value                                     |
|------|-------------------------------------------|
| SLI  | p95 end-to-end API latency                |
| SLO  | ≤ 200 ms (NFR-PRF-01)                     |
| SLA  | ≤ 400 ms                                  |

## Durability

| Item | Value                                     |
|------|-------------------------------------------|
| SLI  | Successful recoverability from backup     |
| SLO  | RPO ≤ 5 min (NFR-AVL-02)                  |
| SLA  | RPO ≤ 15 min                              |

## Error Budget Policy

- If monthly error budget is exhausted, **all feature rollouts pause** until next window.
- Only reliability work and security patches may merge during freeze.
- Budget status published weekly on {{dashboard}}.

## Reporting

- Monthly SLO report to PO + stakeholders.
- Quarterly review with Tech Lead + SRE.
- Annual SLA review with customers (if applicable).
