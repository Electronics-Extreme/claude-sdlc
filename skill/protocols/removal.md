---
doc: skill/protocols/removal.md
status: draft
required_for: ['phase-3-slice', 'phase-6-CR-implementation']
---

# The removal protocol

> Mirror of `protocols/change.md` — for deletion. Read this before deleting any code, file, endpoint, field, or behavior. The skill must not let an agent quietly delete things just because they "look unused."

## When deletion is in scope
- The user explicitly asked.
- A reconciliation pass identified the artifact as candidate for removal (typically a Bucket E previously, now retired).
- An EoL date in `docs/sdlc/06_maintenance/eol_policy.md` has been reached.

## The removal workflow
1. **STOP.** Do not delete on first impulse. "Looks unused" is not evidence.
2. **Trace the artifact.** Find every doc that mentions it (FR-###, UC-###, `api_design.md` endpoints, `data_model.md` fields, `module_breakdown.md` entries, `traceability_matrix.md` rows).
3. **Trace callers.** Find every code reference. If any caller traces to a doc, that caller's doc must be amended first.
4. **Propose the doc amendment(s).** Each doc that mentions the artifact gets a `## Post-vX.Y.Z Amendments (YYYY-MM-DD)` entry marking it removed (or moved to a "Removed in vX.Y.Z" section).
5. **Wait for explicit user approval.**
6. **Deprecation period for external contracts.** If the artifact is in `api_design.md` or any externally-visible surface, mark deprecated for at least one minor version before removal. Communicate the deprecation in `release_notes.md` with a `### Deprecated` entry.
7. **Remove the code.** Failing test first if it's behavior; otherwise delete + run the full suite to confirm nothing breaks.
8. **Update `release_notes.md`** with a `### Removed` entry citing the amendment.
9. **Update `traceability_matrix.md`** — remove the row(s).

## Anti-patterns
- "This file looks unused" — NO. Trace before you delete.
- Deleting comments you don't understand — NO. Understand the why first.
- Removing an endpoint without a deprecation cycle — NO. External contracts get warning periods.
- Quietly removing a field "because no one uses it" — NO. Doc-first amendment, then code.
