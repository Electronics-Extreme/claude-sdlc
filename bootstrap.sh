#!/usr/bin/env sh
# Unix launcher — delegates to scripts/bootstrap.py.
# Python 3.11+ is the only prerequisite.
set -eu
exec python3 "$(dirname "$0")/scripts/bootstrap.py" "$@"
