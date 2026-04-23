# Functional Requirements

Each requirement is **testable**, **atomic**, and **unambiguous**. One FR per row.

## Format

- **ID**: `FR-###` (stable, never renumber)
- **Priority**: `MUST` / `SHOULD` / `MAY` (MoSCoW)
- **Source**: which stakeholder or use case this comes from
- **Verification**: how we'll prove it works (test case ID, demo, inspection)

## Table

| ID     | Priority | Requirement                                                              | Source  | Verification |
|--------|----------|--------------------------------------------------------------------------|---------|--------------|
| FR-001 | MUST     | {{System SHALL allow a user to register with email + password}}          | UC-001  | TC-001       |
| FR-002 | MUST     | {{System SHALL send a verification email within 60 seconds of signup}}   | UC-001  | TC-002       |
| FR-003 | SHOULD   | {{System SHOULD support SSO via Google}}                                 | SH-01   | TC-010       |
| FR-004 | MUST     | {{...}}                                                                  |         |              |

## Writing rules

- Use `SHALL` for MUST, `SHOULD` for SHOULD, `MAY` for optional.
- No ambiguous adjectives: replace "fast", "intuitive", "robust" with numbers.
- One requirement per row — if you see "and", split it.
- Never reference implementation (no "use Postgres", "use JWT").

## Change log

| Date       | ID     | Change                  | Approved by |
|------------|--------|-------------------------|-------------|
| {{YYYY-MM-DD}} | FR-001 | Created                 | {{...}}     |
