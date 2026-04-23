# Test Cases

Every case has a stable ID, traces to a requirement, and states expected result precisely.

## Template

### TC-### — {{Title}}

- **Requirement**: FR-### / NFR-###
- **Level**: unit / integration / E2E / performance / security
- **Pre-conditions**: {{state before test}}
- **Steps**:
  1. {{...}}
  2. {{...}}
- **Expected**: {{observable outcome}}
- **Negative variants**: {{TC-###a, TC-###b}}
- **Automated?**: yes / no — link to test file

---

## TC-001 — Register with valid email + password

- **Requirement**: FR-001
- **Level**: E2E
- **Pre-conditions**: Email `new.user@example.com` not registered.
- **Steps**:
  1. Navigate to `/signup`.
  2. Enter valid email and password meeting policy.
  3. Submit.
- **Expected**:
  - HTTP 201 from `POST /v1/users`
  - User row in `pending_verification` state
  - Verification email delivered to Mailhog within 60s (NFR-PRF: FR-002)
  - UI shows confirmation screen
- **Negative variants**:
  - TC-001a: duplicate email → 409
  - TC-001b: weak password → 422
- **Automated?**: yes — `tests/e2e/signup.spec.ts`

## TC-002 — Verification email delivered in ≤ 60s

- **Requirement**: FR-002
- **Level**: Integration
- **Steps**:
  1. Trigger signup.
  2. Poll Mailhog inbox up to 60s.
- **Expected**: email present, contains valid verification link.
- **Automated?**: yes

## TC-PRF-001 — API p95 latency ≤ 200 ms

- **Requirement**: NFR-PRF-01
- **Level**: Performance
- **Tool**: k6, 500 VUs for 10 min against staging
- **Expected**: p95 ≤ 200ms across `/v1/users/*`
- **Automated?**: yes — run in perf pipeline

## TC-SEC-010 — Password hashing

- **Requirement**: NFR-SEC-02
- **Level**: Code review + integration
- **Steps**: Inspect DB after registration; verify hash starts with `$argon2id$`.
- **Expected**: never cleartext; cost params ≥ configured minimum.
- **Automated?**: yes — unit test on hashing util

## {{... add more ...}}
