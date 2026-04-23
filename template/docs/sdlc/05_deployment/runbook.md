# Operational Runbook

Answers the questions an on-call engineer asks at 3 AM.

## Quick Reference

- **Dashboards**: {{URLs}}
- **Logs**: {{URL + sample query}}
- **Alerts**: {{URL}}
- **Paging**: {{rotation link}}
- **Escalation**: L1 on-call → L2 tech lead → L3 architect

## Start / Stop / Status

| Action          | Command / procedure                  |
|-----------------|--------------------------------------|
| Check health    | `curl https://{{domain}}/healthz`    |
| Start service   | `{{...}}`                            |
| Stop service    | `{{...}}`                            |
| Restart         | `{{...}}`                            |
| Scale out       | `{{...}}`                            |
| Enter maintenance | `{{flag/flip}}`                    |

## Common Incidents

### High 5xx rate

1. Check {{dashboard link}}: where are errors (service, endpoint)?
2. Check recent deploys in {{link}} — if within 30 min, consider rollback.
3. Check dependency status: {{DB, cache, third-party}}.
4. If DB: check connection pool, slow queries.
5. If third-party: engage fallback or degrade gracefully.
6. Document timeline in incident channel.

### Elevated latency

1. {{dashboard}} — is it global or per-endpoint?
2. DB slow queries: `{{query URL}}`.
3. Cache hit rate dropped? Check {{...}}.
4. Saturation: CPU / memory / connections?
5. Scale out or rollback as appropriate.

### Database incident

1. Page DBA.
2. Check replication lag, disk, connections.
3. If PITR needed, follow DR playbook {{link}}.
4. Communicate RPO impact to stakeholders.

### Security alert

1. Page Security Officer.
2. Isolate affected service (traffic freeze if needed).
3. Preserve evidence — do not restart yet.
4. Follow security incident playbook {{link}}.

## Routine Operations

| Task             | Frequency | How                       |
|------------------|-----------|---------------------------|
| Backup verify    | Weekly    | Restore sample to staging |
| Secret rotation  | {{...}}   | `{{cmd/procedure}}`       |
| Dep update       | Weekly    | Renovate/Dependabot PRs   |
| Capacity review  | Monthly   | {{dashboard}} + forecast  |

## Contacts

| Role              | Primary  | Backup   |
|-------------------|----------|----------|
| SRE on-call       | rotation | rotation |
| Tech Lead         | {{...}}  | {{...}}  |
| Security Officer  | {{...}}  | {{...}}  |
| Product Owner     | {{...}}  | {{...}}  |
