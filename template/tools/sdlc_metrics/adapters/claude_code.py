"""Claude Code .jsonl transcript adapter. Reference implementation."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Iterator

from ..errors import AdapterError, SecretsDetectedError
from ..normalizer import Message, Transcript, Usage
from .base import BaseAdapter


# Secrets pre-filter per NFR-METRICS-SEC-1 / AC-M-012
_SECRET_PATTERNS = [
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),          # AWS Access Key
    re.compile(r"\bASIA[0-9A-Z]{16}\b"),          # AWS temporary key
    re.compile(r"\bghp_[A-Za-z0-9]{36,}\b"),      # GitHub personal access token
    re.compile(r"\bgho_[A-Za-z0-9]{36,}\b"),      # GitHub OAuth token
    re.compile(r"\bghs_[A-Za-z0-9]{36,}\b"),      # GitHub server-to-server token
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{82,}\b"),  # Fine-grained PAT
    re.compile(r"\bsk-ant-[A-Za-z0-9_-]{90,}\b"),  # Anthropic API key
    re.compile(r"\bsk-[A-Za-z0-9]{48,}\b"),       # OpenAI-style
    re.compile(r"-----BEGIN (RSA |EC |DSA |OPENSSH |)?PRIVATE KEY-----"),
]


class ClaudeCodeAdapter(BaseAdapter):
    name = "claude-code"

    @classmethod
    def can_parse(cls, path: Path) -> bool:
        if path.suffix != ".jsonl":
            return False
        known_types = {
            "assistant", "user", "system",
            "permission-mode", "summary", "meta",
        }
        try:
            with path.open("r", encoding="utf-8", errors="replace") as f:
                for _ in range(5):
                    line = f.readline()
                    if not line:
                        break
                    if not line.strip():
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(obj, dict) and obj.get("type") in known_types:
                        return True
        except OSError:
            return False
        return False

    def parse(self, path: Path) -> Transcript:
        messages = tuple(self.stream(path))
        phase_hint = self._detect_phase(path, messages)
        return Transcript(
            source_path=path,
            harness=self.name,
            phase_hint=phase_hint,
            messages=messages,
        )

    def stream(self, path: Path) -> Iterator[Message]:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for raw in f:
                line = raw.rstrip("\n")
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = self._decode(data, path)
                if msg:
                    yield msg

    def _decode(self, data: dict, path: Path) -> Message | None:
        typ = data.get("type")
        if typ == "assistant" and isinstance(data.get("message"), dict):
            msg = data["message"]
            usage_raw = msg.get("usage", {}) or {}
            model = msg.get("model")
            # Skip records with no real LLM call (bookkeeping entries like <synthetic>
            # or compaction summaries often have empty usage or no model).
            usage = self._build_usage_or_none(usage_raw, model)
            text = self._excerpt(msg.get("content", ""))
            self._scan_secrets(text, path)
            return Message(
                role="assistant",
                agent_id=None,
                usage=usage,
                text_excerpt=text,
            )
        if typ == "user" and isinstance(data.get("toolUseResult"), dict):
            tur = data["toolUseResult"]
            usage_raw = tur.get("usage")
            agent_id = tur.get("agentId")
            if usage_raw and agent_id:
                model = tur.get("model")
                usage = self._build_usage_or_none(usage_raw, model)
                text = self._excerpt(tur.get("prompt", ""))
                self._scan_secrets(text, path)
                return Message(
                    role="tool_result",
                    agent_id=str(agent_id),
                    usage=usage,
                    text_excerpt=text,
                )
            return None
        if typ == "user":
            text = self._excerpt(data.get("message", ""))
            self._scan_secrets(text, path)
            return Message(role="user", agent_id=None, usage=None, text_excerpt=text)
        return None

    @staticmethod
    def _build_usage_or_none(raw: dict, model: str | None) -> Usage | None:
        """Build a Usage record, or None if the record has no billable tokens.

        Claude Code transcripts include bookkeeping records (compaction summaries,
        <synthetic> markers, cached-only entries) where a Usage row would distort
        cost calculation. We skip them rather than forcing a bogus model lookup.
        """
        input_t = int(raw.get("input_tokens", 0) or 0)
        output_t = int(raw.get("output_tokens", 0) or 0)
        cache_c = int(raw.get("cache_creation_input_tokens", 0) or 0)
        cache_r = int(raw.get("cache_read_input_tokens", 0) or 0)
        # Skip if no billable activity
        if input_t == 0 and output_t == 0 and cache_c == 0 and cache_r == 0:
            return None
        # Skip if model is synthetic / missing — no real LLM call cost attached
        if not model or model in ("<synthetic>", "unknown", ""):
            return None
        return Usage(
            input_tokens=input_t,
            output_tokens=output_t,
            cache_creation=cache_c,
            cache_read=cache_r,
            model=str(model),
        )

    @staticmethod
    def _build_usage(raw: dict, model: str) -> Usage:
        return Usage(
            input_tokens=int(raw.get("input_tokens", 0)),
            output_tokens=int(raw.get("output_tokens", 0)),
            cache_creation=int(raw.get("cache_creation_input_tokens", 0)),
            cache_read=int(raw.get("cache_read_input_tokens", 0)),
            model=str(model),
        )

    @staticmethod
    def _excerpt(content: str | list | dict | None) -> str:
        """Coerce any message-content shape to a ≤ 120-char string."""
        if content is None:
            return ""
        if isinstance(content, dict):
            # Claude Code user records wrap the real content in {role, content}.
            inner = content.get("content", content.get("text", ""))
            return __class__._excerpt(inner)  # type: ignore[name-defined]
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, dict):
                    parts.append(str(item.get("text", item.get("content", ""))))
                else:
                    parts.append(str(item))
            content = " ".join(parts)
        return str(content or "")[:120]

    @staticmethod
    def _scan_secrets(text: str, path: Path) -> None:
        for pattern in _SECRET_PATTERNS:
            m = pattern.search(text)
            if m:
                raise SecretsDetectedError(
                    f"refusing to process transcript: potential secret detected "
                    f"in {path.name} (pattern matched: {pattern.pattern[:40]}…)"
                )

    @staticmethod
    def _detect_phase(path: Path, messages: tuple[Message, ...]) -> str | None:
        # Env var strategy (captured at transcript start)
        env_var = os.environ.get("SDLC_PHASE", "")
        m = re.match(r"^0?([1-6])$", env_var)
        if m:
            return f"0{m.group(1)}"
        # Prompt marker strategy
        for msg in messages[:5]:
            m = re.search(r"(?i)\[phase[- ]?(\d)\]|/sdlc\s+phase\s+(\d)", msg.text_excerpt)
            if m:
                num = m.group(1) or m.group(2)
                return f"0{num}"
        return None
