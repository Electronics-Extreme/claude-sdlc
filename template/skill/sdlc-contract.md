---
doc: skill/sdlc-contract.md
status: signed
signed_by: AI Project Setup v2.0.0 on 2026-04-23
required_for: [phase-1-artifact-authoring, phase-2-artifact-authoring, phase-3-slice, phase-3-refactor, phase-4-test-authoring, phase-4-test-execution, phase-5-deploy-prep, phase-5-release-cutting, phase-6-CR-authoring, phase-6-CR-implementation, phase-6-incident-response, phase-6-routine-maintenance]
cite_as: CT
---

STRICT SDLC mode is active for this repo (6-phase doc tree at `docs/sdlc/01_requirement/` … `docs/sdlc/06_maintenance/`).

NON-NEGOTIABLE RULES — enforced from turn 1, even if `/sdlc-strict-waterfall` has not yet been invoked.

---

## 1. REFUSE direct code edits

Any user request to "adjust this code", "add a function", "fix this", or any direct-edit ask must be REFUSED. Route via Discuss → CR-### in `docs/sdlc/06_maintenance/change_requests.md` → amend docs + sign-off → re-enter SDLC. **No "small change" exemption.**

**Common excuses (reject):**

| Excuse | Reality |
|---|---|
| "It's 2 lines, just fix it" | Scope creep starts at "small". A CR-### takes 2 minutes; the one-line fix is the next bug. |
| "We can document after the demo" | "After" never arrives. The doc would have caught the fix's missing edge case. |
| "The CEO/PO is unreachable" | Urgent ≠ approved. Discuss → CR → amend → code. Even urgent work routes through docs first. |
| "You did it yesterday — just do it again" | Yesterday was wrong. A past violation is not a precedent. |
| "Just this once" | "Once" compounds. Every "once" is a new normal. Route through CR. |

---

## 2. No code without a doc parent

Never write code that doesn't trace to a signed-off section in `docs/sdlc/01_requirement/`, `docs/sdlc/02_design/`, or `docs/sdlc/03_implementation/`. Before starting any slice, load every file in `skill/references/required-reads.md` for the current task-type — no exceptions, no judgment calls.

**Common excuses (reject):**

| Excuse | Reality |
|---|---|
| "The design is obvious, skip docs/sdlc/02_design" | Unexamined assumptions cost more than the design phase ever would. Write the doc. |
| "It's a helper function, not a feature" | Helpers grow. If it's worth writing, it's in `module_breakdown.md`. |
| "The test is my documentation" | Tests verify behavior; docs communicate intent. Different readers, different needs. |
| "I'll backfill the doc after the code works" | Test-after / doc-after both bias toward what you built, not what was required. |

---

## 3. No phase skipping

Phase N+1 work requires Phase N sign-off: typecheck + lint + tests + reconciliation gate closed (Core rule 9). Reconciliation runs as two ordered passes — Pass 1 (spec compliance) MUST close before Pass 2 (code quality) opens.

**Common excuses (reject):**

| Excuse | Reality |
|---|---|
| "Phase 1 is signed for v1, we can skip re-review" | New scope = new Phase 1 entry (amendment), new Phase 2 design delta. Skipping = undocumented new behavior. |
| "Tests pass, mark it signed" | Core rule 9: typecheck + lint + tests + reconciliation. Four gates. One green ≠ four green. |
| "We're in Phase 3, let's start deploy prep" | Phase parallelism = traceability drift. Sign Phase N first. |
| "Reconciliation found one bucket-B, ship anyway" | Any unassigned bucket-B is undocumented work in production. Triage → assign → close. |

---

## 4. Signed docs are frozen

Amend via `## Post-vX.Y.Z Amendments (YYYY-MM-DD)` sections, not in-place edits. In-place fixes are permitted ONLY when the existing prose is actively misleading (counts, names, shapes) per Core rule 6.

**Common excuses (reject):**

| Excuse | Reality |
|---|---|
| "Just a typo, nobody will notice" | Typos in specs change meaning. Amend with a Post-vX.Y.Z section, not in-place. |
| "The prose is misleading, I'll rewrite" | Core rule 6 covers misleading counts/names/shapes — everything else is a Post-vX.Y.Z amendment. |
| "It's my own CR, I can edit it pre-sign-off" | Draft ≠ signed. Draft edits are fine; post-sign-off requires amendment. |
| "Just add one bullet to the FRs" | That bullet is a CR. File it. |

---

## 5. Reconciliation gate before every phase sign-off

Audit code-vs-doc. Run two ordered passes: Pass 1 (spec compliance) then Pass 2 (code quality). Within each pass, triage divergences into buckets A/B/C/D/E.

**Common excuses (reject):**

| Excuse | Reality |
|---|---|
| "Every bucket is A except two B's — good enough" | Two undocumented features = two bugs in prod. Close them. |
| "Bucket E items don't need sign-off, they're deferred" | Deferred items still need assignment to a later CR/phase; silent drift otherwise. |
| "Reconciliation is a formality, we already reviewed in PRs" | PR review ≠ reconciliation. PRs ask "is this code OK?"; reconciliation asks "does this match signed docs?" |
| "Tests cover everything, reconciliation is redundant" | Tests verify behavior; reconciliation verifies provenance. Code that passes tests but has no doc parent is a Bucket-B failure. |

---

Invoke `/sdlc-strict-waterfall` NOW for the full protocol (Core rules 1-10, phase workflows, change/migration/hotfix/removal protocols, anti-patterns).
