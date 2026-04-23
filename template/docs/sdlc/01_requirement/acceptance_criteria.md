# Acceptance Criteria

The pass/fail conditions that trigger **phase exit**. If any row fails, requirements are not done.

## Phase Exit Checklist

- [ ] All `MUST` functional requirements have a verification method assigned
- [ ] All NFRs have a numeric target
- [ ] Every use case links to ≥ 1 FR
- [ ] Glossary covers every domain term in the SRS
- [ ] Assumptions and constraints reviewed by Tech Lead
- [ ] Security officer reviewed NFR-SEC-*
- [ ] Stakeholders listed in `stakeholders.md` have signed below

## Per-Requirement Acceptance (Gherkin style)

### FR-001 — {{Register account}}

```gherkin
Scenario: Successful registration
  Given a visitor with a valid, unused email
  When they submit the signup form with a strong password
  Then an account is created in "pending_verification" state
  And a verification email is sent within 60 seconds
  And the user sees a confirmation screen
```

```gherkin
Scenario: Duplicate email
  Given an email that already has an account
  When a visitor submits the signup form with that email
  Then no new account is created
  And the user sees "account exists" messaging
```

## Sign-off

| Role             | Name    | Date | Decision (✔ / ✘ / ✘ with conditions) | Notes |
|------------------|---------|------|---------------------------------------|-------|
| Product Owner    | {{...}} |      |                                       |       |
| Tech Lead        | {{...}} |      |                                       |       |
| QA Lead          | {{...}} |      |                                       |       |
| Security Officer | {{...}} |      |                                       |       |
