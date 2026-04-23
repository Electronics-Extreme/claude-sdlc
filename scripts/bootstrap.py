#!/usr/bin/env python3
"""Pure Python 3.11+ stdlib bootstrap.

Copies template/ into target directory. Supports --harness selection.

Usage:
  python3 scripts/bootstrap.py <target-dir> [--harness <name>]

--harness values: claude | cursor | codex | gemini | copilot | opencode | all (default)
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _python_check import require_python_311  # noqa: E402

require_python_311()


HARNESS_CHOICES = ["claude", "cursor", "codex", "gemini", "copilot", "opencode", "all"]


# Per-harness Layer-1 + Layer-2 file inventory (under template/).
HARNESS_FILES: dict[str, list[str]] = {
    "claude":   [".claude/settings.json", ".claude/sdlc-contract.md",
                 ".claude-plugin/plugin.json",
                 "CLAUDE.template.md"],
    "cursor":   [".cursor-plugin/plugin.json",
                 ".cursor-plugin/hooks/hooks-cursor.json",
                 ".cursor-plugin/rules/sdlc-contract.mdc",
                 "AGENTS.md"],
    "codex":    ["AGENTS.md"],
    "gemini":   ["gemini-extension.json", "GEMINI.md"],
    "copilot":  [".claude-plugin/plugin.json", "AGENTS.md"],
    "opencode": [".opencode/plugins/sdlc-contract-loader.js", "AGENTS.md"],
}

# Always-copy (no harness-scoping): phase tree + skill + hooks + scripts + config + docs + schemas.
ALWAYS_COPY_DIRS = [
    "docs/sdlc",
    "skill", "hooks", "scripts", "config", "schemas", "tools",
    ".github",
]
ALWAYS_COPY_FILES = [".gitattributes", "README.md"]

# Files under `template/` that are installer scaffolds we never ship into
# bootstrapped projects. `docs/` is kit-maintainer documentation — adopters
# don't need INSTALL guides, VERSIONING policy, or migration guides in their
# own project tree.
SKIP_DIRS_UNDER_TEMPLATE = {"docs"}


def confirm_overlay(target: Path) -> bool:
    if not target.exists():
        return True
    if not target.is_dir():
        sys.stderr.write(f"error: {target} exists and is not a directory\n")
        return False
    if not any(target.iterdir()):
        return True
    reply = input(f"Target {target} is not empty. Overlay anyway? [y/N] ").strip().lower()
    return reply in ("y", "yes")


def copy_tree(src: Path, dst: Path) -> None:
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)
    elif src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a new Waterfall SDLC project from this template.")
    parser.add_argument("target", help="Target directory")
    parser.add_argument("--harness", choices=HARNESS_CHOICES, default="all",
                        help="Which harness wrapper(s) to install. Default: all")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    template = repo_root / "template"
    if not template.is_dir():
        sys.stderr.write(f"error: template dir not found at {template}\n")
        return 1

    target = Path(args.target).resolve()
    if not confirm_overlay(target):
        return 1

    target.mkdir(parents=True, exist_ok=True)

    # Copy always-copy dirs + files.
    for d in ALWAYS_COPY_DIRS:
        src = template / d
        if src.exists():
            copy_tree(src, target / d)
    for f in ALWAYS_COPY_FILES:
        src = template / f
        if src.exists():
            copy_tree(src, target / f)

    # Harness-specific files.
    harnesses = HARNESS_CHOICES[:-1] if args.harness == "all" else [args.harness]
    for h in harnesses:
        for rel in HARNESS_FILES.get(h, []):
            src = template / rel
            if src.exists():
                copy_tree(src, target / rel)

    # Claude Code skill-discoverability: replicate skill/ into
    # .claude/skills/sdlc-strict-waterfall/ so `/sdlc-strict-waterfall` is
    # invocable as a project-scoped skill (per Anthropic's .claude/skills/ layout).
    if args.harness in ("claude", "all"):
        skill_src = target / "skill"
        skill_discovery_dst = target / ".claude" / "skills" / "sdlc-strict-waterfall"
        if skill_src.is_dir() and not skill_discovery_dst.exists():
            shutil.copytree(skill_src, skill_discovery_dst)

    # Pin SHA256 for hook-critical files — the kit's template SHAs are stale
    # the moment bootstrap copies content, so we pin to whatever the adopter
    # just received. The adopter re-pins if they later amend the contract.
    for rel in ("skill/sdlc-contract.md", "hooks/session_start.py"):
        src = target / rel
        if src.is_file():
            sha = hashlib.sha256(src.read_bytes()).hexdigest()
            (src.parent / (src.name + ".sha256")).write_text(
                f"{sha}  {src.name}\n", encoding="utf-8"
            )

    # Promote CLAUDE.template.md → CLAUDE.md if appropriate.
    tpl = target / "CLAUDE.template.md"
    live = target / "CLAUDE.md"
    if tpl.exists() and not live.exists():
        tpl.rename(live)
    elif tpl.exists() and live.exists():
        print(f"note: {live} already exists; left CLAUDE.template.md untouched.", file=sys.stderr)

    # Sanity checks per harness.
    warnings: list[str] = []
    if args.harness in ("claude", "all") and not (target / ".claude" / "settings.json").exists():
        warnings.append(".claude/ hook missing")
    if args.harness in ("all", "codex", "copilot", "opencode") and not (target / "AGENTS.md").exists():
        warnings.append("AGENTS.md missing (needed for Codex/Copilot/OpenCode/generic readers)")
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)

    print(f"\n✓ SDLC project initialized at {target}")
    print(f"  Harness selection: {args.harness}")
    print(f"\nNext steps:")
    print(f"  1. cd {target}")
    print(f"  2. Edit CLAUDE.md — fill {{{{PLACEHOLDER}}}} values")
    print(f"  3. Open docs/sdlc/01_requirement/srs.md and start the spec")

    if args.harness in ("claude", "all"):
        print(f"  4. Start Claude Code in {target} — SessionStart hook auto-loads contract")
    if args.harness in ("cursor", "all"):
        print(f"  4. Open {target} in Cursor — plugin auto-registers on first agent session")
    if args.harness in ("gemini", "all"):
        print(f"  4. Run: (cd {target} && gemini extensions install .)")
    if args.harness in ("codex", "all"):
        print(f"  4. Follow .codex/INSTALL.md for Codex CLI skill-discovery install")
    if args.harness in ("opencode", "all"):
        print(f"  4. Add plugin to your opencode.json — see .opencode/INSTALL.md")
    if args.harness in ("copilot", "all"):
        print(f"  4. Run: (cd {target} && copilot plugin install .)")

    print(f"  5. First message to the agent:")
    print(f"       /sdlc-strict-waterfall")
    print(f"       Start.")
    print(f"     (Greenfield → Bootstrap mode Gate 1. Existing docs → Strict mode.)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
