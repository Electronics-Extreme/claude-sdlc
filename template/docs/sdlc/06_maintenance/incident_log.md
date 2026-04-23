# Incident Log

Append-only. Never rewrite history. One entry per incident.

## Template

### INC-{{YYYY-NNNN}} — {{Short title}}

- **Date / time (UTC)**: {{start}} → {{end}}  (Duration: {{...}})
- **Severity**: SEV-1 / SEV-2 / SEV-3
- **Detected by**: alert / customer / internal
- **Status**: Investigating / Mitigated / Resolved / Closed
- **Commander**: {{name}}
- **Services affected**: {{...}}
- **User impact**: {{who, how many, what broke}}
- **NFR breach**: {{e.g. NFR-AVL-01 — uptime dipped to 99.6% this month}}

#### Timeline

| Time (UTC) | Event                                    |
|------------|------------------------------------------|
| HH:MM      | Alert fired: {{...}}                     |
| HH:MM      | On-call acked, began investigation       |
| HH:MM      | Root cause suspected: {{...}}            |
| HH:MM      | Mitigation applied: {{rollback / flag}}  |
| HH:MM      | Metrics returned to baseline             |
| HH:MM      | Incident closed                          |

#### Root Cause

{{What — technical. Why — the reason *that* happened. Why — deeper, up to five whys.}}

#### What went well
- {{...}}

#### What went poorly
- {{...}}

#### Action items (blameless, assigned)

| # | Action                                       | Owner   | Due        | Done? |
|---|----------------------------------------------|---------|------------|-------|
| 1 | Add alert for {{missing signal}}             | {{...}} | {{date}}   |       |
| 2 | Add regression test                          | {{...}} | {{date}}   |       |
| 3 | Update runbook with this scenario            | {{...}} | {{date}}   |       |

---

## Index

| ID               | Date        | SEV | Title                     | Status  |
|------------------|-------------|-----|---------------------------|---------|
| INC-2026-0001    | 2026-04-17  | 3   | {{example}}               | Closed  |
