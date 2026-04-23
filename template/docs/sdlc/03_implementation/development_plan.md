# Development Plan

Vertical slices ordered by dependency. Every task has an owner, an estimate, and an acceptance condition.

## Milestones

| ID  | Milestone             | Target date     | Dependencies | Exit |
|-----|-----------------------|-----------------|--------------|------|
| M1  | Project scaffold      | {{YYYY-MM-DD}}  | —            | Build + CI green |
| M2  | Auth + registration   | {{...}}         | M1           | UC-001 E2E green |
| M3  | {{Core feature 1}}    | {{...}}         | M2           | {{...}}          |
| M4  | {{Core feature 2}}    | {{...}}         | M3           | {{...}}          |
| M5  | Hardening + NFRs      | {{...}}         | M4           | NFRs verified    |
| M6  | UAT readiness         | {{...}}         | M5           | Phase 4 entry    |

## Task Board (snapshot — live tool is the source of truth)

| ID    | Task                                       | Module   | Est | Owner   | Depends on | Status |
|-------|--------------------------------------------|----------|-----|---------|------------|--------|
| T-001 | Scaffold repo, CI, lint, format            | —        | 1d  | {{...}} | —          | Done   |
| T-002 | DB migration framework + `users` table     | db/users | 0.5d| {{...}} | T-001      | Done   |
| T-003 | POST /v1/users (FR-001)                    | users/api| 1d  | {{...}} | T-002      | Todo   |
| T-004 | Verification email (FR-002)                | mail     | 1d  | {{...}} | T-003      | Todo   |

## Working Agreements

- Thin vertical slices: each PR delivers one observable behavior.
- No more than 2 PRs in flight per engineer.
- Review SLA: first response within 1 business day.
- Green CI required to merge. No exceptions.
- Every task ends with: test proof + demo note in PR.
