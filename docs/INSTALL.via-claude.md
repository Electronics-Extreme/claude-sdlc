---
doc: docs/INSTALL.via-claude.md
status: signed
signed_by: AI Project Setup v2.0.0 on 2026-04-23
required_for: [phase-6-CR-implementation]
cite_as: INST-CC
---

# Install via Claude Code (LLM-assisted)

Skip the terminal. Open Claude Code in the directory where you want the kit
installed, then paste the prompt below as your first message.

## Prerequisites

- Claude Code open in the target project directory
- Python 3.11+ on PATH (`python3 --version`)
- A real network for the initial download

That's it. No `git`, `curl`, `unzip`, or shell scripting required from you —
Claude drives all of them via its Bash tool.

## The prompt

Copy everything between the lines below and paste as your first message:

---

> Install the SDLC Strict Waterfall kit in the current directory. Proceed
> autonomously — do not ask me to confirm each step.
>
> 1. Verify `python3 --version` is 3.11 or higher. If not, stop and tell me.
> 2. Create a temporary working directory: `mktemp -d`.
> 3. Download the release archive + its SHA256 manifest to that tempdir:
>    ```
>    BASE=https://github.com/Electronics-Extreme/claude-sdlc/releases/download/v2.0.0
>    curl -sSfL -o dist.zip         "$BASE/dist.zip"
>    curl -sSfL -o dist.zip.sha256  "$BASE/dist.zip.sha256"
>    ```
> 4. Verify SHA256:
>    ```
>    expected=$(awk '{print $1}' dist.zip.sha256)
>    actual=$(shasum -a 256 dist.zip | awk '{print $1}')
>    [ "$expected" = "$actual" ] || { echo "SHA mismatch"; exit 1; }
>    ```
> 5. Unzip to the tempdir: `unzip -q dist.zip`.
> 6. Run: `bash <tempdir>/dist/bootstrap.sh . --harness claude`
> 7. Remove the tempdir.
> 8. Show me the Next-Steps output verbatim.
> 9. Finally, tell me to CLOSE AND REOPEN Claude Code before typing
>    `/sdlc-strict-waterfall` — hooks registered mid-session don't fire
>    until next session.

---

## What to expect

Claude will run each step with Bash, show output, and stop if anything fails
(missing Python, SHA mismatch, permission error). Expected runtime: ~15
seconds. The terminal output will look identical to running `bootstrap.sh`
directly.

## Why the restart is required

`.claude/settings.json` is read once at session start. Registering a new
SessionStart hook mid-session leaves it dormant until Claude Code starts a
fresh session. Trying to `/sdlc-strict-waterfall` in the same session where
you installed will work (the skill file is on disk), but the auto-loaded
contract will be absent — you'll lose the "from turn 1" enforcement.

## Other harnesses

Swap step 6's `--harness` flag for your harness:

| Harness          | Flag                |
|------------------|---------------------|
| Claude Code      | `--harness claude`  |
| Cursor Agent     | `--harness cursor`  |
| Codex CLI        | `--harness codex`   |
| Gemini CLI       | `--harness gemini`  |
| Copilot CLI      | `--harness copilot` |
| OpenCode         | `--harness opencode`|
| Everything       | `--harness all`     |

The LLM-assisted install works best with Claude Code (this doc's primary
target). For other harnesses, the terminal-based `./bootstrap.sh` install
is recommended — see `docs/INSTALL.<harness>.md`.

## Security notes

- The SHA256 pin is the supply-chain defense. **Do NOT** remove the SHA
  verification step. An attacker who compromises the GitHub release CDN
  but not the published SHA cannot substitute a malicious archive.
- The prompt does not use `curl | bash`. It downloads, verifies, then
  executes — the three steps are inspectable separately.
- If the SHA check fails, Claude will stop with the failed `[ "$expected" =
  "$actual" ]` check and tell you. Do not proceed.

## Troubleshooting

- **"SHA mismatch" error** — the release was re-cut or the pin is stale.
  Open an issue with the observed SHA and the time of attempt.
- **`bootstrap.sh: command not found`** — the download didn't produce
  `dist/bootstrap.sh`. Check the archive structure with `ls <tempdir>/dist`.
- **Hook doesn't fire after restart** — verify `.claude/settings.json`
  contains the SessionStart hook entry. Run
  `python3 hooks/session_start.py --dry-run` to test the hook directly.
