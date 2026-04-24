# Multi-Platform Install Support — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `.claude-plugin`, `npx skills`, `gemini extensions`, and Codex plugin discovery support to claude-sdlc, plus CLI default-to-cwd and scoped npm package setup.

**Architecture:** Root-level harness adapter files (`.claude-plugin/`, `.cursor/`, `.windsurf/`, `.clinerules/`, `.github/`, `.codex/`, `gemini-extension.json`, `skills/`) are consumed by install commands. Each skill/rule file embeds the SDLC contract + a bootstrap guard that detects missing scaffold and offers to create it. CLI `init` uses current directory by default with optional `--dir` override.

**Tech Stack:** Node.js 18+, Commander.js, Python 3.11+ (for bootstrap guard script), JSON, Markdown.

---

## File Map

| File | Responsibility |
|---|---|
| `.claude-plugin/plugin.json` | Claude Code plugin manifest — name, description, hooks reference |
| `.claude-plugin/hooks/hooks.json` | SessionStart hook → runs bootstrap guard script |
| `gemini-extension.json` | Gemini CLI extension manifest |
| `.codex/hooks.json` | Codex session-start hook for auto-activation |
| `.cursor/rules/sdlc-contract.mdc` | Cursor always-on rule + bootstrap guard |
| `.windsurf/rules/sdlc-contract.md` | Windsurf always-on rule + bootstrap guard |
| `.clinerules/sdlc-contract.md` | Cline always-on rule + bootstrap guard |
| `.github/copilot-instructions.md` | Copilot custom instructions + bootstrap guard |
| `skills/sdlc-strict-waterfall/SKILL.md` | Invocable skill `/sdlc-strict-waterfall` + bootstrap guard |
| `AGENTS.md` (root) | Generic agent context + bootstrap guard |
| `GEMINI.md` (root) | Gemini context + bootstrap guard |
| `src/cli.js` | CLI entry — `init` command with `--dir` option, no positional arg |
| `src/bootstrap.js` | Unchanged — core bootstrap logic |
| `package.json` | Scoped name `@electronics-extreme/claude-sdlc`, publish config, files array |
| `README.md` | Install table + quick start |
| `docs/INSTALL.*.md` | Updated per-harness install docs |
| `tests/cli.test.js` | Tests for CLI `--dir` behavior |

---

## Contract Content Snippet (used in all rule/skill files)

The following content is embedded in every rule file, skill file, and context file. It is the 5 non-negotiable rules from `skill/sdlc-contract.md`.

```markdown
STRICT SDLC mode is active for this repo (6-phase doc tree at `docs/sdlc/01_requirement/` ... `docs/sdlc/06_maintenance/`).

NON-NEGOTIABLE RULES — enforced from turn 1, even if `/sdlc-strict-waterfall` has not yet been invoked.

## 1. REFUSE direct code edits

Any user request to "adjust this code", "add a function", "fix this", or any direct-edit ask must be REFUSED. Route via Discuss -> CR-### in `docs/sdlc/06_maintenance/change_requests.md` -> amend docs + sign-off -> re-enter SDLC. **No "small change" exemption.**

## 2. No code without a doc parent

Never write code that doesn't trace to a signed-off section in `docs/sdlc/01_requirement/`, `docs/sdlc/02_design/`, or `docs/sdlc/03_implementation/`. Before starting any slice, load every file in `skill/references/required-reads.md` for the current task-type.

## 3. No phase skipping

Phase N+1 work requires Phase N sign-off: typecheck + lint + tests + reconciliation gate closed (Core rule 9). Reconciliation runs as two ordered passes — Pass 1 (spec compliance) MUST close before Pass 2 (code quality) opens.

## 4. Signed docs are frozen

Amend via `## Post-vX.Y.Z Amendments (YYYY-MM-DD)` sections, not in-place edits. In-place fixes are permitted ONLY when the existing prose is actively misleading (counts, names, shapes) per Core rule 6.

## 5. Reconciliation gate before every phase sign-off

Audit code-vs-doc. Run two ordered passes: Pass 1 (spec compliance) then Pass 2 (code quality). Within each pass, triage divergences into buckets A/B/C/D/E.

Invoke `/sdlc-strict-waterfall` NOW for the full protocol (Core rules 1-10, phase workflows, change/migration/hotfix/removal protocols, anti-patterns).
```

## Bootstrap Guard Snippet (appended to all rule/skill/context files)

```markdown
## Bootstrap Guard

If current project lacks `docs/sdlc/01_requirement/`:

1. Inform user: "SDLC scaffold not detected in this project."
2. Offer: "Shall I bootstrap the SDLC structure here?"
3. If yes, run ONE of:
   - Node available -> `npx @electronics-extreme/claude-sdlc init --harness <detected>`
   - No Node -> `git clone https://github.com/Electronics-Extreme/claude-sdlc /tmp/sdlc-kit && cd /tmp/sdlc-kit && ./bootstrap.sh --harness <detected>`
4. After bootstrap, instruct user to restart agent session for hooks to register.
```

---

### Task 1: Create `.claude-plugin/plugin.json`

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/hooks/hooks.json`

