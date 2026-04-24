# Multi-Platform Install Support — Design Spec

**Date:** 2026-04-24
**Topic:** Add `.claude-plugin`, `npx skills`, `gemini extensions`, and Codex plugin discovery support
**Repo:** https://github.com/Electronics-Extreme/claude-sdlc
**Plugin name:** `Electronics-Extreme/claude-sdlc`

---

## 1. Goal

Enable one-command installation of the SDLC Strict Waterfall kit across 8+ AI agent platforms. After install, the loaded skill/rule file detects a missing SDLC scaffold in the current project and offers to bootstrap it.

## 2. Non-Goal

- Replace `npx claude-sdlc init` as the primary bootstrap mechanism
- Support agent platforms not listed below
- Auto-scaffold without user confirmation

## 3. Architecture

### 3.1 Principle

`npx skills add` and `claude plugin install` only **copy files** — they do not execute scripts. "Bootstrap on install" is implemented as a **bootstrap guard** inside every skill/rule/context file. When the agent loads the file, the guard instructs the agent to check for a scaffold and offer to create one.

### 3.2 Two file layers

| Layer | Location | Purpose |
|---|---|---|
| **Repo root** | `.claude-plugin/`, `.cursor/`, `.windsurf/`, `.clinerules/`, `.github/`, `.codex/`, `gemini-extension.json`, `skills/` | Consumed by install commands. Copied into agent config or global plugin store. |
| **Template** | `template/` | Consumed by `claude-sdlc init` or the bootstrap guard. Copied into the adopter's project. |

Root-level files must be **self-contained** or reference the repo via `git clone` / `npx claude-sdlc init`. They do not assume access to `template/`.

### 3.3 Exception: Claude Code plugin

The `.claude-plugin` install bundles the full repo into Claude's global plugin store. The SessionStart hook runs a script that **does** have access to `${CLAUDE_PLUGIN_ROOT}/template/`, so it can copy directly without external fetch.

## 4. File Structure

### 4.1 New files at repo root

```
.claude-plugin/
  plugin.json              # manifest: name=Electronics-Extreme/claude-sdlc
  hooks/
    hooks.json             # SessionStart → bootstrap-check script

gemini-extension.json      # Gemini CLI extension manifest

.codex/
  hooks.json               # Codex auto-activation on session start

.cursor/
  rules/
    sdlc-contract.mdc      # Cursor always-on rule + bootstrap guard

.windsurf/
  rules/
    sdlc-contract.md       # Windsurf always-on rule + bootstrap guard

.clinerules/
  sdlc-contract.md         # Cline always-on rule + bootstrap guard

.github/
  copilot-instructions.md  # Copilot custom instructions + bootstrap guard

skills/
  sdlc-strict-waterfall/
    SKILL.md               # Invocable skill /sdlc-strict-waterfall + bootstrap guard
```

### 4.2 Existing files to update

| File | Change |
|---|---|
| `README.md` | Replace Quick start with agent-native install table |
| `docs/INSTALL.claude-code.md` | Add plugin install as Option 1, manual bootstrap as Option 2 |
| `docs/INSTALL.cursor.md` | Add `npx skills add` as Option 1 |
| `docs/INSTALL.gemini.md` | Add `gemini extensions install` as Option 1 |
| `docs/INSTALL.codex.md` | Add `/plugins` discovery as Option 1 |
| `docs/INSTALL.copilot.md` | Add `npx skills add` as Option 1 |
| `AGENTS.md` | Add bootstrap guard if used as generic agent context |
| `GEMINI.md` | Add bootstrap guard |

## 5. Per-Agent Install Mapping

