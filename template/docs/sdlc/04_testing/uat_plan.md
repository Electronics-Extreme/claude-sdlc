# User Acceptance Testing (UAT)

## Purpose

Stakeholders verify the system meets business needs *as experienced*, not just as implemented.

## Participants

| Role            | Name    | Scope                    |
|-----------------|---------|--------------------------|
| Product Owner   | {{...}} | Overall sign-off         |
| Business User 1 | {{...}} | {{area}}                 |
| Business User 2 | {{...}} | {{area}}                 |
| QA facilitator  | {{...}} | Runs sessions, logs issues |

## Environment

- **Staging** with anonymized prod-like data.
- Accounts pre-created for each participant.

## Scenarios

Each scenario is end-to-end and observable.

### UAT-001 — First-time signup & verification

- **Goal**: A new user can create an account and log in.
- **Steps**: follow UC-001, UC-002.
- **Success**: participant reaches dashboard within one sitting, no assistance needed.

### UAT-002 — {{Next scenario}}
{{...}}

## Session Protocol

1. QA briefs participant (no solution hints).
2. Participant works through scenario; thinks aloud.
3. Observer logs friction, bugs, confusion.
4. Scenario ends in pass / pass-with-notes / fail.

## Sign-off

| Scenario | Result | Notes                | Signed by | Date |
|----------|--------|----------------------|-----------|------|
| UAT-001  |        |                      |           |      |
| UAT-002  |        |                      |           |      |

**Overall UAT decision**: {{Accept / Accept with conditions / Reject}}

**Product Owner signature**: __________________________  **Date**: ___________
