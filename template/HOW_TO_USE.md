# How to Use This SDLC Scaffold

This project was bootstrapped from a frozen Waterfall SDLC scaffold + Claude Code wiring (SessionStart hook + `/sdlc-strict-waterfall` skill). This file explains what's here and how to drive it.

## What you got

```
.
├── docs/sdlc/01_requirement/ … docs/sdlc/06_maintenance/   # phase doc tree — each with README + {{PLACEHOLDER}} stub artifacts
├── .claude/
│   ├── settings.json                   # SessionStart hook
│   ├── sdlc-contract.md                # 5 non-negotiable rules (~300 tok, auto-loaded)
│   └── skills/sdlc-strict-waterfall/   # full protocol skill (Core rules 1-10, workflows, protocols)
├── CLAUDE.md                           # project-specific facts (fill {{PLACEHOLDERS}})
├── README.md
└── HOW_TO_USE.md                       # this file
```

Phase artifact files (`srs.md`, `architecture.md`, `coding_standards.md`, etc.) ship as filesystem-visible scaffolds with `{{PLACEHOLDER}}` markers — **agent-agnostic** so any LLM, IDE, or human can browse `ls 0X_*/` and see the expected doc shape (C4 levels, FR/NFR/UC/AC tables, etc.) without loading the Claude skill. Bootstrap mode of `/sdlc-strict-waterfall` reads each scaffold, customizes per your gate answers, and writes back to the same path.

## First Steps

1. `cd` into this directory. Run `claude`. The SessionStart hook injects `sdlc-contract.md` as an `IMPORTANT` system reminder — Claude sees the 5 non-negotiable rules from turn 1.
2. Invoke `/sdlc-strict-waterfall` — it auto-detects whether to enter Bootstrap mode (co-author docs gate-by-gate) or Strict mode (docs already signed).
3. Edit `CLAUDE.md` — replace every `{{PLACEHOLDER}}` with project-specific values (name, stack, paths, commands, guardrails, quirks).
4. Open `docs/sdlc/01_requirement/srs.md` — start the spec. Bootstrap mode of the skill will walk you through Gates 1-4.
5. Each phase's `README.md` has its **exit criteria** — don't advance until they're met (and reconciliation gate is closed).

## Placeholder Convention

Every fill-in point uses `{{DOUBLE_BRACES}}`. Grep for them to find unfinished sections:

```bash
grep -rn "{{" .
```

## Verifying the SessionStart hook

In this directory:

```bash
CLAUDE_PROJECT_DIR="$(pwd)" jq -Rs '{priority:"IMPORTANT",message:.}' "$CLAUDE_PROJECT_DIR/.claude/sdlc-contract.md" | head -3
```

Should print a JSON envelope with the contract message. Requires `jq` (preinstalled on macOS via Xcode CLI tools, or `brew install jq`).

## Improvements

Found a missing checklist item, an NFR category that always gets skipped, or refined hook content? Update the files in this project, then push the improvement back to your shared SDLC bootstrap source so the next project benefits too.

## What's Included

- `README.md` — top-level phase map + Claude Code setup notes
- `CLAUDE.md` (renamed from `CLAUDE.template.md` at bootstrap) — project-specific context for Claude (slim; rules live in `.claude/`)
- `.claude/settings.json` + `.claude/sdlc-contract.md` — SessionStart hook injecting the 5-rule contract
- `.claude/skills/sdlc-strict-waterfall/` — full SDLC protocol skill (SKILL.md + workflows/ + protocols/ + references/)
- `docs/sdlc/01_requirement/` → `docs/sdlc/06_maintenance/` — one folder per Waterfall phase with a `README.md` (goal + inputs + doc list + exit criteria + anti-patterns) plus filesystem-visible `{{PLACEHOLDER}}` scaffolds for every artifact in that phase