| Agent | Command | Files consumed | Destination | Activation |
|---|---|---|---|---|
| **Claude Code** | `claude plugin marketplace add Electronics-Extreme/claude-sdlc && claude plugin install claude-sdlc@claude-sdlc` | `.claude-plugin/plugin.json` + `hooks/` | Claude global plugin store | SessionStart hook fires on every Claude session |
| **Gemini CLI** | `gemini extensions install https://github.com/Electronics-Extreme/claude-sdlc` | `gemini-extension.json` + `GEMINI.md` | Gemini ext dir | `GEMINI.md` loaded as context on every `gemini` run |
| **Codex** | Clone repo → `/plugins` → Search "SDLC" → Install | `.codex/hooks.json` + `AGENTS.md` + `skill/` | Codex plugin dir | Hook auto-activates on Codex session start |
| **Cursor** | `npx skills add Electronics-Extreme/claude-sdlc -a cursor` | `.cursor/rules/sdlc-contract.mdc` | `.cursor/rules/` in target repo | Rule always-on in Cursor Agent chat |
| **Windsurf** | `npx skills add Electronics-Extreme/claude-sdlc -a windsurf` | `.windsurf/rules/sdlc-contract.md` | `.windsurf/rules/` in target repo | Rule always-on in Windsurf Cascade |
| **Cline** | `npx skills add Electronics-Extreme/claude-sdlc -a cline` | `.clinerules/sdlc-contract.md` | `.clinerules/` in target repo | Rule loaded into Cline system prompt |
| **Copilot** | `npx skills add Electronics-Extreme/claude-sdlc -a github-copilot` | `.github/copilot-instructions.md` + `AGENTS.md` | `.github/` in target repo | Instructions loaded into Copilot chat |
| **Any other** | `npx skills add Electronics-Extreme/claude-sdlc` | `skills/sdlc-strict-waterfall/SKILL.md` | Agent-specific skills dir | `/sdlc-strict-waterfall` invocable |

## 6. Skill / Rule File Content

### 6.1 Shared structure

All rule files and context files use the same two-part structure:

**Part A — SDLC Contract (always-on context)**
- 5 non-negotiable rules
- Reconciliation gate description
- Per-phase workflow summary
- Link to full protocol: `skill/SKILL.md`

**Part B — Bootstrap Guard**

```markdown
## Bootstrap Guard

If current project lacks `docs/sdlc/01_requirement/`:

1. Inform user: "SDLC scaffold not detected in this project."
2. Offer: "Shall I bootstrap the SDLC structure here?"
3. If yes, run ONE of:
   - Node available → `npx claude-sdlc init . --harness <detected>`
   - No Node → `git clone https://github.com/Electronics-Extreme/claude-sdlc /tmp/sdlc-kit && /tmp/sdlc-kit/bootstrap.sh . --harness <detected>`
4. After bootstrap, instruct user to restart agent session for hooks to register.
```

### 6.2 Agent-specific frontmatter

| Agent | Frontmatter |
|---|---|
| Cursor (`.mdc`) | `---\ndescription: "SDLC Strict Waterfall — doc-first methodology with 5 non-negotiable rules"\nalwaysApply: true\n---` |
| Windsurf (`.md`) | `---\ntrigger: always_on\n---` |
| Cline (`.md`) | None — plain markdown |
| Copilot (`.md`) | None — plain markdown |

### 6.3 Claude Code plugin manifest

`.claude-plugin/plugin.json`:

```json
{
  "name": "Electronics-Extreme/claude-sdlc",
  "description": "Strict waterfall SDLC methodology — doc-first, TDD inside slices, two-pass reconciliation gate, CR-driven changes.",
  "version": "2.0.0",
  "author": {
    "name": "AI Project Setup",
    "url": "https://github.com/Electronics-Extreme"
  },
  "homepage": "https://github.com/Electronics-Extreme/claude-sdlc",
  "repository": "https://github.com/Electronics-Extreme/claude-sdlc",
  "license": "MIT",
  "keywords": ["sdlc", "waterfall", "tdd", "doc-first", "reconciliation"],
  "hooks": "./hooks/hooks.json"
}
```

`.claude-plugin/hooks/hooks.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact|resume",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/scripts/bootstrap_guard.py\"",
            "async": false
          }
        ]
      }
    ]
  }
}
```

The `bootstrap_guard.py` script:
- Checks if `$CLAUDE_PROJECT_DIR/docs/sdlc` exists
- If missing, prints a prompt asking user to bootstrap
- If user confirms, copies from `${CLAUDE_PLUGIN_ROOT}/template/` to `$CLAUDE_PROJECT_DIR/`
- Regenerates SHA256 pins after copy

### 6.4 Gemini extension manifest

`gemini-extension.json`:

```json
{
  "name": "Electronics-Extreme/claude-sdlc",
  "description": "Strict waterfall SDLC methodology — doc-first, TDD inside slices, two-pass reconciliation gate, CR-driven changes.",
  "version": "2.0.0",
  "contextFileName": "GEMINI.md"
}
```

### 6.5 Invocable skill

`skills/sdlc-strict-waterfall/SKILL.md`:

```markdown
---
name: sdlc-strict-waterfall
description: Strict waterfall SDLC methodology — doc-first, TDD inside slices, two-pass reconciliation gate, five-bucket triage, CR-driven changes.
---