- [ ] **Step 1: Write plugin manifest**

Create `.claude-plugin/plugin.json`:

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

- [ ] **Step 2: Write hooks.json**

Create `.claude-plugin/hooks/hooks.json`:

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

- [ ] **Step 3: Validate JSON**

Run:
```bash
python3 -m json.tool .claude-plugin/plugin.json > /dev/null && echo "plugin.json valid"
python3 -m json.tool .claude-plugin/hooks/hooks.json > /dev/null && echo "hooks.json valid"
```

Expected: both print "valid".

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/
git commit -m "feat: add .claude-plugin manifest for claude plugin marketplace"
```

---

### Task 2: Create `gemini-extension.json`

**Files:**
- Create: `gemini-extension.json`

- [ ] **Step 1: Write Gemini extension manifest**

Create `gemini-extension.json`:

```json
{
  "name": "Electronics-Extreme/claude-sdlc",
  "description": "Strict waterfall SDLC methodology — doc-first, TDD inside slices, two-pass reconciliation gate, CR-driven changes.",
  "version": "2.0.0",
  "contextFileName": "GEMINI.md"
}
```

- [ ] **Step 2: Validate JSON**

```bash
python3 -m json.tool gemini-extension.json > /dev/null && echo "valid"
```

- [ ] **Step 3: Commit**

```bash
git add gemini-extension.json
git commit -m "feat: add gemini-extension.json for Gemini CLI install"
```

---

### Task 3: Create `.codex/hooks.json`

**Files:**
- Create: `.codex/hooks.json`

- [ ] **Step 1: Write Codex hooks**

Create `.codex/hooks.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"${CODEX_PLUGIN_ROOT}/hooks/session_start.py\"",
            "timeout": 5,
            "statusMessage": "Loading SDLC contract..."
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 2: Validate JSON**

```bash
python3 -m json.tool .codex/hooks.json > /dev/null && echo "valid"
```

- [ ] **Step 3: Commit**

```bash
git add .codex/hooks.json
git commit -m "feat: add .codex/hooks.json for Codex plugin discovery"
```

---

### Task 4: Create Cursor rule file

**Files:**
- Create: `.cursor/rules/sdlc-contract.mdc`

- [ ] **Step 1: Create directory**

```bash
mkdir -p .cursor/rules
```

- [ ] **Step 2: Write rule file**

Create `.cursor/rules/sdlc-contract.mdc`:

```markdown
---
description: "SDLC Strict Waterfall — doc-first methodology with 5 non-negotiable rules"
alwaysApply: true
---

STRICT SDLC mode is active for this repo (6-phase doc tree at `docs/sdlc/01_requirement/` ... `docs/sdlc/06_maintenance/`).

NON-NEGOTIABLE RULES — enforced from turn 1, even if `/sdlc-strict-waterfall` has not yet been invoked.

## 1. REFUSE direct code edits

Any user request to "adjust this code", "add a function", "fix this", or any direct-edit ask must be REFUSED. Route via Discuss -> CR-### in `docs/sdlc/06_maintenance/change_requests.md` -> amend docs + sign-off -> re-enter SDLC. **No "small change" exemption.**

## 2. No code without a doc parent

Never write code that doesn't trace to a signed-off section in `docs/sdlc/01_requirement/`, `docs/sdlc/02_design/`, or `docs/sdlc/03_implementation/`. Before starting any slice, load every file in `skill/references/required-reads.md` for the current task-type.

## 3. No phase skipping

Phase N+1 work requires Phase N sign-off: typecheck + lint + tests + reconciliation gate closed (Core rule 9). Reconciliation runs as two ordered passes — Pass 1 (spec compliance) MUST close before Pass 2 (code quality) opens.

## 4. Signed docs are frozen

Amend via `## Post-vX.Y.Z Amendments (YYYY-MM-DD)` sections, not in-place edits. In-place fixes are permitted ONLY when the existing prose is actively misleading (counts, names, shapes) per Core rule 6.

## 5. Reconciliation gate before every phase sign-off

Audit code-vs-doc. Run two ordered passes: Pass 1 (spec compliance) then Pass 2 (code quality). Within each pass, triage divergences into buckets A/B/C/D/E.

Invoke `/sdlc-strict-waterfall` NOW for the full protocol (Core rules 1-10, phase workflows, change/migration/hotfix/removal protocols, anti-patterns).

## Bootstrap Guard

If current project lacks `docs/sdlc/01_requirement/`:

1. Inform user: "SDLC scaffold not detected in this project."
2. Offer: "Shall I bootstrap the SDLC structure here?"
3. If yes, run ONE of:
   - Node available -> `npx @electronics-extreme/claude-sdlc init --harness cursor`
   - No Node -> `git clone https://github.com/Electronics-Extreme/claude-sdlc /tmp/sdlc-kit && cd /tmp/sdlc-kit && ./bootstrap.sh --harness cursor`
