"""Cursor transcript adapter — STUB. PR welcome. See docs/adapters.md."""
from __future__ import annotations

from pathlib import Path
from typing import Iterator

from ..errors import AdapterError
from ..normalizer import Message, Transcript
from .base import BaseAdapter


class CursorAdapter(BaseAdapter):
    name = "cursor"

    @classmethod
    def can_parse(cls, path: Path) -> bool:
        return False  # not yet implemented

    def parse(self, path: Path) -> Transcript:
        raise AdapterError(
            "Cursor adapter not implemented. "
            "Contribute: https://github.com/Electronics-Extreme/claude-sdlc/blob/main/docs/adapters.md"
        )

    def stream(self, path: Path) -> Iterator[Message]:
        raise AdapterError("Cursor adapter not implemented.")
