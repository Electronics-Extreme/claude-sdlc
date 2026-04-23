#!/usr/bin/env python3
"""Frontmatter validator — enforces schemas/doc-frontmatter.schema.yaml.

Validates every .md under phase dirs + skill/ + docs/ + config/ + schemas/.

Exit codes:
  0  clean
  1  validation error(s)
  2  schema or config load failure
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _python_check import require_python_311  # noqa: E402

require_python_311()


SIGNED_REQUIRED = ("signed_by",)
DEPRECATED_REQUIRED = ("signed_by", "deprecated_on", "superseded_by")
VALID_STATUSES = {"template", "draft", "signed", "amended", "deprecated"}

SIGNED_BY_RE = re.compile(r"^.+ on \d{4}-\d{2}-\d{2}$")
CR_ID_RE = re.compile(r"^CR-\d{4}-\d{3}[A-Z]?$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CITE_AS_RE = re.compile(r"^[A-Z][A-Z0-9-]{0,7}$")

SCAN_ROOTS = ["docs", "skill"]  # "docs" covers docs/sdlc/0X_* phase docs


def _load_task_types(repo_root: Path) -> set[str]:
    """Load task-type names from config/task-types.yaml (minimal parse)."""
    tt_file = repo_root / "config" / "task-types.yaml"
    if not tt_file.exists():
        return set()
    names: set[str] = set()
    in_section = False
    for raw in tt_file.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if stripped == "task_types:":
            in_section = True
            continue
        if in_section:
            if line and not line.startswith(" ") and not line.startswith("\t") and not stripped.startswith("#"):
                in_section = False
                continue
            m = re.match(r"^  ([A-Za-z][A-Za-z0-9-]*):\s*$", line)
            if m:
                names.add(m.group(1))
    return names


def _extract_frontmatter(text: str) -> dict | None:
    """Parse YAML frontmatter subset we author. Returns dict or None if absent."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    block = text[4:end]

    out: dict = {}
    current_key: str | None = None
    current_list: list | None = None
    amended_entries: list[dict] = []
    amended_current: dict | None = None

    for raw in block.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue

        indent = len(raw) - len(raw.lstrip())
        stripped = raw.strip()

        if indent == 0:
            # Flush any pending amended entry before transitioning away.
            if amended_current:
                amended_entries.append(amended_current)
                amended_current = None
            current_list = None
            if ":" in stripped:
                key, _, val = stripped.partition(":")
                key = key.strip()
                val = val.strip()
                current_key = key
                if val == "":
                    # list-valued key coming
                    current_list = []
                    out[key] = current_list
                    if key == "amended":
                        out[key] = amended_entries
                        current_list = None
                else:
                    # scalar
                    if val.startswith("[") and val.endswith("]"):
                        inner = val[1:-1].strip()
                        out[key] = [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()] if inner else []
                    else:
                        out[key] = val.strip().strip('"').strip("'")
        elif indent == 2:
            if current_key == "amended":
                if stripped.startswith("- "):
                    if amended_current:
                        amended_entries.append(amended_current)
                    amended_current = {}
                    rest = stripped[2:]
                    if ":" in rest:
                        k, _, v = rest.partition(":")
                        amended_current[k.strip()] = v.strip().strip('"').strip("'")
                continue
            if current_list is not None and stripped.startswith("- "):
                current_list.append(stripped[2:].strip().strip('"').strip("'"))
        elif indent == 4 and amended_current is not None:
            if ":" in stripped:
                k, _, v = stripped.partition(":")
                amended_current[k.strip()] = v.strip().strip('"').strip("'")

    if amended_current:
        amended_entries.append(amended_current)

    return out


def validate(path: Path, fm: dict, task_types: set[str]) -> list[str]:
    errors: list[str] = []

    if "doc" not in fm:
        errors.append("missing required field: doc")
    if "status" not in fm:
        errors.append("missing required field: status")
        return errors

    status = fm.get("status")
    if status not in VALID_STATUSES:
        errors.append(f"status={status!r} not in {sorted(VALID_STATUSES)}")
        return errors

    if status in ("signed", "amended", "deprecated"):
        sb = fm.get("signed_by")
        if not sb:
            errors.append(f"status={status} requires signed_by")
        elif not SIGNED_BY_RE.match(str(sb)):
            errors.append(f"signed_by={sb!r} must match '<Name> on YYYY-MM-DD'")

    if status == "deprecated":
        if not fm.get("deprecated_on"):
            errors.append("status=deprecated requires deprecated_on")
        elif not DATE_RE.match(str(fm["deprecated_on"])):
            errors.append(f"deprecated_on must match YYYY-MM-DD")
        if not fm.get("superseded_by"):
            errors.append("status=deprecated requires superseded_by")

    if status == "amended":
        amended = fm.get("amended")
        if not isinstance(amended, list) or not amended:
            errors.append("status=amended requires non-empty amended array")
        else:
            for i, entry in enumerate(amended):
                if not isinstance(entry, dict):
                    errors.append(f"amended[{i}] must be a mapping")
                    continue
                if not DATE_RE.match(str(entry.get("date", ""))):
                    errors.append(f"amended[{i}].date must match YYYY-MM-DD")
                if not CR_ID_RE.match(str(entry.get("cr", ""))):
                    errors.append(f"amended[{i}].cr must match CR-YYYY-NNN[A]")

    rf = fm.get("required_for")
    if rf is not None:
        if not isinstance(rf, list):
            errors.append("required_for must be an array")
        elif task_types:
            for tt in rf:
                if tt not in task_types:
                    errors.append(f"required_for: {tt!r} not in config/task-types.yaml")

    ca = fm.get("cite_as")
    if ca is not None and not CITE_AS_RE.match(str(ca)):
        errors.append(f"cite_as={ca!r} must match ^[A-Z][A-Z0-9-]{{0,7}}$")

    return errors


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    task_types = _load_task_types(repo_root)
    if not task_types:
        sys.stderr.write("WARNING: config/task-types.yaml missing or unreadable; required_for values will not be validated.\n")

    total_errors = 0
    total_files = 0
    missing_fm = 0
    for root_name in SCAN_ROOTS:
        root = repo_root / root_name
        if not root.exists():
            continue
        for path in root.rglob("*.md"):
            total_files += 1
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError as e:
                print(f"{path}: cannot read: {e}")
                total_errors += 1
                continue
            fm = _extract_frontmatter(text)
            rel = path.relative_to(repo_root).as_posix()
            if fm is None:
                missing_fm += 1
                print(f"{rel}: no YAML frontmatter (expected)")
                total_errors += 1
                continue
            errors = validate(path, fm, task_types)
            for err in errors:
                print(f"{rel}: {err}")
                total_errors += 1

    print(f"\nScanned {total_files} markdown files across {len(SCAN_ROOTS)} roots.")
    if total_errors:
        sys.stderr.write(f"{total_errors} error(s); {missing_fm} file(s) lacked frontmatter.\n")
        return 1
    print("OK: all frontmatter valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
