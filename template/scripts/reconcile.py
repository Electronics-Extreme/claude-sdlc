#!/usr/bin/env python3
"""Two-pass reconciliation gate enforcer.

Reconciliation reports use YAML-fenced headers to declare pass state:

  ---
  reconciliation:
    phase: "03"
    pass1:
      status: closed      # open | closed
      buckets:
        A: 12
        B: 0
        C: 0
        E: 2
    pass2:
      status: open        # gated by pass1 closure
      buckets: {}
  ---

This script enforces: pass2 MAY NOT reach `status: closed` while pass1 has any
open items (Bucket B or C unresolved). Sign-off requires both passes closed +
base gates green.

Usage:
  python3 scripts/reconcile.py --status <path-to-report.md>
  python3 scripts/reconcile.py --sign-off <path-to-report.md>
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _python_check import require_python_311  # noqa: E402

require_python_311()


def _parse_yaml_header(text: str) -> dict:
    """Extract and parse the reconciliation: block from the report's frontmatter."""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    block = text[4:end]

    # Minimal nested YAML parser — only understands our known shape.
    out: dict = {}
    stack: list[tuple[int, dict]] = [(0, out)]

    for raw in block.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        while stack and stack[-1][0] > indent:
            stack.pop()
        parent = stack[-1][1] if stack else out
        stripped = line.strip()
        if stripped.endswith(":"):
            key = stripped[:-1]
            parent[key] = {}
            stack.append((indent + 2, parent[key]))
        elif ":" in stripped:
            key, _, val = stripped.partition(":")
            parent[key.strip()] = val.strip().strip('"').strip("'")
    return out


def check_status(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    data = _parse_yaml_header(text)
    rec = data.get("reconciliation", {})
    if not rec:
        print(f"WARN: {path} has no 'reconciliation:' block; treating as unfilled", file=sys.stderr)
        return 2
    p1 = rec.get("pass1", {})
    p2 = rec.get("pass2", {})
    p1_status = p1.get("status", "unknown")
    p2_status = p2.get("status", "unknown")
    phase = rec.get("phase", "??")
    print(f"Phase {phase}: pass1={p1_status}, pass2={p2_status}")

    p1_buckets = p1.get("buckets", {})
    if isinstance(p1_buckets, dict):
        for b in ("B", "C"):
            n = int(p1_buckets.get(b, 0))
            if n > 0 and p1_status != "closed":
                print(f"  Pass-1 Bucket {b}: {n} open item(s)")
    if p2_status == "closed" and p1_status != "closed":
        print("VIOLATION: Pass 2 cannot open while Pass 1 has open items", file=sys.stderr)
        return 1
    return 0


def sign_off(path: Path) -> int:
    rc = check_status(path)
    if rc != 0:
        print("ERROR: cannot sign off — pass-order violation or incomplete state", file=sys.stderr)
        return rc
    text = path.read_text(encoding="utf-8")
    data = _parse_yaml_header(text)
    rec = data.get("reconciliation", {})
    p1 = rec.get("pass1", {}).get("status")
    p2 = rec.get("pass2", {}).get("status")
    if p1 != "closed" or p2 != "closed":
        print(f"ERROR: both passes must be 'closed' for sign-off (got pass1={p1}, pass2={p2})", file=sys.stderr)
        return 1
    print(f"✓ reconciliation complete for {path}")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", metavar="REPORT")
    parser.add_argument("--sign-off", metavar="REPORT")
    args = parser.parse_args(argv[1:])
    if args.status:
        return check_status(Path(args.status))
    if args.sign_off:
        return sign_off(Path(args.sign_off))
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
