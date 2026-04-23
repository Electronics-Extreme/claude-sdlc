---
doc: docs/INSTALL.claude-code.md
status: signed
signed_by: Thanin Piromward on 2026-04-23
required_for: [phase-6-CR-implementation]
cite_as: INST
---

# Installing SDLC Strict Waterfall for Claude Code

## Surfaces covered

One `.claude/settings.json` reaches **5 Claude Code surfaces** — CLI, VS Code
extension, Cursor extension (Anthropic's), JetBrains plugin, and
claude.ai/code (web).

## Prerequisites

- Claude Code installed (any surface)
- Python 3.11+ (for the hook script)

## Install

### Option A: bootstrap a new project from the kit

```bash
./bootstrap.sh ~/WorkSpace/MyNewProject --harness claude
```

Or with all harnesses:

```bash
./bootstrap.sh ~/WorkSpace/MyNewProject
```

### Option B: drop the kit into an existing project

```bash
cp -r /path/to/claude-sdlc/.claude /path/to/your-project/
cp -r /path/to/claude-sdlc/skill /path/to/your-project/
cp /path/to/claude-sdlc/CLAUDE.template.md /path/to/your-project/CLAUDE.md
```

Edit `CLAUDE.md` to fill in `{{PLACEHOLDER}}` values.

## Verify the contract loaded

Start Claude Code in the project directory (CLI: `claude`, or open in VS Code).
Ask:

> What are the 5 non-negotiable rules of this SDLC?

Expected: Claude echoes the 5 rules and cites `skill/sdlc-contract.md`. The first
context block should contain the banner line:

> ── SDLC contract v2.0.0 loaded at <ts> · harness=claude-code ──

If you don't see the banner, the hook didn't fire. Check:
1. `.claude/settings.json` references `hooks/session_start.py` (kit v2.0+) OR
   `skill/sdlc-contract.md` (fallback).
2. `python3 --version` returns ≥ 3.11.
3. `python3 hooks/session_start.py --detect` outputs `detected=claude-code`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Hook silently not firing | `python3 hooks/session_start.py --check-integrity` — fix SHA mismatches |
| "Python not found" | Install Python 3.11+ per `docs/INSTALL.windows.md` or `brew install python@3.11` |
| Contract outdated on amendments | Run `python3 scripts/update_contract_sha.py --write` after editing `skill/sdlc-contract.md` |

## Related

- Multi-surface detail: see `skill/SKILL.md` §"Document map"
- Contract integrity (SHA pinning): `skill/sdlc-contract.md.sha256`
- Other harnesses: `docs/INSTALL.cursor.md`, `.codex/INSTALL.md`, `.opencode/INSTALL.md`, `docs/INSTALL.copilot.md`, `docs/INSTALL.gemini.md`
