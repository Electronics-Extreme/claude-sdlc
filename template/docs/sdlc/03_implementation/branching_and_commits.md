# Branching & Commits

## Branches

- `main` — always green, always deployable.
- `feat/<slug>` — new functionality
- `fix/<slug>` — bug fix
- `chore/<slug>` — tooling, refactors with no behavior change
- `hotfix/<slug>` — emergency fix branched from `main`, merged back + tagged

No long-lived branches. Rebase frequently; no merge commits inside feature branches.

## Commits

Conventional Commits:

```
<type>(<scope>): <subject>

<body — optional, explains WHY>

<footer — optional: BREAKING CHANGE, Refs: FR-###>
```

Types: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`, `perf`, `build`, `ci`, `revert`.

Rules:
- Subject ≤ 72 chars, imperative mood ("add", not "added").
- One logical change per commit. If you say "and" in the subject, split.
- Reference the requirement ID in body/footer: `Refs: FR-001`.
- No WIP commits on `main`. Squash before merge if needed.

## Pull Requests

- Title: conventional-commit style.
- Description template:
  ```
  ## What
  ## Why (link FR/TO/UC)
  ## How
  ## Screenshots / proof
  ## Checklist (see code_review_checklist.md)
  ```
- Size cap: ~400 lines diff excluding generated files. Larger PRs need pre-review design note.
- At least 1 approval from CODEOWNERS. Security-tagged areas: 2 approvals.

## Tags & Versions

- SemVer `MAJOR.MINOR.PATCH`
- Tag format: `v1.2.3`
- Release notes generated from commit log — see `docs/sdlc/05_deployment/release_notes.md`.
