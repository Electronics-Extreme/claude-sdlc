# API Design

## Style
- **Protocol**: {{REST over HTTPS | gRPC | GraphQL}}
- **Format**: JSON, UTF-8
- **Versioning**: URL prefix `/v1/...` — breaking changes = new version
- **Auth**: {{Bearer JWT via `Authorization` header}}
- **Errors**: [RFC 7807 problem+json](https://www.rfc-editor.org/rfc/rfc7807)

## Conventions

- Resources: plural nouns (`/users`, `/orders/{id}`)
- Pagination: cursor-based — `?cursor=...&limit=...`
- Timestamps: ISO 8601 UTC (`2026-04-17T12:34:56Z`)
- IDs: opaque strings, never leak DB internals
- Idempotency: mutating POST accepts `Idempotency-Key` header

## Error Envelope

```json
{
  "type": "https://example.com/errors/validation",
  "title": "Invalid request",
  "status": 400,
  "detail": "email must be a valid address",
  "instance": "/v1/users",
  "errors": [{ "field": "email", "code": "invalid_format" }]
}
```

## Endpoints

### POST /v1/users — Register

- **Auth**: none
- **Body**:
  ```json
  { "email": "a@b.com", "password": "..." }
  ```
- **Responses**:
  - `201` — `{ "id": "...", "status": "pending_verification" }`
  - `409` — email already registered
  - `422` — validation errors
- **Maps to**: FR-001, UC-001

### GET /v1/users/me

- **Auth**: required
- **Response**: `{ "id", "email", "status", "createdAt" }`
- **Maps to**: FR-###

### {{... next endpoint ...}}

## Rate Limits

| Tier             | Limit         | Window |
|------------------|---------------|--------|
| Unauthenticated  | 60 req        | 1 min  |
| Authenticated    | 600 req       | 1 min  |
| Sensitive (auth) | 10 req        | 1 min  |

## Webhooks / Events (if any)

| Event              | Payload schema           | Delivery guarantee |
|--------------------|--------------------------|--------------------|
| `user.registered`  | `{ "userId", "at" }`     | at-least-once      |
