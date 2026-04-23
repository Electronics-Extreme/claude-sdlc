# Defect Log

## Severity Scale

| Level | Meaning                                          | Release-blocking? |
|-------|--------------------------------------------------|-------------------|
| S1    | Data loss, security breach, full outage          | Always            |
| S2    | Major feature broken, no workaround              | Usually           |
| S3    | Minor feature broken, workaround exists          | No                |
| S4    | Cosmetic / tiny polish                           | No                |

## Open Defects

| ID     | Severity | Title                           | Found in  | Reproduce | Owner   | Status     | Target fix |
|--------|----------|---------------------------------|-----------|-----------|---------|------------|------------|
| D-001  | S2       | {{...}}                         | TC-###    | Yes       | {{...}} | In progress| {{date}}   |

## Resolved Defects

| ID     | Severity | Title                           | Resolution           | Closed on |
|--------|----------|---------------------------------|----------------------|-----------|
| D-000  | S3       | {{example}}                     | Fix in PR #{{N}}     | {{date}}  |

## Defect Template

```
ID: D-###
Severity: S1 / S2 / S3 / S4
Title:
Found in: TC-### / manual / prod incident
Environment:
Build / commit:
Steps to reproduce:
Expected:
Actual:
Evidence: (logs, screenshots)
Root cause (filled on fix):
Fix reference: PR / commit
```
