"""Dataclasses normalizing per-harness transcripts to a common shape.

Adapters produce Transcript(messages=tuple(Message, ...)).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Usage:
    input_tokens: int
    output_tokens: int
    cache_creation: int
    cache_read: int
    model: str  # canonical ID, must exist in pricing.yaml

    @property
    def total_input(self) -> int:
        return self.input_tokens + self.cache_creation + self.cache_read

    @property
    def total_tokens(self) -> int:
        return self.total_input + self.output_tokens


@dataclass(frozen=True, slots=True)
class Message:
    role: str                  # assistant | user | system | tool_result
    agent_id: str | None       # None for main session; non-empty for subagents
    usage: Usage | None
    text_excerpt: str = ""     # ≤ 120 chars for description inference


@dataclass(frozen=True, slots=True)
class Transcript:
    source_path: Path
    harness: str                              # must match config/harnesses.yaml
    phase_hint: str | None                    # phase id ("01".."06") if adapter detected
    messages: tuple[Message, ...] = field(default_factory=tuple)


@dataclass(slots=True)
class Aggregate:
    """Rollup of usage by subagent + model + totals."""
    main: Usage | None = None
    subagents: dict[str, Usage] = field(default_factory=dict)  # agent_id → accumulated
    per_model: dict[str, Usage] = field(default_factory=dict)  # model → accumulated
    message_count: int = 0

    @property
    def total_usage(self) -> Usage:
        """Sum across main + all subagents."""
        ins = cache_r = cache_c = out = 0
        for u in [self.main, *self.subagents.values()]:
            if u is None:
                continue
            ins += u.input_tokens
            out += u.output_tokens
            cache_r += u.cache_read
            cache_c += u.cache_creation
        return Usage(
            input_tokens=ins,
            output_tokens=out,
            cache_read=cache_r,
            cache_creation=cache_c,
            model="<mixed>",
        )

    @property
    def cache_hit_rate(self) -> float:
        """Cache-read / (cache-read + cache-creation + input)."""
        t = self.total_usage
        denom = t.total_input
        return (t.cache_read / denom) if denom else 0.0
