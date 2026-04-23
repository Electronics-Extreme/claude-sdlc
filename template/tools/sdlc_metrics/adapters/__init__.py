"""Per-harness transcript adapters."""
from __future__ import annotations

from .base import BaseAdapter
from .claude_code import ClaudeCodeAdapter

__all__ = ["BaseAdapter", "ClaudeCodeAdapter", "all_adapters", "find_adapter"]


def all_adapters() -> list[type[BaseAdapter]]:
    """Return list of registered adapters. Add new harnesses here after subclassing BaseAdapter."""
    from . import cursor, codex, gemini, copilot, opencode  # noqa: F401
    return [
        ClaudeCodeAdapter,
        cursor.CursorAdapter,
        codex.CodexAdapter,
        gemini.GeminiAdapter,
        copilot.CopilotAdapter,
        opencode.OpenCodeAdapter,
    ]


def find_adapter(path):
    """Resolve the correct adapter for a given transcript file."""
    for cls in all_adapters():
        if cls.can_parse(path):
            return cls()
    return None
