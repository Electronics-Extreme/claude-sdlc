---
doc: docs/sdlc/06_maintenance/change_requests.md
status: template
required_for: ['phase-6-CR-authoring', 'phase-6-CR-implementation', 'phase-6-routine-maintenance']
cite_as: CR
---

# Change Requests (CR)

After Phase-1 sign-off, any requirement or design change enters here. Nothing merges to `main` without an approved CR — unless it's a bug fix or critical security patch.

## Process

1. Requester files a CR entry (template below).
2. Tech Lead classifies: **minor / major / breaking**.
3. Impact assessment: requirements, design, schedule, cost, risk.
4. Approvers sign per the class.
5. Approved CRs are linked to tasks in `docs/sdlc/03_implementation/development_plan.md`.
6. Docs in phases 1/2/3 are updated; requirements change log noted.

## Classes & Approvers

| Class     | Examples                              | Approvers                    |
|-----------|---------------------------------------|------------------------------|
| Minor     | Copy tweak, non-behavioral refactor   | Tech Lead                    |
| Major     | New feature, NFR target shift         | Tech Lead + PO               |
| Breaking  | API change, data migration, SLA shift | Tech Lead + PO + Security    |

## Template

```
CR ID: CR-{{YYYY-NNN}}
Requested by:
Date:
Class: minor / major / breaking
Title:
Summary:
Motivation:
Affected requirements (IDs):
Affected design docs:
Proposed change:
Alternatives considered:
Risks / impact:
Schedule impact:
Cost impact:
Test impact:
Rollback impact:
Decision: approved / rejected / deferred
Approvers:
Decision date:
Implementation ref: PR / task IDs
```

## Register

| ID              | Title                       | Class | Status   | Opened     | Decided    | Design doc                          |
|-----------------|-----------------------------|-------|----------|------------|------------|-------------------------------------|
| CR-{{YYYY-001}} | {{Example CR title}}        | minor | Draft    | {{YYYY-MM-DD}} |        | inline below / `crs/CR-{{YYYY-001}}.md` |

> Large CRs (design doc > ~100 lines) live in `crs/` as standalone files and are linked from the Design-doc column. Small CRs remain inline below.

---

## Filed CRs — inline detail

<!--
Append each small CR body here using the Template format above. Move the full body
into `crs/CR-YYYY-NNN.md` once it exceeds ~100 lines and reference it from the
Register's Design-doc column.
-->
