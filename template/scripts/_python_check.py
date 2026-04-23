"""Python-version entry check — imported at the top of every script.

Fails loud on Python < 3.11 per NFR-PORT-STDLIB-1.
"""
from __future__ import annotations

import sys

MIN_VERSION: tuple[int, int] = (3, 11)


def require_python_311() -> None:
    if sys.version_info[:2] < MIN_VERSION:
        sys.stderr.write(
            f"Python {MIN_VERSION[0]}.{MIN_VERSION[1]}+ required; "
            f"found {sys.version_info.major}.{sys.version_info.minor}\n"
            f"Install:\n"
            f"  macOS:   brew install python@3.11\n"
            f"  Ubuntu:  sudo apt install python3.11\n"
            f"  Windows: winget install Python.Python.3.11\n"
            f"         or https://python.org/downloads\n"
        )
        sys.exit(2)


if __name__ == "__main__" or __name__ == "_python_check":
    require_python_311()
