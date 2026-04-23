#!/usr/bin/env python3
"""SessionStart hook — detects harness via env vars, emits correct JSON shape.

Multi-harness support with Python 3.11+ stdlib and SHA-pinned integrity check.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from _python_check import require_python_311  # noqa: E402

require_python_311()


HOOK_VERSION = 1
CONTRACT_REL_PATH = "skill/sdlc-contract.md"


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _read_version() -> str:
    version_file = _project_root() / "VERSION"
    try:
        return version_file.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return "unknown"


def _read_contract() -> tuple[str, str]:
    """Returns (body, sha256_hex)."""
    path = _project_root() / CONTRACT_REL_PATH
    body = path.read_text(encoding="utf-8")
    sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return body, sha


def _verify_integrity(actual_sha: str) -> None:
    """Check committed .sha256 file if present; fail loud on mismatch."""
    sha_file = _project_root() / (CONTRACT_REL_PATH + ".sha256")
    if not sha_file.exists():
        # No pinned SHA yet — soft-allow (bootstrap/initial install path)
        return
    expected = sha_file.read_text(encoding="utf-8").strip().split()[0]
    if expected != actual_sha:
        sys.stderr.write(
            f"INTEGRITY FAILURE: {CONTRACT_REL_PATH} sha256 mismatch.\n"
            f"  Expected: {expected}\n"
            f"  Actual:   {actual_sha}\n"
            f"Refusing to inject tampered contract. Investigate via "
            f"`git log -- {CONTRACT_REL_PATH}` before proceeding.\n"
        )
        sys.exit(1)


def _detect_harness() -> str:
    """Env-var priority order (first match wins)."""
    env = os.environ
    if env.get("CURSOR_PLUGIN_ROOT"):
        return "cursor"
    if env.get("COPILOT_CLI"):
        return "copilot-cli"
    if env.get("CLAUDE_PLUGIN_ROOT") or env.get("CLAUDE_PROJECT_DIR"):
        return "claude-code"
    if env.get("CODEX_PLUGIN_ROOT"):
        return "codex-cli"
    if env.get("GEMINI_EXTENSION_ROOT"):
        return "gemini-cli"
    if env.get("OPENCODE_PLUGIN_ROOT"):
        return "opencode"
    return "unknown"


def _build_context(contract_body: str, contract_sha: str, harness: str) -> str:
    version = _read_version()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sha_prefix = contract_sha[:12]
    banner = f"── SDLC contract v{version} loaded at {now} · harness={harness} ──"
    tail = f"── contract sha256: {sha_prefix} ──"
    return f"{banner}\n\n{contract_body}\n\n{tail}"


def _emit(harness: str, context: str) -> int:
    """Emit the JSON shape the detected harness expects."""
    payload = {
        "sdlc_hook_version": HOOK_VERSION,
    }
    if harness == "claude-code":
        payload.update(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": context,
                }
            }
        )
    elif harness == "cursor":
        payload["additional_context"] = context
    elif harness in ("copilot-cli", "codex-cli", "gemini-cli", "opencode", "unknown"):
        # SDK-standard / fallback
        payload["additionalContext"] = context
    else:
        sys.stderr.write(f"Unknown harness '{harness}' — emitting SDK-standard shape\n")
        payload["additionalContext"] = context

    sys.stdout.write(json.dumps(payload, ensure_ascii=False))
    sys.stdout.write("\n")
    return 0


def main(argv: list[str]) -> int:
    contract_body, contract_sha = _read_contract()

    mode = argv[1] if len(argv) > 1 else ""

    if mode == "--version":
        print(f"sdlc-session-start v{HOOK_VERSION}")
        return 0

    if mode == "--detect":
        harness = _detect_harness()
        print(f"detected={harness} hook_version={HOOK_VERSION} contract_sha={contract_sha[:12]}")
        return 0

    if mode == "--check-integrity":
        _verify_integrity(contract_sha)
        print(f"ok contract_sha={contract_sha[:12]}")
        return 0

    _verify_integrity(contract_sha)

    harness = _detect_harness()
    context = _build_context(contract_body, contract_sha, harness)

    if mode == "--dry-run":
        print(json.dumps({"sdlc_hook_version": HOOK_VERSION, "harness": harness, "context_length": len(context)}))
        return 0

    return _emit(harness, context)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
