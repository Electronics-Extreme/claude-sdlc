"""Budget loader + gate logic."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .errors import BudgetBreachError, ConfigError


@dataclass(frozen=True, slots=True)
class BudgetBand:
    p50: float
    p95: float
    hard_cap: float


@dataclass(frozen=True, slots=True)
class CacheBand:
    target: float
    fail_below: float


@dataclass(frozen=True, slots=True)
class PhaseBudget:
    phase: str
    tokens: BudgetBand
    cost_usd: BudgetBand
    cache_hit_rate: CacheBand


@dataclass(frozen=True, slots=True)
class Budgets:
    version: int
    informational: bool
    phases: dict[str, PhaseBudget]

    def for_phase(self, phase_id: str) -> PhaseBudget | None:
        return self.phases.get(phase_id)


_PHASE_KEY_RE = re.compile(r'^  "?(0[1-6])"?:\s*(?:#.*)?$')
_SUBSEC_RE = re.compile(r"^    (tokens|cost_usd|cache_hit_rate):\s*(?:#.*)?$")
_FIELD_RE = re.compile(r"^      ([a-z_]+):\s*([0-9.]+)\s*(?:#.*)?$")


def load_budgets(repo_root: Path) -> Budgets:
    path = repo_root / "config" / "budgets.yaml"
    if not path.exists():
        raise ConfigError(f"budgets.yaml not found at {path}")
    text = path.read_text(encoding="utf-8")

    version = 1
    informational = True
    phases: dict[str, dict[str, dict[str, float]]] = {}
    current_phase: str | None = None
    current_sub: str | None = None
    in_phases = False

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("version:"):
            version = int(line.split(":", 1)[1].strip())
            continue
        if line.startswith("informational:"):
            v = line.split(":", 1)[1].strip().lower()
            informational = v in ("true", "1", "yes")
            continue
        if line == "phases:":
            in_phases = True
            continue
        if not in_phases:
            continue

        m = _PHASE_KEY_RE.match(line)
        if m:
            current_phase = m.group(1)
            phases[current_phase] = {}
            current_sub = None
            continue
        if current_phase is None:
            continue
        s = _SUBSEC_RE.match(line)
        if s:
            current_sub = s.group(1)
            phases[current_phase][current_sub] = {}
            continue
        if current_sub is None:
            continue
        f = _FIELD_RE.match(line)
        if f:
            phases[current_phase][current_sub][f.group(1)] = float(f.group(2))

    parsed: dict[str, PhaseBudget] = {}
    for phase_id, subs in phases.items():
        t = subs.get("tokens", {})
        c = subs.get("cost_usd", {})
        h = subs.get("cache_hit_rate", {})
        parsed[phase_id] = PhaseBudget(
            phase=phase_id,
            tokens=BudgetBand(
                p50=t.get("p50", 0.0),
                p95=t.get("p95", 0.0),
                hard_cap=t.get("hard_cap", 0.0),
            ),
            cost_usd=BudgetBand(
                p50=c.get("p50", 0.0),
                p95=c.get("p95", 0.0),
                hard_cap=c.get("hard_cap", 0.0),
            ),
            cache_hit_rate=CacheBand(
                target=h.get("target", 0.0),
                fail_below=h.get("fail_below", 0.0),
            ),
        )

    return Budgets(version=version, informational=informational, phases=parsed)


@dataclass(frozen=True, slots=True)
class BudgetVerdict:
    phase: str
    ok: bool
    cost_usd: float
    cost_hard_cap: float
    cost_pct: float
    tokens: int
    tokens_hard_cap: int
    cache_hit_rate: float
    cache_fail_below: float
    breaches: tuple[str, ...]


def evaluate(*, phase: str, actual_cost: float, actual_tokens: int,
             actual_cache_hit: float, budget: PhaseBudget) -> BudgetVerdict:
    breaches: list[str] = []
    if actual_cost > budget.cost_usd.hard_cap:
        breaches.append(
            f"cost ${actual_cost:.3f} > hard_cap ${budget.cost_usd.hard_cap:.3f} "
            f"(+{(actual_cost / budget.cost_usd.hard_cap - 1) * 100:.0f}%)"
        )
    if actual_tokens > budget.tokens.hard_cap:
        breaches.append(
            f"tokens {actual_tokens:,} > hard_cap {int(budget.tokens.hard_cap):,}"
        )
    # Cache hit rate below floor is a WARNING not a failure
    pct = (actual_cost / budget.cost_usd.hard_cap * 100.0) if budget.cost_usd.hard_cap else 0.0
    return BudgetVerdict(
        phase=phase,
        ok=not breaches,
        cost_usd=actual_cost,
        cost_hard_cap=budget.cost_usd.hard_cap,
        cost_pct=pct,
        tokens=actual_tokens,
        tokens_hard_cap=int(budget.tokens.hard_cap),
        cache_hit_rate=actual_cache_hit,
        cache_fail_below=budget.cache_hit_rate.fail_below,
        breaches=tuple(breaches),
    )
