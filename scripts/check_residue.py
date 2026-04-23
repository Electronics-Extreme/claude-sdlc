#!/usr/bin/env python3
"""Placeholder residue guard — fails if signed docs contain TODO/FIXME/{{…}}/etc.

Per NFR-DOC-HYGIENE-1.

Exit codes:
  0  clean
  1  residue found
  2  config error
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _python_check import require_python_311  # noqa: E402

require_python_311()


PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("{{...}}",        re.compile(r"\{\{[^}]*\}\}")),
    ("TODO",           re.compile(r"\bTODO\b:?")),
    ("FIXME",          re.compile(r"\bFIXME\b:?")),
    ("XXX",            re.compile(r"\bXXX\b:?")),
    ("<TBD>",          re.compile(r"[<\[(]TBD[>\])]")),
    ("[to-be-filled]", re.compile(r"\[(?:to-be-filled|replace me|PLACEHOLDER)\]", re.IGNORECASE)),
    ("bare-ellipsis",  re.compile(r"^\s*\.\.\.\s*$")),
]

SCAN_ROOTS = ["docs", "skill", "config", "schemas"]  # "docs" covers docs/sdlc/0X_* phase docs

SIGNED_STATUSES = {"signed", "amended"}


def _load_exceptions(repo_root: Path) -> set[tuple[str, str]]:
    """Load (file, token) exception tuples from config/residue-exceptions.yaml.

    Minimal YAML parse — no PyYAML dep. Accepts the subset we author.
    """
    exc_file = repo_root / "config" / "residue-exceptions.yaml"
    if not exc_file.exists():
        return set()
    out: set[tuple[str, str]] = set()
    current: dict[str, str] = {}
    for raw in exc_file.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if stripped.startswith("- file:"):
            if current.get("file") and current.get("token"):
                out.add((current["file"], current["token"]))
            current = {"file": stripped.split(":", 1)[1].strip()}
        elif stripped.startswith("file:") and indent > 0:
            current["file"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("token:"):
            current["token"] = stripped.split(":", 1)[1].strip().strip('"').strip("'")
    if current.get("file") and current.get("token"):
        out.add((current["file"], current["token"]))
    return out


def _parse_frontmatter_status(path: Path) -> str | None:
    """Return `status` field from YAML frontmatter, or None if none/parse-error."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    block = text[4:end]
    for raw in block.splitlines():
        line = raw.strip()
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return None


def scan(repo_root: Path) -> list[tuple[Path, int, int, str, str]]:
    exceptions = _load_exceptions(repo_root)
    hits: list[tuple[Path, int, int, str, str]] = []
    for root_name in SCAN_ROOTS:
        root = repo_root / root_name
        if not root.exists():
            continue
        for path in root.rglob("*.md"):
            # Only scan signed/amended docs (per CR-009 §5 expanded pattern rules)
            status = _parse_frontmatter_status(path)
            if status not in SIGNED_STATUSES:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                for token, pattern in PATTERNS:
                    for match in pattern.finditer(line):
                        rel = path.relative_to(repo_root).as_posix()
                        if (rel, token) in exceptions:
                            continue
                        hits.append((path, lineno, match.start() + 1, token, line.rstrip()))
    return hits


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    hits = scan(repo_root)
    if not hits:
        print(f"OK: no placeholder residue in signed docs under {repo_root}")
        return 0
    for path, lineno, col, token, line in hits:
        rel = path.relative_to(repo_root).as_posix()
        print(f"{rel}:{lineno}:{col}: residue type={token} — {line.strip()[:100]}")
    sys.stderr.write(f"\n{len(hits)} residue hit(s) in signed docs. Either fix the doc, or add an allowlist entry to config/residue-exceptions.yaml with a justification.\n")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
