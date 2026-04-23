#!/usr/bin/env python3
"""Verify config/task-types.yaml matches schemas/task-types.schema.yaml shape.

Per Core rule 8.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _python_check import require_python_311  # noqa: E402

require_python_311()


TASK_TYPE_KEY = re.compile(r"^  ([A-Za-z][A-Za-z0-9-]*):\s*$")
PHASE_VAL = re.compile(r'^    phase:\s*["\']?(0[1-6])["\']?\s*$')
PURPOSE_KEY = re.compile(r"^    purpose:\s*")


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    path = repo_root / "config" / "task-types.yaml"
    if not path.exists():
        sys.stderr.write(f"FAIL: {path} not found\n")
        return 2

    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    types_seen: dict[str, dict[str, bool]] = {}
    current: str | None = None
    in_types = False

    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.rstrip()
        if line.strip() == "task_types:":
            in_types = True
            continue
        if not in_types:
            continue
        if line and not line.startswith(" ") and not line.startswith("\t"):
            in_types = False
            continue
        m = TASK_TYPE_KEY.match(line)
        if m:
            current = m.group(1)
            types_seen[current] = {"purpose": False, "phase": False}
            if not re.match(r"^phase-[1-6]-[A-Za-z0-9-]+$", current):
                errors.append(f"{path.name}:{lineno}: {current!r} does not match phase-<N>-<name> pattern")
            continue
        if current is None:
            continue
        if PURPOSE_KEY.match(line):
            types_seen[current]["purpose"] = True
        elif PHASE_VAL.match(line):
            types_seen[current]["phase"] = True

    if not types_seen:
        errors.append("task_types is empty")

    for name, fields in types_seen.items():
        if not fields["purpose"]:
            errors.append(f"{name}: missing required field 'purpose'")
        if not fields["phase"]:
            errors.append(f"{name}: missing required field 'phase'")

    if errors:
        for e in errors:
            print(e)
        return 1

    print(f"OK: {len(types_seen)} task-types in {path.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
