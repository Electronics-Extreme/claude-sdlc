# Use Cases

Each use case describes one actor-goal interaction. Keep it behavioral, not technical.

## Template

### UC-### — {{Short goal name}}

- **Actor**: {{user class}}
- **Preconditions**: {{what must be true before}}
- **Trigger**: {{event that starts this}}
- **Main flow**:
  1. {{step}}
  2. {{step}}
  3. {{step}}
- **Alternate flows**:
  - A1. {{variation}}
- **Exception flows**:
  - E1. {{error case, expected outcome}}
- **Postconditions**: {{state after success}}
- **Related requirements**: FR-###, FR-###

---

## UC-001 — {{Example: Register account}}

- **Actor**: New user
- **Preconditions**: User has a valid email, is not already registered.
- **Trigger**: User clicks "Sign up".
- **Main flow**:
  1. System shows registration form.
  2. User submits email + password.
  3. System validates input.
  4. System creates account, sends verification email.
  5. System shows "check your inbox" confirmation.
- **Alternate flows**:
  - A1. User signs up via SSO — skips steps 2–3.
- **Exception flows**:
  - E1. Email already in use → message "account exists, try logging in".
  - E2. Email service down → queue email, show non-blocking notice.
- **Postconditions**: Account created in `pending_verification` state.
- **Related requirements**: FR-001, FR-002, NFR-SEC-003
