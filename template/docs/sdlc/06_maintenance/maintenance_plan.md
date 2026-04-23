# Maintenance Plan

## Cadences

| Activity                    | Frequency | Owner     | Output                           |
|-----------------------------|-----------|-----------|----------------------------------|
| Dependency updates          | Weekly    | Dev team  | PRs from Renovate/Dependabot     |
| Security patches (critical) | Within 24h| Security  | Hotfix release                   |
| OS / base image refresh     | Monthly   | SRE       | New base image + redeploy        |
| Backup restore drill        | Quarterly | SRE + DBA | Restore report                   |
| DR drill (full failover)    | Bi-annually | SRE     | DR report                        |
| Capacity review             | Monthly   | SRE       | Updated forecast                 |
| Cost review                 | Monthly   | SRE + PO  | Cost report                      |
| Architecture review         | Quarterly | Tech Lead | Updated architecture.md          |
| Pen test                    | Annually  | Security  | Findings + remediation plan      |

## Patch Classification

| Class         | SLA         | Requires CR?         |
|---------------|-------------|----------------------|
| Critical sec  | ≤ 24h       | No (retroactive)     |
| High sec      | ≤ 7d        | Yes (lightweight)    |
| Bug fix (S1)  | ≤ 24h       | No                   |
| Bug fix (S2)  | Next sprint | No                   |
| Enhancement   | Roadmap     | Yes                  |
| Dep minor/patch | Weekly    | No                   |
| Dep major     | Planned     | Yes                  |

## Technical Debt

- Tracked in {{issue tracker}} with `tech-debt` label.
- Each sprint allocates {{20%}} capacity to debt + maintenance.
- Quarterly review of highest-risk items with Tech Lead.

## Documentation Hygiene

- Whenever code diverges from docs in phases 1–3, **the doc wins** or it is updated. No "code is the spec" drift.
- Runbook reviewed after every incident.
