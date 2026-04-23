# Design Trade-offs

Log major decisions and what we rejected. Pair with full ADRs for high-impact calls.

## Template

### TO-### — {{Decision title}}

- **Context**: {{what's the problem}}
- **Options considered**:
  1. **{{Option A}}** — pros: {{...}}, cons: {{...}}
  2. **{{Option B}}** — pros: {{...}}, cons: {{...}}
- **Decision**: Option {{X}}
- **Rationale**: {{why this wins given our NFRs and constraints}}
- **Consequences**:
  - Positive: {{...}}
  - Negative: {{...}}
- **Revisit when**: {{trigger that would re-open the decision}}

---

## TO-001 — Database choice

- **Context**: Need transactional store with moderate scale (≤ 1M rows/year in largest table).
- **Options considered**:
  1. **Postgres** — pros: ACID, JSONB, mature; cons: vertical scaling ceiling
  2. **MongoDB** — pros: flexible schema; cons: weaker transactions, team unfamiliar
  3. **MySQL** — pros: familiar; cons: weaker JSON support
- **Decision**: Postgres 16
- **Rationale**: ACID + JSON + team skillset + fits CN-03 (existing K8s operators).
- **Consequences**:
  - Positive: strong consistency, easy ops
  - Negative: sharding later will require work
- **Revisit when**: single-node write throughput exceeds {{X}} TPS.

## TO-002 — {{Next decision}}
