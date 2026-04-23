#!/usr/bin/env python3
"""SHA-pinning for hook-critical files.

Writes `.sha256` companion files for:
  - skill/sdlc-contract.md
  - hooks/session_start.py

Modes:
  --write   recompute and overwrite both .sha256 files
  --check   verify both .sha256 match computed values; exit 1 on mismatch
"""
from __future__ import annotations

import hashlib
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


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    mode = argv[1] if len(argv) > 1 else "--check"

    failures = 0
    for rel in PINNED:
        path = repo_root / rel
        if not path.exists():
            sys.stderr.write(f"ERROR: {rel} missing\n")
            failures += 1
            continue
        actual = sha256_of(path)
        sha_path = repo_root / (rel.as_posix() + ".sha256")

        if mode == "--write":
            sha_path.write_text(f"{actual}  {rel.name}\n", encoding="utf-8")
            print(f"wrote {sha_path.relative_to(repo_root)}: {actual[:12]}…")
            continue

        # --check mode
        if not sha_path.exists():
            sys.stderr.write(f"MISSING: {sha_path.relative_to(repo_root)} not committed\n")
            failures += 1
            continue
        committed = sha_path.read_text(encoding="utf-8").strip().split()[0]
        if committed != actual:
            sys.stderr.write(
                f"MISMATCH: {rel}\n"
                f"  committed: {committed}\n"
                f"  actual:    {actual}\n"
                f"  Run: python3 scripts/update_contract_sha.py --write\n"
            )
            failures += 1
        else:
            print(f"ok {rel}: {actual[:12]}…")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