4. After bootstrap, instruct user to restart agent session for hooks to register.
```

- [ ] **Step 3: Verify frontmatter**

```bash
head -4 .cursor/rules/sdlc-contract.mdc
```

Expected:
```
---
description: "SDLC Strict Waterfall — doc-first methodology with 5 non-negotiable rules"
alwaysApply: true
---
```

- [ ] **Step 4: Commit**

```bash
git add .cursor/
git commit -m "feat: add Cursor rule file for npx skills add -a cursor"
```

---

### Task 5: Create Windsurf rule file

**Files:**
- Create: `.windsurf/rules/sdlc-contract.md`

- [ ] **Step 1: Create directory**

```bash
mkdir -p .windsurf/rules
```

- [ ] **Step 2: Write rule file**

Create `.windsurf/rules/sdlc-contract.md`:

```markdown
---
trigger: always_on
---

STRICT SDLC mode is active for this repo (6-phase doc tree at `docs/sdlc/01_requirement/` ... `docs/sdlc/06_maintenance/`).

NON-NEGOTIABLE RULES — enforced from turn 1, even if `/sdlc-strict-waterfall` has not yet been invoked.

## 1. REFUSE direct code edits

Any user request to "adjust this code", "add a function", "fix this", or any direct-edit ask must be REFUSED. Route via Discuss -> CR-### in `docs/sdlc/06_maintenance/change_requests.md` -> amend docs + sign-off -> re-enter SDLC. **No "small change" exemption.**

## 2. No code without a doc parent

Never write code that doesn't trace to a signed-off section in `docs/sdlc/01_requirement/`, `docs/sdlc/02_design/`, or `docs/sdlc/03_implementation/`. Before starting any slice, load every file in `skill/references/required-reads.md` for the current task-type.

## 3. No phase skipping

Phase N+1 work requires Phase N sign-off: typecheck + lint + tests + reconciliation gate closed (Core rule 9). Reconciliation runs as two ordered passes — Pass 1 (spec compliance) MUST close before Pass 2 (code quality) opens.

## 4. Signed docs are frozen

Amend via `## Post-vX.Y.Z Amendments (YYYY-MM-DD)` sections, not in-place edits. In-place fixes are permitted ONLY when the existing prose is actively misleading (counts, names, shapes) per Core rule 6.

## 5. Reconciliation gate before every phase sign-off

Audit code-vs-doc. Run two ordered passes: Pass 1 (spec compliance) then Pass 2 (code quality). Within each pass, triage divergences into buckets A/B/C/D/E.

Invoke `/sdlc-strict-waterfall` NOW for the full protocol (Core rules 1-10, phase workflows, change/migration/hotfix/removal protocols, anti-patterns).

## Bootstrap Guard

If current project lacks `docs/sdlc/01_requirement/`:

1. Inform user: "SDLC scaffold not detected in this project."
2. Offer: "Shall I bootstrap the SDLC structure here?"
3. If yes, run ONE of:
   - Node available -> `npx @electronics-extreme/claude-sdlc init --harness windsurf`
   - No Node -> `git clone https://github.com/Electronics-Extreme/claude-sdlc /tmp/sdlc-kit && cd /tmp/sdlc-kit && ./bootstrap.sh --harness windsurf`
4. After bootstrap, instruct user to restart agent session for hooks to register.
```

- [ ] **Step 3: Verify frontmatter**

```bash
head -3 .windsurf/rules/sdlc-contract.md
```

Expected:
```
---
trigger: always_on
---
```

- [ ] **Step 4: Commit**

```bash
git add .windsurf/
git commit -m "feat: add Windsurf rule file for npx skills add -a windsurf"
```

---

### Task 6: Create Cline rule file

**Files:**
- Create: `.clinerules/sdlc-contract.md`

- [ ] **Step 1: Create directory**

```bash
mkdir -p .clinerules
```

- [ ] **Step 2: Write rule file**

Create `.clinerules/sdlc-contract.md`:

```markdown
STRICT SDLC mode is active for this repo (6-phase doc tree at `docs/sdlc/01_requirement/` ... `docs/sdlc/06_maintenance/`).

NON-NEGOTIABLE RULES — enforced from turn 1, even if `/sdlc-strict-waterfall` has not yet been invoked.

## 1. REFUSE direct code edits

Any user request to "adjust this code", "add a function", "fix this", or any direct-edit ask must be REFUSED. Route via Discuss -> CR-### in `docs/sdlc/06_maintenance/change_requests.md` -> amend docs + sign-off -> re-enter SDLC. **No "small change" exemption.**

## 2. No code without a doc parent

Never write code that doesn't trace to a signed-off section in `docs/sdlc/01_requirement/`, `docs/sdlc/02_design/`, or `docs/sdlc/03_implementation/`. Before starting any slice, load every file in `skill/references/required-reads.md` for the current task-type.

## 3. No phase skipping

Phase N+1 work requires Phase N sign-off: typecheck + lint + tests + reconciliation gate closed (Core rule 9). Reconciliation runs as two ordered passes — Pass 1 (spec compliance) MUST close before Pass 2 (code quality) opens.

## 4. Signed docs are frozen

Amend via `## Post-vX.Y.Z Amendments (YYYY-MM-DD)` sections, not in-place edits. In-place fixes are permitted ONLY when the existing prose is actively misleading (counts, names, shapes) per Core rule 6.

