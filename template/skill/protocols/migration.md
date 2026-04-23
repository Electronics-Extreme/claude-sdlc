---
doc: skill/protocols/migration.md
status: draft
required_for: ['phase-3-slice', 'phase-6-CR-implementation']
---

# The migration protocol (data + schema changes)

> Read this when you're about to modify a DB schema, change persisted data shape, or change shared config / feature flags. Migrations follow the change protocol PLUS these extra steps.

## What counts as a migration
- Modifies a database schema (Prisma migrate, raw DDL, ORM auto-migration).
- Modifies persisted data shape (backfills, type coercions, JSON-shape changes).
- Modifies stored config / feature flags in a shared environment.

## The migration workflow
1. **Document-first.** Update `docs/sdlc/02_design/data_model.md` AND `docs/sdlc/02_design/database_design.md` first via `protocols/change.md`. Migration cannot start until both reflect the new shape.
2. **Forward + reverse.** Every migration must have a documented rollback. If irreversible (data deletion, type narrowing, dropped column), record the irreversibility in `docs/sdlc/02_design/trade_offs.md` and require explicit user acknowledgement before applying.
3. **Dry-run.** Run against a copy of production data (or a representative dev DB) and capture the diff (`prisma migrate diff`, `pg_dump` before/after, etc.).
4. **Backup gate.** For shared environments: confirm a backup exists AND is restorable BEFORE applying. "I'll take a backup if it goes wrong" is too late.
5. **Failing test first.** Test that the post-migration state matches the new schema (typecheck against new Prisma client, integration test against the new shape).
6. **Apply.** Run the migration. Verify with `\d` / `prisma db pull` / equivalent introspection.
7. **Verify behavior.** Full test suite + smoke tests against the migrated environment.
8. **Update `runbook.md`** with the migration entry: command, observed timing, rollback command, gotchas.

## Anti-patterns
- "I'll migrate first, then update the docs" — NO. Data model is the doc; migrate against the new spec.
- `prisma migrate reset` on shared environments — DESTRUCTIVE. Confirm env is local-only first.
- Skipping the dry-run because "it's a small column rename" — NO. Aliasing during a rename can break running clients.
- "Manual" rollback — NO. Document the exact rollback commands in the migration entry.
