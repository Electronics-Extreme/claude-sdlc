---
doc: docs/INSTALL.codex.md
status: signed
signed_by: Thanin Piromward on 2026-04-23
required_for: [phase-6-CR-implementation]
cite_as: INST
---

# Installing SDLC Strict Waterfall for Codex CLI / Codex App

This is a pointer to the canonical install guide shipped with the harness
adapter: `.codex/INSTALL.md`.

## Quick summary

1. Clone the kit: `git clone … ~/.codex/sdlc-kit`
2. Symlink skills: `ln -s ~/.codex/sdlc-kit/skill ~/.agents/skills/sdlc-strict-waterfall`
3. Restart Codex.

See `.codex/INSTALL.md` for full instructions including Windows junction setup.

## Verify

After restart, ask Codex:

> What are the 5 non-negotiable rules of this SDLC?

Expected: rules echoed from `AGENTS.md` + auto-discovered skill.
