---
doc: docs/INSTALL.copilot.md
status: signed
signed_by: Thanin Piromward on 2026-04-23
required_for: [phase-6-CR-implementation]
cite_as: INST
---

# Installing SDLC Strict Waterfall for GitHub Copilot CLI

## Layer

Copilot CLI uses **Layer 1** — it reads the Claude Code plugin format
(`.claude-plugin/plugin.json`) with `COPILOT_CLI=1` env var distinguishing it
at runtime. Field-tested: a single plugin manifest serves both harnesses.

## Prerequisites

- GitHub Copilot CLI (v1.0.11+ with plugin support)
- Python 3.11+ (for the hook script)

## Install

Add the project's plugin manifest to Copilot CLI:

```bash
cd /path/to/your-project
copilot plugin install .
```

Or publish to a marketplace and install by name (future).

## How detection works

At session start, Copilot CLI invokes `hooks/run-hook.cmd` (or `.sh`), which
runs `hooks/session_start.py`. The Python script sees `COPILOT_CLI=1` in the
environment and emits the `additionalContext` JSON shape Copilot expects (SDK
standard).

## Verify

In Copilot CLI:

> What are the 5 non-negotiable rules of this SDLC?

Expected: rules echoed from the injected context.

## Fallback

If the hook doesn't fire, Copilot CLI also reads `AGENTS.md` as a Layer-2
convention. The contract is duplicated there via `scripts/sync_wrappers.py`
for redundancy.

## Troubleshooting

- **Hook not firing** → check `COPILOT_CLI=1` is set in the session
  environment: `python3 hooks/session_start.py --detect`.
- **Plugin not loading** → `copilot plugin list` should show
  `sdlc-strict-waterfall`.
