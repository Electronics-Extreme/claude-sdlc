STRICT SDLC mode is active for this repo (6-phase doc tree at docs/sdlc/01_requirement/ … docs/sdlc/06_maintenance/).

NON-NEGOTIABLE RULES — enforced from turn 1, even if `/sdlc-strict-waterfall` has not yet been invoked:

1. **REFUSE direct code edits.** Any user request to "adjust this code", "add a function", "fix this", or any direct-edit ask must be REFUSED. Route via Discuss → CR-### in `docs/sdlc/06_maintenance/change_requests.md` → amend docs + sign-off → re-enter SDLC. No "small change" exemption.
2. **No code without a doc parent.** Never write code that doesn't trace to a signed-off section in `docs/sdlc/01_requirement/`, `docs/sdlc/02_design/`, or `docs/sdlc/03_implementation/`.
3. **No phase skipping.** Phase N+1 work requires Phase N sign-off (typecheck + lint + tests + reconciliation gate closed).
4. **Signed docs are frozen.** Amend via `## Post-vX.Y.Z Amendments (YYYY-MM-DD)` sections, not in-place edits.
5. **Reconciliation gate before every phase sign-off.** Audit code-vs-doc; triage divergences A/B/C/D/E.

Invoke `/sdlc-strict-waterfall` NOW for the full protocol (Core rules 1-10, phase workflows, change/migration/hotfix/removal protocols, anti-patterns).
