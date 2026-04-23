# Installing SDLC Strict Waterfall for Codex CLI

## Layer

Codex CLI uses **Layer 2** (no session-start hook API exists). The kit integrates via
Codex's native skill discovery + the `AGENTS.md` convention.

## Prerequisites

- OpenAI Codex CLI installed
- Git
- Python 3.11+ (only needed if you plan to use the metrics subsystem or other scripts)

## Install

1. Clone the kit (or bootstrap a new project from the kit):

```bash
git clone https://github.com/Electronics-Extreme/claude-sdlc.git ~/.codex/sdlc-kit
```

2. Symlink the skills directory into Codex's discovery path:

```bash
mkdir -p ~/.agents/skills
ln -s ~/.codex/sdlc-kit/skill ~/.agents/skills/sdlc-strict-waterfall
```

**Windows (PowerShell):**

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
cmd /c mklink /J "$env:USERPROFILE\.agents\skills\sdlc-strict-waterfall" "$env:USERPROFILE\.codex\sdlc-kit\skill"
```

3. Restart Codex. The skill auto-activates via its frontmatter description.

4. Verify `AGENTS.md` is present at the project root — Codex reads it on start.

## Verify the contract loaded

After restart, ask Codex:

> What are the 5 non-negotiable rules of this SDLC?

Expected: Codex should echo the 5 rules from `AGENTS.md` (and `skill/sdlc-contract.md`
by reference).

## Troubleshooting

- **Skill not showing up** → verify `ls ~/.agents/skills/sdlc-strict-waterfall` returns a
  symlink; restart Codex.
- **Rules not cited** → `AGENTS.md` may not be in the repo root (or the adopter's
  project root). Confirm it's present and readable.
