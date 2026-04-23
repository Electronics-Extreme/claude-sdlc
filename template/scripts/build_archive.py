#!/usr/bin/env python3
"""Python 3.11+ stdlib archive builder.

Produces dist/ + dist.zip from the current source tree.

Usage:
  python3 scripts/build_archive.py           # uses ./VERSION
  python3 scripts/build_archive.py 1.2.3     # override version
"""
from __future__ import annotations

import shutil
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _python_check import require_python_311  # noqa: E402

require_python_311()


# Files/dirs at repo root to include in dist/.
DIST_INCLUDES = [
    "docs/sdlc/01_requirement", "docs/sdlc/02_design", "docs/sdlc/03_implementation",
    "docs/sdlc/04_testing", "docs/sdlc/05_deployment", "docs/sdlc/06_maintenance",
    "skill", "hooks", "scripts", "config", "docs", "schemas", "template",
    ".gitattributes", "VERSION", "CLAUDE.template.md", "README.md",
    "PRIVACY.md", "NOTICE.md", "CHANGELOG.md", "LICENSE",
    "bootstrap.sh", "bootstrap.bat", "bootstrap.ps1",
    "build-archive.sh",
]

# Exclusions under included dirs.
EXCLUDES = {".DS_Store", "__pycache__", "*.pyc", ".metrics", ".git"}


def _version(repo_root: Path, override: str | None) -> str:
    if override:
        return override
    vfile = repo_root / "VERSION"
    if vfile.exists():
        return vfile.read_text(encoding="utf-8").strip()
    return "0.0.0"


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    version = _version(repo_root, argv[1] if len(argv) > 1 else None)

    dist = repo_root / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir()

    copied = 0
    for name in DIST_INCLUDES:
        src = repo_root / name
        if not src.exists():
            continue
        dst = dist / name
        if src.is_dir():
            def _ignore(_src: str, names: list[str]) -> list[str]:
                out: list[str] = []
                for n in names:
                    if n in EXCLUDES or n.endswith(".pyc"):
                        out.append(n)
                return out
            shutil.copytree(src, dst, ignore=_ignore)
        else:
            shutil.copy2(src, dst)
        copied += 1

    # Write version into dist
    (dist / "VERSION").write_text(f"{version}\n", encoding="utf-8")

    # Zip it up
    zip_path = repo_root / "dist.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in dist.rglob("*"):
            if any(part in EXCLUDES for part in path.parts):
                continue
            arcname = "dist/" + path.relative_to(dist).as_posix()
            zf.write(path, arcname)

    print(f"✓ built dist/ v{version} ({copied} top-level items)")
    print(f"✓ built dist.zip")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
