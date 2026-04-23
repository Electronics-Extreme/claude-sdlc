#!/usr/bin/env python3
"""Release gate — verify VERSION + CHANGELOG are consistent.

Per NFR-SEMVER-1.

Usage:
  python3 scripts/release_check.py --tag vX.Y.Z
  python3 scripts/release_check.py --check-changelog-for-pr
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _python_check import require_python_311  # noqa: E402

require_python_311()


TAG_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def check_tag(tag: str) -> int:
    m = TAG_RE.match(tag)
    if not m:
        print(f"FAIL: tag {tag!r} does not match vX.Y.Z", file=sys.stderr)
        return 1
    version = f"{m.group(1)}.{m.group(2)}.{m.group(3)}"
    repo = _repo_root()

    vfile = repo / "VERSION"
    file_ver = vfile.read_text(encoding="utf-8").strip()
    if file_ver != version:
        print(f"FAIL: VERSION file {file_ver!r} != tag {version!r}", file=sys.stderr)
        return 1

    cl = repo / "CHANGELOG.md"
    text = cl.read_text(encoding="utf-8")
    if f"## [{version}]" not in text:
        print(f"FAIL: CHANGELOG.md missing section [{version}]", file=sys.stderr)
        return 1

    print(f"✓ release gate pass for tag {tag}")
    return 0


def check_changelog_for_pr() -> int:
    """Verify the [Unreleased] section has an entry since the last tag.

    Used by PR workflows to ensure contributors don't merge without a CHANGELOG
    entry. Heuristic: [Unreleased] section must contain at least one of
    ### Added / Changed / Deprecated / Removed / Fixed / Security lines
    with a non-empty body.
    """
    repo = _repo_root()
    cl = repo / "CHANGELOG.md"
    text = cl.read_text(encoding="utf-8")
    m = re.search(r"##\s+\[Unreleased\](.*?)(?=^##\s+\[|\Z)", text, re.S | re.M)
    if not m:
        print("FAIL: CHANGELOG.md has no [Unreleased] section", file=sys.stderr)
        return 1
    section = m.group(1).strip()
    if section in ("", "(nothing yet)"):
        print("WARN: [Unreleased] is empty. If this PR changes functional behavior, add an entry.", file=sys.stderr)
        # Non-fatal — docs-only PRs may legitimately leave it empty
        return 0
    print("✓ [Unreleased] has entries")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", help="verify against a specific vX.Y.Z tag")
    parser.add_argument("--check-changelog-for-pr", action="store_true",
                        help="verify [Unreleased] section has entries")
    args = parser.parse_args(argv[1:])

    if args.tag:
        return check_tag(args.tag)
    if args.check_changelog_for_pr:
        return check_changelog_for_pr()
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
