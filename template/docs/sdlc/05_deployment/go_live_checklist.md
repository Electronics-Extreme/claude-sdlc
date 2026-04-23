# Go-Live Checklist

Sign each item. If you can't tick a box, you don't go live.

## Code & Build
- [ ] Release tagged (`v{{...}}`)
- [ ] Artifact built from tagged commit, published, signed
- [ ] No open S1/S2 defects

## Test & Quality
- [ ] All mandatory test suites green in CI
- [ ] UAT signed by Product Owner
- [ ] Performance NFRs verified in staging
- [ ] Security scan clean (no criticals)

## Infrastructure
- [ ] Capacity headroom ≥ {{%}} for current peak
- [ ] Scaling policies verified
- [ ] TLS certificates valid > 30 days
- [ ] DB backups verified restorable

## Observability
- [ ] Dashboards cover new code paths
- [ ] Alerts tuned, acknowledged routes
- [ ] Log sampling set appropriately
- [ ] Trace sampling enabled

## Security
- [ ] Secrets rotated where required
- [ ] New endpoints behind proper AuthZ
- [ ] Rate limits applied
- [ ] Dependency scan clean

## Operations
- [ ] Runbook updated
- [ ] Rollback tested in staging
- [ ] On-call briefed and available
- [ ] Feature flags defaults confirmed

## Compliance / Legal
- [ ] Privacy notice updated if data handling changed
- [ ] Data residency verified
- [ ] Audit logging enabled

## Communication
- [ ] Stakeholders notified (T-24h)
- [ ] Support / CS briefed with FAQ
- [ ] Status page scheduled maintenance (if applicable)
- [ ] Release notes published to {{channel}}

## Final sign-off

| Role              | Name    | Decision | Date |
|-------------------|---------|----------|------|
| Tech Lead         | {{...}} |          |      |
| QA Lead           | {{...}} |          |      |
| Security Officer  | {{...}} |          |      |
| SRE               | {{...}} |          |      |
| Product Owner     | {{...}} |          |      |
