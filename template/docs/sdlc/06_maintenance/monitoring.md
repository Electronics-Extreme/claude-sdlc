# Monitoring & Alerting

## Four Golden Signals

| Signal       | Metric                               | Dashboard | Alert threshold                   |
|--------------|--------------------------------------|-----------|-----------------------------------|
| Latency      | p50, p95, p99 per endpoint           | {{link}}  | p95 > 200ms sustained 5 min       |
| Traffic      | req/s                                | {{link}}  | Sudden drop > 50% vs baseline     |
| Errors       | 5xx rate                             | {{link}}  | > 1% sustained 2 min              |
| Saturation   | CPU, memory, DB connections          | {{link}}  | > 80% sustained 10 min            |

## Business Metrics

| Metric                          | Threshold                | Owner   |
|---------------------------------|--------------------------|---------|
| Signup completion rate          | drop > 20% vs 7-day avg  | PO      |
| Login success rate              | < 98%                    | PO      |
| {{Core KPI}}                    | {{...}}                  | {{...}} |

## Logs

- Central log store: {{Loki / ELK / Datadog}}
- Retention: {{30 days hot, 1 year cold}}
- PII scrubbed at ingest — verify in pipeline

## Tracing

- OpenTelemetry SDK in all services
- Sample rate: {{10% baseline, 100% for errors}}

## Alert Hygiene

- Every alert must have a **runbook link**.
- Symptom-based, not cause-based (alert on user impact, not on a stuck queue).
- No flapping alerts — silence and fix, don't tolerate.
- Quarterly review: delete or rewrite alerts that didn't page a real problem.

## Escalation

1. Primary on-call — 5 min ACK
2. Secondary on-call — 15 min
3. Tech Lead — 30 min
4. Incident Commander activated for SEV-1/2

## Status Page

- Public status: {{URL}}
- Update within {{5 min}} of SEV-1 confirmed
- Post-mortem summary within {{5 business days}}
