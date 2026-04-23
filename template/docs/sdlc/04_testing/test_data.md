# Test Data

## Principles

- **No real PII** in any non-prod environment.
- **Reproducible**: fixtures live in source control; seeding is scripted.
- **Minimal**: smallest dataset that exercises the scenario.

## Fixture Inventory

| Fixture ID | Description                         | Location               | Used by              |
|------------|-------------------------------------|------------------------|----------------------|
| FX-users-baseline | 10 users: mix of states      | `tests/fixtures/users.json` | TC-001..005     |
| FX-{{...}} | {{...}}                             | {{...}}                | {{...}}              |

## Seed Strategy

- **Unit**: in-test factories (no DB).
- **Integration**: per-test transaction rolled back at end.
- **E2E (CI)**: ephemeral DB, seeded at startup via `{{cmd}}`.
- **Staging**: weekly refresh from anonymized prod snapshot.

## Anonymization Rules

When sourced from prod:
- Hash emails, names, phone numbers
- Shift dates by a random offset
- Nullify free-text fields that may contain PII
- Replace all payment / financial identifiers
- Strip API keys, tokens

## Data Lifecycles

| Scope  | Lifecycle            |
|--------|----------------------|
| Unit   | Per test             |
| Integ  | Per test transaction |
| E2E    | Per CI job           |
| Staging| Weekly               |
