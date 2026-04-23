# Code Review Checklist

Five axes. A PR merges only when reviewer has considered each.

## 1. Correctness
- [ ] Does it do what the linked requirement / design says?
- [ ] Edge cases handled (empty, null, max, boundary, concurrent)?
- [ ] Errors propagated or handled — none silently swallowed?
- [ ] Tests cover the behavior, not the implementation?

## 2. Readability
- [ ] Names reveal intent without needing comments?
- [ ] Functions short, single-purpose?
- [ ] No dead code, no commented-out blocks?
- [ ] Comments (if any) explain *why*, not *what*?

## 3. Architecture
- [ ] Change respects module boundaries from `module_breakdown.md`?
- [ ] No new cross-cutting concerns introduced without discussion?
- [ ] Public API changes documented and versioned?
- [ ] Level of abstraction appropriate — no speculative generality?

## 4. Security
- [ ] Input validated at boundary?
- [ ] Parameterized queries / safe serialization?
- [ ] Secrets from config, never hard-coded?
- [ ] AuthN/AuthZ enforced on new endpoints (NFR-SEC-03)?
- [ ] No sensitive data in logs?
- [ ] Dependencies added are trustworthy and pinned?

## 5. Performance & Ops
- [ ] N+1 queries, unbounded loops, missing indexes?
- [ ] Hot paths allocate no more than necessary?
- [ ] Metrics / logs added for new critical paths (NFR-OBS)?
- [ ] Feature flag or rollout plan for risky changes?
- [ ] Rollback story clear?

## Author self-check
- [ ] Ran tests, lint, typecheck locally — all green
- [ ] Updated docs / ADR if design decision changed
- [ ] Requirement ID referenced in commit + PR
- [ ] Screenshots or logs attached as proof
