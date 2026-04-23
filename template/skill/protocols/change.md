---
doc: skill/protocols/change.md
status: draft
required_for: ['phase-3-slice', 'phase-6-CR-implementation']
---

# The change protocol

> Read this when you find a divergence between docs and code, or want to change anything documented.

If during implementation you find:
- The docs are wrong (contradict reality, contradict each other, missing a case)
- The user's request contradicts the docs
- A "better" approach occurs to you that diverges from the docs

**Do NOT silently change the code.** Instead:

1. **STOP.** Halt all code edits.
2. **Name the divergence precisely.** "FR-042 says X, but the user request implies Y." Or: "api_design.md §3.2 specifies field `prompt`, but the natural REST convention would be `instruction`."
3. **Propose the doc amendment.** State which file, which section, what the new text should be.
4. **Wait for explicit user approval.** Don't assume "ok" means "rewrite everything".
5. **Apply the doc amendment first.** Either in-place (if pre-sign-off) or as a `## Post-vX.Y.Z Amendments (YYYY-MM-DD)` section (if post-sign-off).
6. **Then update the code.**
