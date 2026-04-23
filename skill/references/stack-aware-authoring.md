---
doc: skill/references/stack-aware-authoring.md
status: draft
required_for: ['phase-3-slice', 'phase-6-CR-implementation']
---

# Stack-aware authoring (applies to Phase 3 docs)

> Read this when authoring `coding_standards.md`, `build_and_run.md`, or `module_breakdown.md` (during Bootstrap Gate 4 or any later amendment via the change protocol).

These three docs are **stack-specific** — they MUST encode the idiomatic conventions of the chosen language/framework, not generic placeholders.

## Authoring rules

1. **Anchor the standard in the stack's load-bearing tools.** For each stack, name the canonical:
   - **formatter** (Prettier / Black / Pint / rustfmt / gofmt)
   - **linter** (ESLint / ruff / PHPStan / clippy / golangci-lint)
   - **type checker** (tsc / mypy / PHPStan level / N/A)
   - **test framework** (Vitest / Jest / pytest / Pest / cargo test / go test)
   - **package manager** (pnpm / uv / composer / cargo / go mod)
   - **strict/safety pragmas** (`"use strict"` / `declare(strict_types=1)` / `from __future__ import annotations` / `#![deny(unsafe_code)]`)
   - **naming convention** native to the language (camelCase vs snake_case vs PascalCase per identifier kind)

2. **Cover the load-bearing topics first** — the minimum viable `coding_standards.md` covers: style enforcement, naming, error handling contract, logging shape, DI / config boundary, file layout (PSR-4 / src layout / module structure), test discipline (TDD / test-after rules from Core rule 7).

3. **Don't speculatively over-specify.** Premature specification is its own failure mode. Cover the load-bearing stuff for TO-001; expand `coding_standards.md` (via the change protocol) when a gap actually bites in a later TO-### — with a concrete case in hand, not a hypothetical.

4. **Cite stack docs in `code_review_checklist.md`** when a rule is non-obvious (e.g., "PSR-12 §6", "PEP 8 §maximum-line-length", "Effective Go §Names").

5. **Mirror the stack's project layout** in `module_breakdown.md` — PSR-4 for PHP, `src/` layout for Python, `internal/` + `cmd/` for Go, App Router conventions for Next.js, etc. Don't invent a custom tree if a community-standard one exists.

6. **Enums and constants live in code, referenced by docs.** Per Core rule 8 — `coding_standards.md` should explicitly say "no enum duplication; doc references code path." Pick a canonical module per enum (e.g., `src/lib/constants.ts`, `app/Enums/`) and write it down so future readers know where the source-of-truth lives.
