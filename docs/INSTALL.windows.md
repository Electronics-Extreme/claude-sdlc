---
doc: docs/INSTALL.windows.md
status: signed
signed_by: Thanin Piromward on 2026-04-23
required_for: [phase-6-CR-implementation]
cite_as: INST
---

# Installing on Windows 11

Windows adopters need **only Python 3.11+** — no WSL2, no Git
Bash, no MinGW.

## Install Python 3.11+

```powershell
winget install Python.Python.3.11
```

Or download the installer from https://python.org/downloads.
**Check "Add Python to PATH"** during installation.

Verify:

```powershell
python --version      # expect Python 3.11.x or higher
```

If `python` resolves to an older version, use the Python Launcher:

```powershell
py -3.11 --version
```

## Install the kit

Download and extract `dist.zip` from the latest release, or clone the repo:

```powershell
git clone https://github.com/Electronics-Extreme/claude-sdlc.git C:\sdlc-kit
cd C:\sdlc-kit
```

## Bootstrap a new project

```powershell
.\bootstrap.bat C:\Projects\MyProject
```

Or with PowerShell:

```powershell
.\bootstrap.ps1 C:\Projects\MyProject
```

Or via Python directly (fallback):

```powershell
python scripts\bootstrap.py C:\Projects\MyProject
```

## Configure line endings (one-time)

The repository enforces LF line endings via `.gitattributes`. If your editor
defaults to CRLF, configure it to respect the repo setting:

**VS Code** — `.vscode/settings.json`:

```json
{
  "files.eol": "\n"
}
```

**Git global** (optional):

```powershell
git config --global core.autocrlf input
```

## Verify hook script runs

```powershell
python hooks\session_start.py --detect
python hooks\session_start.py --check-integrity
python hooks\session_start.py --dry-run
```

All three should exit 0 (or dry-run print JSON).

## Troubleshooting

- **"Python not found"** → re-install Python with "Add to PATH" checked, or
  restart your terminal so the PATH update takes effect.
- **SmartScreen / Windows Defender quarantine** → downloaded `dist.zip` may
  trigger SmartScreen. Right-click → Properties → Unblock. Consider verifying
  the `.sha256` files under `skill/` and `hooks/` against the release signature.
- **CRLF-rejected commits** → enforce LF in your editor or run
  `dos2unix <file>` before committing.
- **"Long path" errors** on Windows with deep repo structures → enable
  `LongPathsEnabled`:
  ```powershell
  reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v LongPathsEnabled /t REG_DWORD /d 1 /f
  ```

## What works vs. what doesn't

✅ Works on Windows 11 + Python 3.11+:
- All bootstrap, build-archive, residue guard, frontmatter check scripts
- Hook script (all modes: --detect, --dry-run, --check-integrity, --version)
- Metrics CLI (analyze, budget-check, trend, adapters)
- All CI workflows (sdlc-tests runs on windows-2022 runner)

⚠️ Not tested on Windows:
- Symlink-based Codex install — use junctions instead (`mklink /J`) as per
  `.codex/INSTALL.md`.

❌ Not supported on Windows:
- (none known)
