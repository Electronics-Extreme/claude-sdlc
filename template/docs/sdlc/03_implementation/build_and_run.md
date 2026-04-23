# Build & Run (Local Dev)

## Prerequisites

- {{Node 20+ / Python 3.12+ / Go 1.22+}}
- {{Docker + docker compose}}
- {{Package manager}}: {{pnpm / uv / cargo}}

## First-time setup

```bash
git clone {{repo}}
cd {{repo}}
{{install cmd}}               # install deps
cp .env.example .env          # fill local secrets
{{migrate cmd}}               # apply DB migrations
{{seed cmd}}                  # optional seed data
```

## Everyday commands

| Intent         | Command          |
|----------------|------------------|
| Dev server     | `{{CMD}}`        |
| Unit tests     | `{{CMD}}`        |
| Integration    | `{{CMD}}`        |
| Lint           | `{{CMD}}`        |
| Typecheck      | `{{CMD}}`        |
| Format         | `{{CMD}}`        |
| Build artifact | `{{CMD}}`        |
| Clean          | `{{CMD}}`        |

## Services (via docker compose)

| Service  | Port  | Purpose          |
|----------|-------|------------------|
| postgres | 5432  | Primary DB       |
| redis    | 6379  | Cache/session    |
| mailhog  | 8025  | Local SMTP UI    |

## Troubleshooting

- **Port conflict**: stop other instances, or set `PORT=` in `.env`.
- **Migration fails**: drop local DB, re-run setup.
- **Stale types**: run `{{regen cmd}}`.
