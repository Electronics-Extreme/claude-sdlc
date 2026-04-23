---
doc: skill/workflows/phase3-implementation.md
status: signed
signed_by: Thanin Piromward on 2026-04-23
required_for: ["phase-3-slice", "phase-6-CR-implementation"]
---

# Phase 3 — Implementation workflow (TDD inside every slice)

> Read this when starting any TO-### in `docs/sdlc/03_implementation/task_list.md`. Inner loop is RED → GREEN → REFACTOR; outer loop is the 8 steps below.

## Step 1 — Load required reads (Core rule 1)
Consult `skill/references/required-reads.md` for task-type `phase-3-slice`. Load every file in `must_read`:
- `docs/sdlc/01_requirement/functional_requirements.md` — FR-### authorizing slice
- `docs/sdlc/01_requirement/acceptance_criteria.md` — AC-### to satisfy
- `docs/sdlc/02_design/architecture.md` — module context
- `docs/sdlc/02_design/api_design.md` — if touching endpoints
- `docs/sdlc/02_design/data_model.md` — if touching persistence
- `docs/sdlc/03_implementation/coding_standards.md` — ALWAYS
- `docs/sdlc/03_implementation/module_breakdown.md` — file-to-doc map
- `docs/sdlc/04_testing/test_cases.md` — TC-### to author/update

If any authorizing doc (FR/AC/architecture) doesn't exist → STOP. Invoke `protocols/change.md` — don't code against a missing spec. If they exist but aren't signed off → STOP. Confirm sign-off status before coding.

Cite each loaded file in your opening message using the `must_cite_in_opening` template.

## Step 2 — Locate the file map
Open `docs/sdlc/03_implementation/module_breakdown.md`. Find which file(s) implement this spec.
- If the file location isn't documented → STOP. Ask the user to add it to module_breakdown first.

## Step 3 — Read the standards
Open `docs/sdlc/03_implementation/coding_standards.md`. Note the rules that apply (naming, error handling, logging, etc.).

## Step 3a — Decide: direct execution or subagent delegation?

Per FR-MDL-003:
- If slice touches **< 2 files AND < 1 hour estimated AND < 2 FRs** → execute directly (continue to Step 4).
- If slice touches **≥ 2 files OR ≥ 1 hour OR spans multiple FRs** → DELEGATE to a subagent.

### How to delegate (controller-extracts-text pattern)

1. **Extract** from the signed docs:
   - Full TO-### text verbatim
   - AC-### items the slice must satisfy
   - Relevant doc excerpts (not paths — the actual quoted text)
   - File paths from `module_breakdown.md`
2. **Pick a tier** per `skill/SKILL.md` §"Model selection per phase":
   - mechanical slice → `cheap`
   - multi-file integration → `standard`
   - spec-ambiguity or design judgment → `capable`
3. **Dispatch** a fresh subagent with the extracted bundle. Do NOT tell the subagent to "read the docs". Provide verbatim excerpts.
4. **Subagent returns** `{status, files_changed, tests_added, self_review_notes}`. It is forbidden from reading files outside the provided paths or expanding scope beyond the bundle.
5. **Controller runs reconciliation Pass 1** (spec compliance) per `skill/reconciliation.md`. Loop back to subagent for fixes. Pass 2 (quality) runs only when Pass 1 closes.

If tier-override is needed (e.g., using `capable` for a `cheap` slice), include one-line justification in the commit message or PR body:

    tier-override: phase-3-slice cheap→capable reason=<short explanation>

## Step 4 — Write the failing test (RED)
Locate the AC-### (or TC-### if `test_cases.md` already catalogs this slice) that defines the behavior. Translate it into an executable test in the project's test framework. Run it. **Confirm it fails for the right reason** (e.g., "function not defined" or "expected X, got undefined"), not for an unrelated reason (e.g., a typo or missing import).
- One assertion or one behavior at a time. Don't pre-write a whole test suite.
- If the AC is ambiguous, STOP and invoke the change protocol (`protocols/change.md`) — don't guess in the test.
- Cite the AC-### / TC-### in the test's docstring or comment.

## Step 5 — Implement the smallest slice (GREEN)
Write the **minimum code** that makes the failing test pass.
- One file or one function at a time.
- Match the spec **verbatim**: names, types, error codes, error messages, response shapes.
- No extra parameters, no extra fields, no extra endpoints.
- Re-run the test. Confirm it passes.

## Step 6 — Refactor (still GREEN)
With the test green, clean up: extract constants, rename, de-duplicate, reshape for readability. Re-run the test after each change to confirm it still passes. Do NOT add new behavior in refactor.

## Step 7 — Verify against the full spec
Cross-check against:
- `acceptance_criteria.md` — does the slice satisfy the AC end-to-end?
- `code_review_checklist.md` — does it pass the documented gates?
- The spec doc itself — character-for-character match where applicable.
- Adjacent `docs/sdlc/04_testing/test_cases.md` entries — are there other TCs for this slice that need running?
- Typecheck + lint + full test suite green (Core rule 9).

## Step 7a — Spec self-review before sign-off

Before marking the slice done, run the 4-question self-review:

1. **Placeholders**: `{{PLACEHOLDER}}` / `TODO` / `FIXME` / `XXX` / `<TBD>` / `[to-be-filled]` anywhere in touched files? Fix inline. Confirm `python3 scripts/check_residue.py` exits 0 if any of the touched files have `status: signed`.
2. **Contradictions**: does the slice contradict signed docs?
3. **Scope**: focused (one FR or a cohesive set), or did it balloon?
4. **Ambiguity**: any AC you had to interpret creatively? If yes → amendment-protocol.

Opening-message template when marking done:

```
Spec self-review (4 questions):
  Placeholders: none (check_residue exited 0)
  Contradictions: none
  Scope: focused (1 FR, 1 AC; single-slice)
  Ambiguity: none
```

Missing block = Pass-1 Bucket C at reconciliation.

## Step 8 — Catalog the test
If `docs/sdlc/04_testing/test_cases.md` doesn't yet list the test you wrote, add it with its TC-### + AC-### back-reference. Update `test_report.md` with the pass result when the phase moves to docs/sdlc/04_testing. Update `traceability_matrix.md` row for the AC-### with TC, code, commit (`traceability-matrix.md`).

## Exception: when TDD doesn't add value
For UI rendering, config/constants, or generated code where unit-level tests add no meaningful signal, test-after (or E2E-only) is acceptable — but state explicitly in the update: "TDD skipped for <file>; reason: <UI / config / generated>; E2E covers via <spec ref>."