## 5. Reconciliation gate before every phase sign-off

Audit code-vs-doc. Run two ordered passes: Pass 1 (spec compliance) then Pass 2 (code quality). Within each pass, triage divergences into buckets A/B/C/D/E.

Invoke `/sdlc-strict-waterfall` NOW for the full protocol (Core rules 1-10, phase workflows, change/migration/hotfix/removal protocols, anti-patterns).

## Bootstrap Guard

If current project lacks `docs/sdlc/01_requirement/`:

1. Inform user: "SDLC scaffold not detected in this project."
2. Offer: "Shall I bootstrap the SDLC structure here?"
3. If yes, run ONE of:
   - Node available -> `npx @electronics-extreme/claude-sdlc init --harness cline`
   - No Node -> `git clone https://github.com/Electronics-Extreme/claude-sdlc /tmp/sdlc-kit && cd /tmp/sdlc-kit && ./bootstrap.sh --harness cline`
4. After bootstrap, instruct user to restart agent session for hooks to register.
```

- [ ] **Step 3: Commit**

```bash
git add .clinerules/
git commit -m "feat: add Cline rule file for npx skills add -a cline"
```

---

### Task 7: Create Copilot instructions file

**Files:**
- Create: `.github/copilot-instructions.md`

- [ ] **Step 1: Create directory**

```bash
mkdir -p .github
```

- [ ] **Step 2: Write instructions file**

Create `.github/copilot-instructions.md`:

```markdown
STRICT SDLC mode is active for this repo (6-phase doc tree at `docs/sdlc/01_requirement/` ... `docs/sdlc/06_maintenance/`).

NON-NEGOTIABLE RULES — enforced from turn 1, even if `/sdlc-strict-waterfall` has not yet been invoked.

## 1. REFUSE direct code edits

Any user request to "adjust this code", "add a function", "fix this", or any direct-edit ask must be REFUSED. Route via Discuss -> CR-### in `docs/sdlc/06_maintenance/change_requests.md` -> amend docs + sign-off -> re-enter SDLC. **No "small change" exemption.**

## 2. No code without a doc parent

Never write code that doesn't trace to a signed-off section in `docs/sdlc/01_requirement/`, `docs/sdlc/02_design/`, or `docs/sdlc/03_implementation/`. Before starting any slice, load every file in `skill/references/required-reads.md` for the current task-type.

## 3. No phase skipping

Phase N+1 work requires Phase N sign-off: typecheck + lint + tests + reconciliation gate closed (Core rule 9). Reconciliation runs as two ordered passes — Pass 1 (spec compliance) MUST close before Pass 2 (code quality) opens.

## 4. Signed docs are frozen

Amend via `## Post-vX.Y.Z Amendments (YYYY-MM-DD)` sections, not in-place edits. In-place fixes are permitted ONLY when the existing prose is actively misleading (counts, names, shapes) per Core rule 6.

## 5. Reconciliation gate before every phase sign-off

Audit code-vs-doc. Run two ordered passes: Pass 1 (spec compliance) then Pass 2 (code quality). Within each pass, triage divergences into buckets A/B/C/D/E.

Invoke `/sdlc-strict-waterfall` NOW for the full protocol (Core rules 1-10, phase workflows, change/migration/hotfix/removal protocols, anti-patterns).

## Bootstrap Guard

If current project lacks `docs/sdlc/01_requirement/`:

1. Inform user: "SDLC scaffold not detected in this project."
2. Offer: "Shall I bootstrap the SDLC structure here?"
3. If yes, run ONE of:
   - Node available -> `npx @electronics-extreme/claude-sdlc init --harness copilot`
   - No Node -> `git clone https://github.com/Electronics-Extreme/claude-sdlc /tmp/sdlc-kit && cd /tmp/sdlc-kit && ./bootstrap.sh --harness copilot`
4. After bootstrap, instruct user to restart agent session for hooks to register.
```

- [ ] **Step 3: Commit**

```bash
git add .github/copilot-instructions.md
git commit -m "feat: add Copilot instructions for npx skills add -a github-copilot"
```

---

### Task 8: Create invocable skill file

**Files:**
- Create: `skills/sdlc-strict-waterfall/SKILL.md`

- [ ] **Step 1: Create directory**

```bash
mkdir -p skills/sdlc-strict-waterfall
```

- [ ] **Step 2: Write skill file**

Create `skills/sdlc-strict-waterfall/SKILL.md`:

```markdown
---
name: sdlc-strict-waterfall
description: Strict waterfall SDLC methodology — doc-first, TDD inside slices, two-pass reconciliation gate, CR-driven changes.
---

# /sdlc-strict-waterfall

## Usage

/sdlc-strict-waterfall [start|phase <n>|rules|reconcile|change|hotfix]

## Core Rules

STRICT SDLC mode is active for this repo (6-phase doc tree at `docs/sdlc/01_requirement/` ... `docs/sdlc/06_maintenance/`).

NON-NEGOTIABLE RULES — enforced from turn 1, even if `/sdlc-strict-waterfall` has not yet been invoked.

