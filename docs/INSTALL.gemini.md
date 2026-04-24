---
doc: docs/INSTALL.gemini.md
status: signed
signed_by: Thanin Piromward on 2026-04-23
required_for: [phase-6-CR-implementation]
cite_as: INST
---

# Installing SDLC Strict Waterfall for Gemini CLI

## Layer

Gemini CLI uses **Layer 2** — no session-start hook API exists. The kit
integrates via Gemini's extension mechanism + `contextFileName` pointer to
`GEMINI.md`.

## Prerequisites

- [Gemini CLI](https://github.com/google-gemini/gemini-cli) installed

## Install

### Option 1: Gemini extension (recommended)

```bash
gemini extensions install https://github.com/Electronics-Extreme/claude-sdlc
```

### Option 2: Manual bootstrap

```bash
cd /path/to/your-project
gemini extensions install .
```

The project's `gemini-extension.json` declares:

```json
{
  "name": "sdlc-strict-waterfall",
  "version": "2.0.0",
  "contextFileName": "GEMINI.md"
}
```

Gemini reads `GEMINI.md` on extension activation.

## Verify the contract loaded

Start a Gemini CLI session in the project. Ask:

> What are the 5 non-negotiable rules of this SDLC?

Expected: Gemini echoes the 5 rules from `GEMINI.md`.

## Keep GEMINI.md fresh

`GEMINI.md` is **auto-generated** from `skill/sdlc-contract.md` by
`scripts/sync_wrappers.py`. Re-run after any contract amendment:

```bash
python3 scripts/sync_wrappers.py --write
```

CI enforces sync via `scripts/sync_wrappers.py --check`.

## Troubleshooting

- **Extension not activating** → verify `gemini extensions list` shows
  `sdlc-strict-waterfall`.
- **Context not loaded** → confirm `GEMINI.md` is present in the project root
  and referenced in `gemini-extension.json`.
- **Contract outdated** → `python3 scripts/sync_wrappers.py --write` +
  reactivate extension.
