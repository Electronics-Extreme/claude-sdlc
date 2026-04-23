#!/usr/bin/env python3
"""Version bump + CHANGELOG promotion.

Usage:
  python3 scripts/bump_version.py <major|minor|patch>
"""
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _python_check import require_python_311  # noqa: E402

require_python_311()


SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def bump(current: str, level: str) -> str:
    m = SEMVER.match(current.strip())
    if not m:
        raise ValueError(f"VERSION does not match semver: {current!r}")
    major, minor, patch = (int(x) for x in m.groups())
    if level == "major":
        return f"{major + 1}.0.0"
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    if level == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"unknown level: {level!r} (expected major/minor/patch)")


def promote_changelog(repo_root: Path, new_version: str) -> None:
    cl = repo_root / "CHANGELOG.md"
    if not cl.exists():
        sys.stderr.write("note: CHANGELOG.md not found; skipping promotion\n")
        return
    today = date.today().isoformat()
    text = cl.read_text(encoding="utf-8")
    if "## [Unreleased]" not in text:
        sys.stderr.write("warning: CHANGELOG.md has no [Unreleased] section\n")
        return
    text = text.replace(
        "## [Unreleased]",
        f"## [Unreleased]\n\n(nothing yet)\n\n## [{new_version}] - {today}",
        1,
    )
    cl.write_text(text, encoding="utf-8")
    print(f"promoted CHANGELOG [Unreleased] → [{new_version}] - {today}")


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] not in ("major", "minor", "patch"):
        print("usage: bump_version.py <major|minor|patch>", file=sys.stderr)
        return 2
    level = argv[1]
    repo_root = Path(__file__).resolve().parent.parent
    vfile = repo_root / "VERSION"
    current = vfile.read_text(encoding="utf-8").strip()
    new = bump(current, level)
    vfile.write_text(new + "\n", encoding="utf-8")
    print(f"VERSION bumped: {current} → {new}")
    promote_changelog(repo_root, new)
    print(f"\nNext: commit, tag v{new}, push --tags")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
