---
doc: skill/workflows/phase5-deployment.md
status: draft
required_for: ['phase-3-slice', 'phase-6-CR-implementation']
---

# Phase 5 — Deployment workflow

> Read this when Phase 4 is signed and you're cutting a release.

## Step 1 — Verify Phase 4 sign-off
Phase 5 cannot start until Phase 4 is signed AND reconciled.

## Step 2 — Cut the release
- Bump version per the project's semver convention (documented in `release_notes.md`).
- Move entries from `[Unreleased]` to the new version section in `release_notes.md`.
- Tag the commit (`git tag vX.Y.Z`).

## Step 3 — Read the deployment plan
Open `docs/sdlc/05_deployment/deployment_plan.md`. Confirm target environment, prerequisites, rollback trigger, who's on call.

## Step 4 — Walk the go-live checklist
Execute `go_live_checklist.md` item by item. Don't pre-check items; check after each completes successfully.

## Step 5 — Run smoke tests
Execute `smoke_tests.md` against the target environment. **Any smoke failure → invoke `rollback_plan.md` immediately** — do not "investigate first".

## Step 6 — Reconciliation gate (deployed-state vs spec)
Verify the deployed system matches the docs: env vars, feature flags, config values, DB schema, dependency versions. Drift here is silent and dangerous. See `reconciliation.md`.

## Step 7 — Sign off the release
User signs the new version entry in `release_notes.md`. Phase 6 opens — the project is now live.
