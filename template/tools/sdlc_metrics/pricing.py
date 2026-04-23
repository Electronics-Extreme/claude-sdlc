"""Pricing table loader. Canonical source: config/pricing.yaml (Core rule 8)."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .errors import ConfigError, PricingMissingError


@dataclass(frozen=True, slots=True)
class ModelPrice:
    model: str
    input: float
    output: float
    cache_read: float
    cache_create: float
    tier_hint: str


@dataclass(frozen=True, slots=True)
class Pricing:
    version: int
    currency: str
    unit: str
    last_synced: str
    models: dict[str, ModelPrice]

    def cost_of(self, *, input_tokens: int, output_tokens: int,
                cache_read: int, cache_creation: int, model: str) -> float:
        mp = self.models.get(model)
        if mp is None:
            raise PricingMissingError(
                f"pricing.yaml missing entry for model: {model}\n"
                f"Known models: {sorted(self.models)}\n"
                f"Update config/pricing.yaml or run scripts/pricing_sync.py."
            )
        return (
            input_tokens    * mp.input        / 1_000_000
            + output_tokens * mp.output       / 1_000_000
            + cache_read    * mp.cache_read   / 1_000_000
            + cache_creation * mp.cache_create / 1_000_000
        )


_MODEL_KEY_RE = re.compile(r"^  ([a-zA-Z][a-zA-Z0-9._-]+):\s*$")
_FLOAT_FIELD_RE = re.compile(r"^    ([a-zA-Z_]+):\s*([0-9.]+|\"[^\"]*\"|'[^']*'|[A-Za-z][A-Za-z0-9_-]*)\s*$")


def load_pricing(repo_root: Path) -> Pricing:
    """Minimal YAML subset parser — no PyYAML dep per NFR-PORT-STDLIB-1."""
    path = repo_root / "config" / "pricing.yaml"
    if not path.exists():
        raise ConfigError(f"pricing.yaml not found at {path}")
    text = path.read_text(encoding="utf-8")

    meta: dict[str, str | int] = {}
    models: dict[str, dict[str, str]] = {}
    current_model: str | None = None
    in_models = False

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line == "models:":
            in_models = True
            continue
        if not in_models:
            # Top-level key: value
            if ":" in line and not line.startswith(" "):
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip().strip('"').strip("'")
            continue

        # Inside models:
        m = _MODEL_KEY_RE.match(line)
        if m:
            current_model = m.group(1)
            models[current_model] = {"model": current_model}
            continue
        if current_model is None:
            continue
        f = _FLOAT_FIELD_RE.match(line)
        if f:
            models[current_model][f.group(1)] = f.group(2).strip('"').strip("'")

    try:
        parsed = {
            name: ModelPrice(
                model=name,
                input=float(d.get("input", 0)),
                output=float(d.get("output", 0)),
                cache_read=float(d.get("cache_read", 0)),
                cache_create=float(d.get("cache_create", 0)),
                tier_hint=d.get("tier_hint", "unknown"),
            )
            for name, d in models.items()
        }
    except (ValueError, KeyError) as e:
        raise ConfigError(f"pricing.yaml malformed: {e}") from e

    return Pricing(
        version=int(meta.get("version", 1)),
        currency=str(meta.get("currency", "USD")),
        unit=str(meta.get("unit", "per_million_tokens")),
        last_synced=str(meta.get("last_synced", "unknown")),
        models=parsed,
    )
