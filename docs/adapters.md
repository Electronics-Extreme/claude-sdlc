---
doc: docs/adapters.md
status: signed
signed_by: Thanin Piromward on 2026-04-23
required_for: [phase-6-CR-implementation]
cite_as: ADPT
---

# Writing a new transcript adapter

This guide covers how to contribute a new harness adapter to
`tools/sdlc_metrics/adapters/`.

## Scope

An adapter parses a session transcript produced by a specific harness and
normalizes it to the kit's `Transcript(messages=tuple[Message, ...])` shape.

Target: ≤ 200 LOC per adapter for well-formed transcript formats
(NFR-METRICS-ADAPT-1).

## Interface

Subclass `BaseAdapter` from `tools/sdlc_metrics/adapters/base.py`:

```python
from pathlib import Path
from typing import Iterator
from ..normalizer import Message, Transcript, Usage
from .base import BaseAdapter

class MyHarnessAdapter(BaseAdapter):
    name = "my-harness"  # must match a key in config/harnesses.yaml

    @classmethod
    def can_parse(cls, path: Path) -> bool:
        # Cheap probe. Open the first line; check shape.
        ...

    def parse(self, path: Path) -> Transcript:
        messages = tuple(self.stream(path))
        return Transcript(source_path=path, harness=self.name,
                          phase_hint=self._detect_phase(...),
                          messages=messages)

    def stream(self, path: Path) -> Iterator[Message]:
        # Yield one Message at a time (memory-safe for large files).
        ...
```

## Register the adapter

Add to `tools/sdlc_metrics/adapters/__init__.py` in `all_adapters()`:

```python
from . import my_harness
return [
    ClaudeCodeAdapter,
    ...,
    my_harness.MyHarnessAdapter,
]
```

## Required behaviors

1. **Secrets pre-filter** — call the same regex sweep as `ClaudeCodeAdapter._scan_secrets`
   on any user-visible content. Raise `SecretsDetectedError` if a pattern matches.
2. **Phase detection** — respect the four strategies in `config/phase-markers.yaml`:
   env var, prompt marker, branch prefix, commit prefix.
3. **Model names** — emit canonical model IDs that match `config/pricing.yaml`.
   Unknown models cause `PricingMissingError` at analyze time.
4. **Cache tokens** — split `cache_read` from `cache_creation` — these price
   differently (10× factor on Anthropic).
5. **Agent IDs** — use harness-native subagent IDs. Main session emits `agent_id=None`.

## Testing

Add a synthetic transcript fixture under
`tools/sdlc_metrics/tests/fixtures/sample-<harness>.<ext>` — minimal, 3-5 messages,
covering: main message, subagent call, cache read, multiple models if supported.

Run:

```bash
python3 tools/sdlc_metrics/analyze.py analyze tools/sdlc_metrics/tests/fixtures/sample-<harness>.<ext> --format text
python3 tools/sdlc_metrics/analyze.py analyze tools/sdlc_metrics/tests/fixtures/sample-<harness>.<ext> --format json
```

Both must succeed; the json output should validate against the schema v1 shape.

## PR checklist

- [ ] Adapter class ≤ 200 LOC
- [ ] `can_parse()` returns False for non-matching files
- [ ] Secrets pre-filter on every decoded Message
- [ ] Phase detection honors env var first, then markers/branch/commit
- [ ] Model names match canonical IDs in `config/pricing.yaml`
- [ ] Synthetic fixture committed under `tools/sdlc_metrics/tests/fixtures/`
- [ ] `config/harnesses.yaml` entry updated with api_stability label
- [ ] `NOTICE.md` attribution added if the parser approach was borrowed from
      another OSS project
- [ ] CHANGELOG [Unreleased] entry referencing the CR

## Stability labels

`config/harnesses.yaml` tags each adapter's stability as:
- `documented-stable` — harness vendor officially documents the transcript format
- `field-tested` — works empirically; vendor docs unclear on stability
- `experimental` — uses an experimental vendor API; expect churn
- `best-effort` — Layer-2-only, reads `AGENTS.md`, no structured transcript

Ensure your label is accurate and updated on vendor-API changes.
