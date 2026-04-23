# Installing SDLC Strict Waterfall for OpenCode

## Layer

OpenCode uses **Layer 1-JS** — a JavaScript plugin that injects contract context
into the first user message of each session via `experimental.chat.messages.transform`.

## API stability note

OpenCode's `experimental.chat.messages.transform` hook is, per their public docs,
**experimental** and not in the stable hook list. If it's removed, fall back to
the stable `session.created` + `tui.prompt.append` combination (see plugin source
for the fallback branch). The kit's CI smoke suite exercises this hook weekly
against OpenCode's latest release to catch API drift early.

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed
- Python 3.11+ (only for the metrics subsystem; not required for hook injection)

## Install

Add the plugin to your `opencode.json` (global or project-level):

```json
{
  "plugin": ["sdlc-strict-waterfall@git+https://github.com/Electronics-Extreme/claude-sdlc.git"]
}
```

Restart OpenCode. The plugin auto-installs and registers the SDLC contract.

## Verify

After restart, start a new conversation. The first user message should be preceded
by an injected context block starting with:

> ── SDLC contract v2.0.0 loaded at <timestamp> · harness=opencode ──

Then ask:

> What are the 5 non-negotiable rules of this SDLC?

Expected: OpenCode echoes the 5 rules from the injected contract.

## Troubleshooting

- **Plugin not loading** → `opencode run --print-logs "hello" 2>&1 | grep sdlc`
- **Context not injected** → OpenCode may have updated its plugin API; check
  `.opencode/plugins/sdlc-contract-loader.js` for the `experimental.*` hook name.
- **Skills not found** → this integration uses the plugin hook, not native skill
  discovery. The contract lives in `skill/sdlc-contract.md` at the project root.

## Uninstall

Remove the line from `opencode.json` and restart OpenCode.
