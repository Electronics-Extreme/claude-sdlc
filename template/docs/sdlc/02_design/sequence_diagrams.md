# Sequence Diagrams

Use Mermaid so diagrams live in source control.

## SD-001 — User Registration (UC-001)

```mermaid
sequenceDiagram
    participant U as User
    participant W as Web App
    participant G as API Gateway
    participant S as User Service
    participant DB as Database
    participant M as Mail Service

    U->>W: Submit signup form
    W->>G: POST /v1/users
    G->>S: CreateUser(email, password)
    S->>DB: INSERT user (status=pending)
    DB-->>S: id
    S->>M: Queue verification email
    S-->>G: 201 {id, status}
    G-->>W: 201
    W-->>U: Show "check your inbox"
    M-->>U: Verification email
```

## SD-002 — Email Verification

```mermaid
sequenceDiagram
    participant U as User
    participant W as Web App
    participant G as API Gateway
    participant S as User Service
    participant DB as Database

    U->>W: Click verification link
    W->>G: POST /v1/users/verify?token=...
    G->>S: Verify(token)
    S->>DB: UPDATE user SET status='active'
    DB-->>S: ok
    S-->>G: 200
    G-->>W: redirect /login
```

## SD-003 — {{Next flow}}

```mermaid
sequenceDiagram
    {{...}}
```
