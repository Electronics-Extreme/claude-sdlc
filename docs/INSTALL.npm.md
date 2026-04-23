---
doc: docs/INSTALL.npm.md
status: signed
signed_by: AI Project Setup v2.0.0 on 2026-04-23
required_for: [phase-6-CR-implementation]
cite_as: INST-NPM
---

# Install via npm / npx

Node.js-based installer for the SDLC Strict Waterfall kit. Mirrors the
shell-bootstrap behavior: copies `template/` contents, applies per-harness
wrapper files, and regenerates SHA256 integrity pins.

## Prerequisites

- **Node.js ≥18** — for the installer itself (`node --version`)
- **Python 3.11+** — for the runtime: hooks, scripts, and the metrics
  subsystem all require Python (`python3 --version`)

## Option 1 — npx (no install)

```bash
npx claude-sdlc init ~/Projects/MyProject --harness claude
```

npx downloads the package into its cache, runs `init`, and moves on — no
permanent global install.

## Option 2 — npm global

```bash
npm install -g claude-sdlc
claude-sdlc init ~/Projects/MyProject --harness claude
```

Then the `claude-sdlc` command is on your `$PATH` for future projects.

## Option 3 — local link (development)

```bash
git clone https://github.com/Electronics-Extreme/claude-sdlc
cd claude-sdlc
npm install
npm link
claude-sdlc init ~/Projects/MyProject --harness claude
```

Use this when you want to modify the kit itself and test installer changes.

## Command reference

```
claude-sdlc init <dir> [options]

Options:
  -f, --force              Overlay a non-empty target directory without
                           prompting.
  --harness <name>         Harness wrapper(s) to install. One of:
                           claude, cursor, codex, gemini, copilot,
                           opencode, all (default: all).
  -h, --help               Show help.
  -V, --version            Print installer version.
```

Examples:

```bash
# Full install of everything into a new directory
claude-sdlc init ~/Projects/MyApp

# Claude Code only, overwrite an existing non-empty dir
claude-sdlc init ~/Projects/MyApp --harness claude --force

# Cursor Agent only
claude-sdlc init . --harness cursor
```

## What the installer does

1. Copies every directory from `template/` into the target:
   `docs/sdlc/01_requirement/…docs/sdlc/06_maintenance/`, `skill/`, `hooks/`, `scripts/`,
   `config/`, `schemas/`, `tools/`, `.github/`.
2. Applies harness-specific wrapper files based on `--harness`:
   `.claude/`, `.cursor-plugin/`, `AGENTS.md`, `GEMINI.md`,
   `gemini-extension.json`, `.opencode/`, `.claude-plugin/`.
3. For `--harness claude` (or `all`), replicates `skill/` into
   `.claude/skills/sdlc-strict-waterfall/` so `/sdlc-strict-waterfall`
   is invocable.
4. Promotes `CLAUDE.template.md` → `CLAUDE.md` (only if `CLAUDE.md` doesn't
   already exist; otherwise both are kept and a note is printed).
5. Regenerates SHA256 companions for `skill/sdlc-contract.md` and
   `hooks/session_start.py` so the integrity check matches the freshly-
   copied content.
6. Prints warnings for any missing critical files, then the next-steps
   ceremony.

## After install

```
1. cd <target-dir>
2. Edit CLAUDE.md — fill {{PLACEHOLDER}} values
3. Open docs/sdlc/01_requirement/srs.md and start the spec
4. Start Claude Code (or your chosen harness) in the target directory
5. First message to the agent:
     /sdlc-strict-waterfall
     Start.
```

The SessionStart hook auto-loads the non-negotiable SDLC contract. Brand-new
project → Bootstrap mode (Gate 1 Q&A). Existing signed docs → Strict mode.

## Verification

After install, the hook's integrity check should pass:

```bash
cd <target-dir>
python3 hooks/session_start.py --check-integrity
# Expected: ok contract_sha=<hex-prefix>
```

If you see `INTEGRITY FAILURE`, re-pin:
```bash
python3 scripts/update_contract_sha.py --write
```

## Comparison with other install paths

| Path                       | Prereqs            | When to use                                   |
|----------------------------|--------------------|-----------------------------------------------|
| `npx claude-sdlc init`     | Node ≥18 + Python  | Quickest; no global install                   |
| `npm install -g`           | Node ≥18 + Python  | Run installer many times across projects      |
| `bootstrap.sh`             | Bash + Python      | Unix/macOS terminal users                     |
| `bootstrap.bat`/`.ps1`     | Python only        | Windows without WSL                           |
| `git clone` + bootstrap    | Git + Python       | Want to inspect/fork source before installing |
| LLM-assisted               | Agent + Python     | See `docs/INSTALL.via-claude.md`              |

## Troubleshooting

- **`permission denied` during `npm install -g`** — macOS/Linux system Node
  requires sudo. Prefer `npx` or configure an nvm/volta Node.
- **`error: Template directory not found`** — the published tarball is
  corrupted, or your npm cache is stale. Clear: `npm cache clean --force`.
- **Hook fires but contract loads nothing after install** — verify your
  harness was detected: `python3 hooks/session_start.py --detect`.
- **`python3: command not found`** — install Python 3.11+ (see
  `docs/INSTALL.windows.md` on Windows; `brew install python@3.11` on macOS).

## Security

- Published under the `claude-sdlc` npm name; `npm view claude-sdlc` should
  show Electronics-Extreme as publisher.
- Only runtime dependency is `commander` (arg parsing). Audit:
  `npm view claude-sdlc dependencies`.
- No network access during `init` after the package tarball is fetched —
  the installer copies files from its own bundled `template/` directory.
