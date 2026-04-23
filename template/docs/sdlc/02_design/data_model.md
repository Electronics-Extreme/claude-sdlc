# Data Model (Domain)

The *logical* model — independent of database engine. Maps to physical schema in `database_design.md`.

## Entities

### User
- **Identity**: `email` (natural), `id` (surrogate)
- **Lifecycle states**: `pending_verification` → `active` → `suspended` → `deleted`
- **Invariants**:
  - Exactly one active email per user
  - Password hash present for password accounts only (SSO users have null)
- **Owns**: Sessions, {{...}}

### {{Entity 2}}
- **Identity**: {{...}}
- **Invariants**: {{...}}

## Relationships

```
User 1 ─── * Session
User 1 ─── * {{...}}
```

## Value Objects

| Name       | Shape                              | Validation                    |
|------------|------------------------------------|-------------------------------|
| Email      | `string`                           | RFC 5322, ≤ 254 chars         |
| Money      | `{ amount: integer, currency }`    | ISO 4217 currency             |
| TimeRange  | `{ start, end }`                   | `start < end`, both UTC       |

## State Machines

### User

```
[pending_verification] ──verify──▶ [active]
    │                                │
    │                                ├──suspend──▶ [suspended] ──reinstate──▶ [active]
    │                                │
    └──expire(30d)──▶ [deleted]      └──delete──▶ [deleted]
```

## Events (if event-driven)

| Event                | Trigger                         | Payload             |
|----------------------|---------------------------------|---------------------|
| `user.registered`    | User completes signup           | `{ userId, at }`    |
| `user.verified`      | Email verification succeeds     | `{ userId, at }`    |