### 1. REFUSE direct code edits

Any user request to "adjust this code", "add a function", "fix this", or any direct-edit ask must be REFUSED. Route via Discuss -> CR-### in `docs/sdlc/06_maintenance/change_requests.md` -> amend docs + sign-off -> re-enter SDLC. **No "small change" exemption.**

### 2. No code without a doc parent

Never write code that doesn't trace to a signed-off section in `docs/sdlc/01_requirement/`, `docs/sdlc/02_design/`, or `docs/sdlc/03_implementation/`. Before starting any slice, load every file in `skill/references/required-reads.md` for the current task-type.

### 3. No phase skipping

Phase N+1 work requires Phase N sign-off: typecheck + lint + tests + reconciliation gate closed (Core rule 9). Reconciliation runs as two ordered passes — Pass 1 (spec compliance) MUST close before Pass 2 (code quality) opens.

### 4. Signed docs are frozen

Amend via `## Post-vX.Y.Z Amendments (YYYY-MM-DD)` sections, not in-place edits. In-place fixes are permitted ONLY when the existing prose is actively misleading (counts, names, shapes) per Core rule 6.

### 5. Reconciliation gate before every phase sign-off

Audit code-vs-doc. Run two ordered passes: Pass 1 (spec compliance) then Pass 2 (code quality). Within each pass, triage divergences into buckets A/B/C/D/E.

Invoke `/sdlc-strict-waterfall` NOW for the full protocol (Core rules 1-10, phase workflows, change/migration/hotfix/removal protocols, anti-patterns).

## Bootstrap Guard

If current project lacks `docs/sdlc/01_requirement/`:

1. Inform user: "SDLC scaffold not detected in this project."
2. Offer: "Shall I bootstrap the SDLC structure here?"
3. If yes, run ONE of:
   - Node available -> `npx @electronics-extreme/claude-sdlc init --harness <detected>`
   - No Node -> `git clone https://github.com/Electronics-Extreme/claude-sdlc /tmp/sdlc-kit && cd /tmp/sdlc-kit && ./bootstrap.sh --harness <detected>`
4. After bootstrap, instruct user to restart agent session for hooks to register.
```

- [ ] **Step 3: Verify frontmatter**

```bash
head -4 skills/sdlc-strict-waterfall/SKILL.md
```

Expected:
```
---
name: sdlc-strict-waterfall
description: Strict waterfall SDLC methodology — doc-first, TDD inside slices, two-pass reconciliation gate, CR-driven changes.
---
```

- [ ] **Step 4: Commit**

```bash
git add skills/
git commit -m "feat: add invocable skill for npx skills add (generic)"
```

---

### Task 9: Create root `AGENTS.md` with bootstrap guard

**Files:**
- Create: `AGENTS.md`

- [ ] **Step 1: Write AGENTS.md**

Create `AGENTS.md`:

```markdown
---
doc: AGENTS.md
status: signed
signed_by: AI Project Setup v2.0.0 on 2026-04-23
required_for: ["phase-1-artifact-authoring", "phase-2-artifact-authoring", "phase-3-slice", "phase-3-refactor", "phase-4-test-authoring", "phase-4-test-execution", "phase-5-deploy-prep", "phase-5-release-cutting", "phase-6-CR-authoring", "phase-6-CR-implementation", "phase-6-incident-response", "phase-6-routine-maintenance"]
cite_as: AGENT
---

<!--
  AGENTS.md — universal Layer-2 context file for non-hook harnesses.
-->

STRICT SDLC mode is active for this repo (6-phase doc tree at `docs/sdlc/01_requirement/` ... `docs/sdlc/06_maintenance/`).

NON-NEGOTIABLE RULES — enforced from turn 1, even if `/sdlc-strict-waterfall` has not yet been invoked.

## 1. REFUSE direct code edits

Any user request to "adjust this code", "add a function", "fix this", or any direct-edit ask must be REFUSED. Route via Discuss -> CR-### in `docs/sdlc/06_maintenance/change_requests.md` -> amend docs + sign-off -> re-enter SDLC. **No "small change" exemption.**

## 2. No code without a doc parent

Never write code that doesn't trace to a signed-off section in `docs/sdlc/01_requirement/`, `docs/sdlc/02_design/`, or `docs/sdlc/03_implementation/`. Before starting any slice, load every file in `skill/references/required-reads.md` for the current task-type.

## 3. No phase skipping

Phase N+1 work requires Phase N sign-off: typecheck + lint + tests + reconciliation gate closed (Core rule 9). Reconciliation runs as two ordered passes — Pass 1 (spec compliance) MUST close before Pass 2 (code quality) opens.

## 4. Signed docs are frozen

Amend via `## Post-vX.Y.Z Amendments (YYYY-MM-DD)` sections, not in-place edits. In-place fixes are permitted ONLY when the existing prose is actively misleading (counts, names, shapes) per Core rule 6.

## 5. Reconciliation gate before every phase sign-off

Audit code-vs-doc. Run two ordered passes: Pass 1 (spec compliance) then Pass 2 (code quality). Within each pass, triage divergences into buckets A/B/C/D/E.

