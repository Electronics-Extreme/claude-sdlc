---
doc: docs/INSTALL.cursor.md
status: signed
signed_by: Thanin Piromward on 2026-04-23
required_for: [phase-6-CR-implementation]
cite_as: INST
---

# Installing SDLC Strict Waterfall for Cursor

**Disambiguation first.** Cursor hosts two different AI experiences in the same
IDE:

1. **Cursor Agent** — Cursor's own built-in AI. Uses `.cursor-plugin/plugin.json`
   with a hooks section. **This doc covers Cursor Agent.**
2. **Claude Code running in Cursor** — Anthropic's extension running inside the
   Cursor IDE (Cursor is a VS Code fork). Uses `.claude/settings.json`. See
   `docs/INSTALL.claude-code.md`.

You can run both simultaneously. Each reads its own hook config.

## Layer

Cursor Agent uses **Layer 1** — a plugin with a SessionStart hook
(field-tested across live installs).

## Prerequisites

- Cursor (latest stable)
- Python 3.11+ (for the hook script)

## Install

1. Bootstrap the kit into your project (if not already present):

   ```bash
   ./bootstrap.sh ~/WorkSpace/MyProject --harness cursor
   ```

   Or with all harnesses: `./bootstrap.sh ~/WorkSpace/MyProject`.

2. Open the project in Cursor. The `.cursor-plugin/plugin.json` auto-registers
   on first Cursor Agent session.

3. The plugin's `hooks-cursor.json` invokes `hooks/run-hook.sh` →
   `hooks/session_start.py`, which detects `CURSOR_PLUGIN_ROOT` and emits the
   contract with the `additional_context` shape Cursor expects.

## Verify the contract loaded

In Cursor Agent chat:

> What are the 5 non-negotiable rules of this SDLC?

Expected: Cursor echoes the 5 rules from the injected contract. Context banner:

> ── SDLC contract v2.0.0 loaded at <ts> · harness=cursor ──

## Troubleshooting

- **Hook not firing** → check `CURSOR_PLUGIN_ROOT` is set; run
  `python3 hooks/session_start.py --detect` in an integrated terminal.
- **Layer-2 fallback** → `.cursor-plugin/rules/sdlc-contract.mdc` is also
  auto-applied by Cursor's rules engine as a belt-and-suspenders.

## Windows

Windows launcher `hooks/run-hook.cmd` is used instead of `run-hook.sh`. No
Git Bash / WSL dependency — just Python 3.11+.
