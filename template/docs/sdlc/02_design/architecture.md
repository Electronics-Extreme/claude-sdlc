# System Architecture

## 1. Context Diagram (C4 Level 1)

```
[External User] ──▶ [{{System}}] ──▶ [{{External Svc A}}]
                           │
                           └──▶ [{{External Svc B}}]
```

**Boundaries**: what's inside the system vs. outside.

## 2. Container Diagram (C4 Level 2)

List each deployable unit:

| Container         | Tech                 | Responsibility                    | Talks to           |
|-------------------|----------------------|-----------------------------------|--------------------|
| Web frontend      | {{Next.js}}          | UI, session handling              | API Gateway        |
| API Gateway       | {{FastAPI / Express}}| Auth, routing, rate limit         | Services, DB       |
| {{Service X}}     | {{...}}              | {{...}}                           | DB, Queue          |
| Database          | {{Postgres 16}}      | Persistence                       | —                  |
| Cache             | {{Redis}}            | Session + hot data                | API Gateway        |
| Message queue     | {{SQS / Kafka}}      | Async jobs                        | Workers            |

## 3. Component Diagram (C4 Level 3)

For each container, list internal components and their roles.

## 4. Data Flow

Describe the golden-path request end-to-end. Reference `sequence_diagrams.md`.

## 5. Cross-cutting Concerns

| Concern          | Approach                                             | NFR mapping    |
|------------------|------------------------------------------------------|----------------|
| AuthN/AuthZ      | {{OIDC via X, RBAC}}                                 | NFR-SEC-03     |
| Logging          | {{Structured JSON → central store}}                  | NFR-OBS-01     |
| Metrics          | {{Prometheus + Grafana}}                             | NFR-OBS-02     |
| Tracing          | {{OpenTelemetry}}                                    |                |
| Config           | {{Env vars + secret store}}                          |                |
| Error handling   | {{Typed errors, boundary logging}}                   |                |
| Rate limiting    | {{per-IP + per-token}}                               | NFR-SEC        |

## 6. Deployment Topology

- Environments: {{dev, staging, prod}}
- Regions: {{...}}
- Scaling model: {{horizontal / vertical, autoscaling rules}}

## 7. Technology Choices (headline)

Full rationale in `trade_offs.md`.

| Concern   | Choice      | Alternatives considered |
|-----------|-------------|-------------------------|
| Language  | {{...}}     | {{...}}                 |
| DB        | {{...}}     | {{...}}                 |
| Cache     | {{...}}     | {{...}}                 |
