#!/usr/bin/env python3
"""Claude plugin SessionStart hook — bootstrap guard.

Checks whether $CLAUDE_PROJECT_DIR/docs/sdlc exists.  If not, prompts the
user to copy the SDLC template into the project and regenerates SHA256 pins.

Usage (from hooks.json):
  python3 "${CLAUDE_PLUGIN_ROOT}/scripts/bootstrap_guard.py"
"""
from __future__ import annotations

import hashlib
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _python_check import require_python_311  # noqa: E402

require_python_311()


PINNED = [
    Path("skill/sdlc-contract.md"),
    Path("hooks/session_start.py"),
]


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def regenerate_pins(project_dir: Path) -> None:
    for rel in PINNED:
        src = project_dir / rel
        if src.is_file():
            sha = sha256_of(src)
            (src.parent / (src.name + ".sha256")).write_text(
                f"{sha}  {src.name}\n", encoding="utf-8"
            )
            print(f"  pinned {rel}: {sha[:12]}…")


def copy_template(template_dir: Path, project_dir: Path) -> None:
    """Copy template tree into project_dir, skipping installer scaffolds."""
    skip_dirs = {"docs"}  # kit-maintainer docs — adopters don't need these

    for item in template_dir.iterdir():
        if item.name in skip_dirs:
            continue
        dst = project_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dst, dirs_exist_ok=True)
        elif item.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dst)


def main() -> int:
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
    sdlc_dir = project_dir / "docs" / "sdlc"

    if sdlc_dir.is_dir():
        return 0

    plugin_root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT", ".")).resolve()
    template_dir = plugin_root / "template"

    print("SDLC template not found in this project.")
    print(f"  Missing: {sdlc_dir}")
    if template_dir.is_dir():
        print(f"  Template source: {template_dir}")
    else:
        print(f"  warning: template dir not found at {template_dir}", file=sys.stderr)

    reply = input("Bootstrap SDLC now? [y/N] ").strip().lower()
    if reply not in ("y", "yes"):
        print("Skipped.  Run this script again when ready.")
        return 0

    if not template_dir.is_dir():
        sys.stderr.write(f"error: template dir not found at {template_dir}\n")
        return 1

    print(f"\nCopying template → {project_dir} …")
    copy_template(template_dir, project_dir)

    print("\nRegenerating SHA256 pins …")
    regenerate_pins(project_dir)

    print(f"\n✓ SDLC bootstrapped at {project_dir}")
    print("  Next: edit CLAUDE.md and start /sdlc-strict-waterfall")
    return 0


if __name__ == "__main__":
    sys.exit(main())
