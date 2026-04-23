---
doc: docs/INSTALL.opencode.md
status: signed
signed_by: Thanin Piromward on 2026-04-23
required_for: [phase-6-CR-implementation]
cite_as: INST
---

# Installing SDLC Strict Waterfall for OpenCode

This is a pointer to the canonical install guide shipped with the harness
adapter: `.opencode/INSTALL.md`.

## Layer

**Layer 1-JS** — a JavaScript plugin module (not a bash/Python hook).
`.opencode/plugins/sdlc-contract-loader.js` uses
`experimental.chat.messages.transform` to inject the contract into the first
user message of each session.

## API stability

⚠️ `experimental.chat.messages.transform` is **not** in OpenCode's documented
stable hook list as of 2026-04-23. Monitor for deprecation. Fallback plan
(documented in the plugin source): switch to stable `session.created` +
`tui.prompt.append` combination.

## Install summary

Add to `opencode.json`:

```json
{
  "plugin": ["sdlc-strict-waterfall@git+https://github.com/Electronics-Extreme/claude-sdlc.git"]
}
```

Restart OpenCode.

Full instructions including troubleshooting: `.opencode/INSTALL.md`.

## Verify

In OpenCode:

> What are the 5 non-negotiable rules of this SDLC?

Expected: rules echoed; first context line reads:

> ── SDLC contract v2.0.0 loaded at <ts> · harness=opencode ──