# /sdlc-strict-waterfall

## Usage

/sdlc-strict-waterfall [start|phase <n>|rules|reconcile|change|hotfix]

## Core Rules

[5 non-negotiable rules — same as contract]

## Bootstrap Guard

[Same guard as Section 6.1]
```

## 7. README Updates

Replace the current "Quick start" section with:

```markdown
## Install

Pick your agent. One command. Done.

| Agent | Install |
|---|---|
| **Claude Code** | `claude plugin marketplace add Electronics-Extreme/claude-sdlc && claude plugin install claude-sdlc@claude-sdlc` |
| **Codex** | Clone repo → `/plugins` → Search "SDLC" → Install |
| **Gemini CLI** | `gemini extensions install https://github.com/Electronics-Extreme/claude-sdlc` |
| **Cursor** | `npx skills add Electronics-Extreme/claude-sdlc -a cursor` |
| **Windsurf** | `npx skills add Electronics-Extreme/claude-sdlc -a windsurf` |
| **Copilot** | `npx skills add Electronics-Extreme/claude-sdlc -a github-copilot` |
| **Cline** | `npx skills add Electronics-Extreme/claude-sdlc -a cline` |
| **Any other** | `npx skills add Electronics-Extreme/claude-sdlc` |

Install once. Use in every session. On first interaction, the agent loads the SDLC contract, detects a missing scaffold, and offers to bootstrap.

## Quick start (after install)

1. Open your project in the agent
2. Ask: "What are the 5 non-negotiable rules?"
3. Agent loads SDLC contract → detects no scaffold → offers bootstrap
4. Accept → `docs/sdlc/01_requirement/` … `06_maintenance/` created
5. Start spec in `docs/sdlc/01_requirement/srs.md`

## Manual bootstrap (alternative)

```bash
npx claude-sdlc init . --harness claude
```
```

Per-harness detail docs stay in `docs/INSTALL.*.md` but are demoted to "Option 2" or "Troubleshooting."

## 8. Package.json

No changes required. `npx skills add` does not read `package.json`. The npm package name (`claude-sdlc`) and CLI behavior stay unchanged.

## 9. Verification Plan

| Check | How |
|---|---|
| `.claude-plugin/plugin.json` valid | `python3 -m json.tool .claude-plugin/plugin.json` |
| `gemini-extension.json` valid | Same |
| `.cursor/rules/sdlc-contract.mdc` has frontmatter | `head -3` check |
| `.windsurf/rules/sdlc-contract.md` has frontmatter | `head -3` check |
| `skills/sdlc-strict-waterfall/SKILL.md` has frontmatter | `head -3` check |
| Bootstrap guard present in all rule files | Grep for "Bootstrap Guard" |
| README install table complete | Visual check |
| `npx skills add` simulation | Clone repo, run `npx skills add . -a cursor --dry-run` if available |

## 10. Open Questions

None — all sections approved by user.
