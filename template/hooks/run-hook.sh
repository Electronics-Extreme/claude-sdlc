#!/usr/bin/env sh
# Unix launcher for hooks/session_start.py — invokes Python 3.11+ directly.
exec python3 "$(dirname "$0")/session_start.py" "$@"