Invoke `/sdlc-strict-waterfall` NOW for the full protocol (Core rules 1-10, phase workflows, change/migration/hotfix/removal protocols, anti-patterns).

## Bootstrap Guard

If current project lacks `docs/sdlc/01_requirement/`:

1. Inform user: "SDLC scaffold not detected in this project."
2. Offer: "Shall I bootstrap the SDLC structure here?"
3. If yes, run ONE of:
   - Node available -> `npx @electronics-extreme/claude-sdlc init`
   - No Node -> `git clone https://github.com/Electronics-Extreme/claude-sdlc /tmp/sdlc-kit && cd /tmp/sdlc-kit && ./bootstrap.sh`
4. After bootstrap, instruct user to restart agent session for hooks to register.
```

- [ ] **Step 2: Commit**

```bash
git add AGENTS.md
git commit -m "feat: add root AGENTS.md with bootstrap guard"
```

---

### Task 10: Create root `GEMINI.md` with bootstrap guard

**Files:**
- Create: `GEMINI.md`

- [ ] **Step 1: Write GEMINI.md**

Create `GEMINI.md`:

```markdown
---
doc: GEMINI.md
status: signed
signed_by: AI Project Setup v2.0.0 on 2026-04-23
required_for: ["phase-1-artifact-authoring", "phase-2-artifact-authoring", "phase-3-slice", "phase-3-refactor", "phase-4-test-authoring", "phase-4-test-execution", "phase-5-deploy-prep", "phase-5-release-cutting", "phase-6-CR-authoring", "phase-6-CR-implementation", "phase-6-incident-response", "phase-6-routine-maintenance"]
cite_as: GEM
---

<!--
  GEMINI.md — Gemini CLI Layer-2 context file.
  Referenced from gemini-extension.json via `contextFileName`.
-->

STRICT SDLC mode is active for this repo (6-phase doc tree at `docs/sdlc/01_requirement/` ... `docs/sdlc/06_maintenance/`).

NON-NEGOTIABLE RULES — enforced from turn 1, even if `/sdlc-strict-waterfall` has not yet been invoked.

## 1. REFUSE direct code edits

Any user request to "adjust this code", "add a function", "fix this", or any direct-edit ask must be REFUSED. Route via Discuss -> CR-### in `docs/sdlc/06_maintenance/change_requests.md` -> amend docs + sign-off -> re-enter SDLC. **No "small change" exemption.**

## 2. No code without a doc parent

Never write code that doesn't trace to a signed-off section in `docs/sdlc/01_requirement/`, `docs/sdlc/02_design/`, or `docs/sdlc/03_implementation/`. Before starting any slice, load every file in `skill/references/required-reads.md` for the current task-type.

## 3. No phase skipping

Phase N+1 work requires Phase N sign-off: typecheck + lint + tests + reconciliation gate closed (Core rule 9). Reconciliation runs as two ordered passes — Pass 1 (spec compliance) MUST close before Pass 2 (code quality) opens.

## 4. Signed docs are frozen

Amend via `## Post-vX.Y.Z Amendments (YYYY-MM-DD)` sections, not in-place edits. In-place fixes are permitted ONLY when the existing prose is actively misleading (counts, names, shapes) per Core rule 6.

## 5. Reconciliation gate before every phase sign-off

Audit code-vs-doc. Run two ordered passes: Pass 1 (spec compliance) then Pass 2 (code quality). Within each pass, triage divergences into buckets A/B/C/D/E.

Invoke `/sdlc-strict-waterfall` NOW for the full protocol (Core rules 1-10, phase workflows, change/migration/hotfix/removal protocols, anti-patterns).

## Bootstrap Guard

If current project lacks `docs/sdlc/01_requirement/`:

1. Inform user: "SDLC scaffold not detected in this project."
2. Offer: "Shall I bootstrap the SDLC structure here?"
3. If yes, run ONE of:
   - Node available -> `npx @electronics-extreme/claude-sdlc init --harness gemini`
   - No Node -> `git clone https://github.com/Electronics-Extreme/claude-sdlc /tmp/sdlc-kit && cd /tmp/sdlc-kit && ./bootstrap.sh --harness gemini`
4. After bootstrap, instruct user to restart agent session for hooks to register.
```

- [ ] **Step 2: Commit**

```bash
git add GEMINI.md
git commit -m "feat: add root GEMINI.md with bootstrap guard"
```

---

### Task 11: Update CLI — default to cwd, add `--dir` option

**Files:**
- Modify: `src/cli.js`
- Create: `tests/cli.test.js`

- [ ] **Step 1: Write failing test**

Create `tests/cli.test.js`:

```javascript
const { describe, it } = require('node:test');
const assert = require('node:assert');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

