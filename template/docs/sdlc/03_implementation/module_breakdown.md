# Module Breakdown

Maps design components → code modules → requirements. Acts as the traceability matrix.

## Module Map

| Module path              | Responsibility                              | Design ref             | Requirements |
|--------------------------|---------------------------------------------|------------------------|--------------|
| `src/auth/`              | Auth tokens, session lifecycle              | arch §5, SD-001        | FR-001..004, NFR-SEC-* |
| `src/users/`             | User CRUD, verification flow                | data_model User        | FR-001..005  |
| `src/api/`               | HTTP layer, routing, error mapping          | api_design.md          | all FR       |
| `src/db/`                | Query layer, migrations                     | database_design.md     | all          |
| `src/mail/`              | Outbound email, templates                   | SD-001 step 5          | FR-002       |
| `src/observability/`     | Logs, metrics, tracing                      | arch §5                | NFR-OBS-*    |
| `src/config/`            | Env + secrets loader                        | arch §5                | NFR-SEC-*    |
| `web/pages/`             | UI screens                                  | ui_design.md           | UC-*         |

## Module Contract (template)

For each module, define:

```
Name:           {{e.g. users}}
Purpose:        {{one sentence}}
Public API:     {{exported fns/types}}
Depends on:     {{other modules}}
Depended on by: {{...}}
Side effects:   {{DB, network, FS}}
Failure modes:  {{timeouts, conflicts}}
Owner:          {{person or team}}
```

## Traceability Matrix

| Requirement | Design element       | Module(s)         | Test case(s) |
|-------------|----------------------|-------------------|--------------|
| FR-001      | SD-001, users entity | src/users, src/api | TC-001      |
| FR-002      | SD-001 step 5        | src/mail          | TC-002       |
| NFR-SEC-02  | coding_standards     | src/auth          | TC-SEC-010   |
