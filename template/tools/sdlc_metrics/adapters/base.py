"""Abstract base class for transcript adapters. Per NFR-METRICS-ADAPT-1."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator

from ..normalizer import Message, Transcript


class BaseAdapter(ABC):
    """Subclass per harness. Target: ≤ 200 LOC per well-formed transcript format."""

    name: str = ""  # must match config/harnesses.yaml key

    @classmethod
    @abstractmethod
    def can_parse(cls, path: Path) -> bool:
        """Quickly probe whether this adapter handles the given transcript."""

    @abstractmethod
    def parse(self, path: Path) -> Transcript:
        """Load and normalize the entire transcript."""

    @abstractmethod
    def stream(self, path: Path) -> Iterator[Message]:
        """Yield one Message at a time (for large-file memory safety)."""