describe('cli init', () => {
  it('defaults to current directory when no --dir provided', () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'sdlc-test-'));
    const result = execSync(
      `node ${path.resolve('src/cli.js')} init --harness claude`,
      { cwd: tmpDir, encoding: 'utf8' }
    );
    assert.ok(fs.existsSync(path.join(tmpDir, 'docs', 'sdlc', '01_requirement')));
  });

  it('uses --dir override when provided', () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'sdlc-test-'));
    const targetDir = path.join(tmpDir, 'target');
    const result = execSync(
      `node ${path.resolve('src/cli.js')} init --dir ${targetDir} --harness claude`,
      { cwd: tmpDir, encoding: 'utf8' }
    );
    assert.ok(fs.existsSync(path.join(targetDir, 'docs', 'sdlc', '01_requirement')));
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

```bash
node --test tests/cli.test.js
```

Expected: FAIL — `init` still requires positional `<dir>` argument, `--dir` option not recognized.

- [ ] **Step 3: Modify CLI**

Edit `src/cli.js`. Change:

```javascript
program
  .command('init <dir>')
  .description('Initialize a new SDLC project in the target directory')
  .option('-f, --force', 'Overlay non-empty directory without prompting')
  .option(
    '--harness <name>',
    `Harness wrapper(s) to install. One of: ${HARNESS_CHOICES.join(', ')}`,
    'all',
  )
  .action(async (dir, options) => {
    const targetDir = path.resolve(dir);

    if (fs.existsSync(targetDir) && fs.readdirSync(targetDir).length > 0 && !options.force) {
      const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
      const answer = await new Promise((resolve) => {
        rl.question(`Target ${targetDir} is not empty. Overlay anyway? [y/N] `, resolve);
      });
      rl.close();
      if (!/^y(es)?$/i.test(answer)) {
        console.error('aborted.');
        process.exit(1);
      }
    }
```

To:

```javascript
program
  .command('init')
  .description('Initialize SDLC scaffold in the target directory (default: current directory)')
  .option('-f, --force', 'Overlay non-empty directory without prompting')
  .option(
    '--harness <name>',
    `Harness wrapper(s) to install. One of: ${HARNESS_CHOICES.join(', ')}`,
    'all',
  )
  .option('--dir <path>', 'Target directory (default: current directory)', '.')
  .action(async (options) => {
    const targetDir = path.resolve(options.dir);

    // Always proceed — cwd is expected to be the project root.
    // --force retained for backward compatibility (no-op).
```

- [ ] **Step 4: Run test to verify it passes**

```bash
node --test tests/cli.test.js
```

Expected: PASS on both tests.

- [ ] **Step 5: Commit**

```bash
git add src/cli.js tests/cli.test.js
git commit -m "feat: CLI init defaults to cwd, --dir override, no positional arg"
```

---

### Task 12: Update `package.json` for scoped publish

**Files:**
- Modify: `package.json`

- [ ] **Step 1: Update package.json**

Edit `package.json`:

```json
{
  "name": "@electronics-extreme/claude-sdlc",
  "version": "2.0.0",
  "description": "Cross-platform CLI to bootstrap a frozen Waterfall SDLC scaffold for Claude Code / Cursor / Codex / Gemini / Copilot CLI / OpenCode. Runtime requires Python 3.11+.",
  "keywords": ["sdlc", "waterfall", "bootstrap", "claude-code", "cursor", "codex", "gemini", "copilot-cli", "opencode"],
  "homepage": "https://github.com/Electronics-Extreme/claude-sdlc",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/Electronics-Extreme/claude-sdlc.git"
  },
  "bugs": "https://github.com/Electronics-Extreme/claude-sdlc/issues",
  "license": "MIT",
  "main": "src/cli.js",
  "bin": {
    "claude-sdlc": "./src/cli.js"
  },
  "files": [
    "src",
    "template",
    ".claude-plugin",
    ".cursor",
    ".windsurf",
    ".clinerules",
    ".github",
    ".codex",
    "gemini-extension.json",
    "skills",
    "AGENTS.md",
    "GEMINI.md",
    "README.md",
    "LICENSE",
    "NOTICE.md",
    "VERSION"
  ],
  "engines": {
    "node": ">=18.0.0"
  },
  "dependencies": {
    "commander": "^12.1.0"
  },
  "publishConfig": {
    "access": "public",
    "registry": "https://registry.npmjs.org/"
  },
  "scripts": {
    "test": "node --test tests/**/*.test.js"
  }
}
```

- [ ] **Step 2: Validate JSON**

```bash
python3 -m json.tool package.json > /dev/null && echo "valid"
```

- [ ] **Step 3: Verify files array**

```bash
npm pack --dry-run
```

Expected: output lists `.claude-plugin/`, `.cursor/`, `.windsurf/`, `.clinerules/`, `.github/`, `.codex/`, `gemini-extension.json`, `skills/`, `AGENTS.md`, `GEMINI.md`.

- [ ] **Step 4: Commit**

```bash
git add package.json
git commit -m "feat: scoped npm package @electronics-extreme/claude-sdlc with publish config"
```

---

### Task 13: Update README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace Quick start section**

Find the "## Quick start" section in `README.md` (starts around line 27). Replace it with:

