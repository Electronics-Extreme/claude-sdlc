"""OpenCode transcript adapter — STUB. PR welcome."""
from __future__ import annotations

from pathlib import Path
from typing import Iterator

from ..errors import AdapterError
from ..normalizer import Message, Transcript
from .base import BaseAdapter


class OpenCodeAdapter(BaseAdapter):
    name = "opencode"

    @classmethod
    def can_parse(cls, path: Path) -> bool:
        return False

    def parse(self, path: Path) -> Transcript:
        raise AdapterError("OpenCode adapter not implemented. PR welcome; see docs/adapters.md.")

    def stream(self, path: Path) -> Iterator[Message]:
        raise AdapterError("OpenCode adapter not implemented.")
