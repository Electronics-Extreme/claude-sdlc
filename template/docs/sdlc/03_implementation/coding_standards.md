# Coding Standards

Consistency > personal preference. Tools enforce; humans don't hand-format.

## Tooling

| Language      | Formatter    | Linter        | Typechecker      |
|---------------|--------------|---------------|------------------|
| TypeScript    | Prettier     | ESLint        | tsc --strict     |
| Python        | Ruff format  | Ruff          | mypy --strict    |
| Go            | gofmt        | golangci-lint | (built-in)       |
| Rust          | rustfmt      | clippy        | (built-in)       |

**All formatters run on pre-commit. CI fails on any lint/type error.**

## Naming

- Files: `kebab-case.ts`, `snake_case.py` per language convention
- Classes / types: `PascalCase`
- Functions / variables: `camelCase` (TS/Go), `snake_case` (Py/Rust)
- Constants: `UPPER_SNAKE_CASE`
- Booleans: prefix `is`, `has`, `can`, `should`
- No single-letter names except loop counters and mathematical notation

## Structure

- Max file length: soft ~400 lines. If you pass, ask whether it should be split.
- Max function length: soft ~40 lines.
- Max cyclomatic complexity: 10.
- One exported symbol per file unless tightly cohesive.

## Comments

- Default: **no comments**.
- Write one only when the *why* is non-obvious (workaround, hidden invariant, counterintuitive perf).
- Never restate *what* the code does.
- Never reference tickets or PRs inline — that's the commit/PR's job.

## Errors

- Fail loud at boundaries; trust internal calls.
- Never swallow exceptions silently.
- Error types are enumerable and typed.
- User-facing errors separate from internal (don't leak stack traces).

## Logs

- Structured (JSON). Fields: `ts`, `level`, `service`, `trace_id`, `message`, `...context`.
- No PII in logs.
- Log levels: `debug` (dev only), `info` (lifecycle events), `warn` (recoverable), `error` (action required).

## Tests

- Co-located with source (`foo.ts` + `foo.test.ts`) or mirrored tree (`src/foo.py` + `tests/test_foo.py`).
- One behavior per test. No shared mutable fixtures.
- Assertion count ≥ 1; no "if-else" assertions.
- No sleeps — use deterministic waits.

## Security (inline)

- Validate all input at the boundary.
- Parameterized queries only. Never string-concat SQL.
- Secrets from env/secret manager. Never in code or logs.
- Deps pinned; update via dependabot/renovate.

## Accessibility (frontend)

- Semantic HTML first; ARIA only when semantics insufficient.
- Every interactive element keyboard reachable.
- Color contrast ≥ WCAG AA.