```markdown
## Install

Pick your agent. One command. Done.

| Agent | Install |
|---|---|
| **Claude Code** | `claude plugin marketplace add Electronics-Extreme/claude-sdlc && claude plugin install claude-sdlc@claude-sdlc` |
| **Codex** | Clone repo -> `/plugins` -> Search "SDLC" -> Install |
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
3. Agent loads SDLC contract -> detects no scaffold -> offers bootstrap
4. Accept -> `docs/sdlc/01_requirement/` ... `06_maintenance/` created
5. Start spec in `docs/sdlc/01_requirement/srs.md`

## Manual bootstrap (alternative)

```bash
# Run inside your project directory — no arguments needed
cd ~/Projects/MyApp
npx @electronics-extreme/claude-sdlc init --harness claude
```
```

Also update the `## What's in the kit` table row for Harness adapters to include the new root-level files.

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update README with multi-platform install table"
```

---

### Task 14: Update per-harness install docs

**Files:**
- Modify: `docs/INSTALL.claude-code.md`
- Modify: `docs/INSTALL.cursor.md`
- Modify: `docs/INSTALL.gemini.md`
- Modify: `docs/INSTALL.codex.md`
- Modify: `docs/INSTALL.copilot.md`

- [ ] **Step 1: Update `docs/INSTALL.claude-code.md`**

Add at the top of the Install section:

```markdown
### Option 1: Claude Code plugin (recommended)

```bash
claude plugin marketplace add Electronics-Extreme/claude-sdlc
claude plugin install claude-sdlc@claude-sdlc
```

### Option 2: Manual bootstrap
```

Keep existing Option A/B content as Option 2.

- [ ] **Step 2: Update `docs/INSTALL.cursor.md`**

Add at the top:

```markdown
### Option 1: npx skills (recommended)

```bash
npx skills add Electronics-Extreme/claude-sdlc -a cursor
```

### Option 2: Manual bootstrap
```

- [ ] **Step 3: Update `docs/INSTALL.gemini.md`**

Add at the top:

```markdown
### Option 1: Gemini extension (recommended)

```bash
gemini extensions install https://github.com/Electronics-Extreme/claude-sdlc
```

### Option 2: Manual bootstrap
```

- [ ] **Step 4: Update `docs/INSTALL.codex.md`**

Add at the top:

```markdown
### Option 1: Codex plugin discovery (recommended)

Clone this repo, then in Codex run `/plugins`, search "SDLC", and install.

### Option 2: Manual symlink
```

- [ ] **Step 5: Update `docs/INSTALL.copilot.md`**

Add at the top:

```markdown
### Option 1: npx skills (recommended)

```bash
npx skills add Electronics-Extreme/claude-sdlc -a github-copilot
```

### Option 2: Manual plugin install
```

- [ ] **Step 6: Commit**

```bash
git add docs/INSTALL.*.md
git commit -m "docs: update per-harness install docs with one-command options"
```

---

### Task 15: Final verification

- [ ] **Step 1: Run all tests**

```bash
npm test
```

Expected: PASS (tests/cli.test.js passes).

- [ ] **Step 2: Validate all JSON files**

```bash
for f in .claude-plugin/plugin.json .claude-plugin/hooks/hooks.json gemini-extension.json .codex/hooks.json; do
  python3 -m json.tool "$f" > /dev/null && echo "$f valid" || echo "$f INVALID"
done
```

Expected: all print "valid".

- [ ] **Step 3: Verify bootstrap guard in all rule files**

```bash
grep -l "Bootstrap Guard" .cursor/rules/sdlc-contract.mdc .windsurf/rules/sdlc-contract.md .clinerules/sdlc-contract.md .github/copilot-instructions.md skills/sdlc-strict-waterfall/SKILL.md AGENTS.md GEMINI.md
```

Expected: lists all 7 files.

- [ ] **Step 4: Verify npm pack includes harness adapters**

```bash
npm pack --dry-run 2>&1 | grep -E '\.claude-plugin|\.cursor|\.windsurf|\.clinerules|\.github|\.codex|gemini-extension|skills/'
```

Expected: lists all harness adapter paths.

- [ ] **Step 5: Commit verification results (optional)**

If all checks pass, no commit needed. If fixes were required, commit them.

---

## Spec Coverage Check

| Spec Section | Implementing Task |
|---|---|
| `.claude-plugin/plugin.json` | Task 1 |
| `.claude-plugin/hooks/hooks.json` | Task 1 |
| `gemini-extension.json` | Task 2 |
| `.codex/hooks.json` | Task 3 |
| `.cursor/rules/sdlc-contract.mdc` | Task 4 |
| `.windsurf/rules/sdlc-contract.md` | Task 5 |
| `.clinerules/sdlc-contract.md` | Task 6 |
| `.github/copilot-instructions.md` | Task 7 |
| `skills/sdlc-strict-waterfall/SKILL.md` | Task 8 |
| Root `AGENTS.md` | Task 9 |
| Root `GEMINI.md` | Task 10 |
| CLI default cwd, `--dir` option | Task 11 |
| Scoped npm package, publish config | Task 12 |
| README install table | Task 13 |
| Per-harness doc updates | Task 14 |
| Verification | Task 15 |

All spec requirements covered. No gaps.
