"""Text-table report formatter — fixed-width ≤ 120 char."""
from __future__ import annotations

from ..normalizer import Aggregate, Transcript, Usage
from ..pricing import Pricing


def _fmt_n(n: int) -> str:
    return f"{n:,}"


def _row(agent: str, desc: str, msgs: int, u: Usage, cost: float) -> str:
    return (
        f"{agent:<15} {desc:<35} {msgs:>5} "
        f"{_fmt_n(u.input_tokens):>10} "
        f"{_fmt_n(u.output_tokens):>10} "
        f"{_fmt_n(u.cache_read):>10} "
        f"${cost:>7.3f}"
    )


def format_text(*, transcript: Transcript, agg: Aggregate, pricing: Pricing,
                phase: str | None = None, budget_verdict=None) -> str:
    lines: list[str] = []
    w = "=" * 104
    sep = "-" * 104
    lines.append(w)
    lines.append("TOKEN USAGE ANALYSIS")
    lines.append(w)
    lines.append("")
    if phase:
        lines.append(f"Phase: {phase}")
    lines.append(f"Source: {transcript.source_path}")
    lines.append(f"Harness: {transcript.harness}")
    lines.append(f"Messages: {agg.message_count}")
    lines.append("")
    lines.append(f"{'Agent':<15} {'Description':<35} {'Msgs':>5} {'Input':>10} {'Output':>10} {'Cache':>10} {'Cost':>8}")
    lines.append(sep)
    total_cost = 0.0

    if agg.main:
        c = pricing.cost_of(
            input_tokens=agg.main.input_tokens,
            output_tokens=agg.main.output_tokens,
            cache_read=agg.main.cache_read,
            cache_creation=agg.main.cache_creation,
            model=agg.main.model,
        )
        total_cost += c
        lines.append(_row("main", f"Main session ({agg.main.model})", 1, agg.main, c))

    for agent_id, u in sorted(agg.subagents.items()):
        c = pricing.cost_of(
            input_tokens=u.input_tokens,
            output_tokens=u.output_tokens,
            cache_read=u.cache_read,
            cache_creation=u.cache_creation,
            model=u.model,
        )
        total_cost += c
        desc = f"Subagent ({u.model})"[:35]
        lines.append(_row(agent_id[:15], desc, 1, u, c))

    lines.append(sep)
    lines.append("")
    total = agg.total_usage
    lines.append("TOTALS:")
    lines.append(f"  Messages:          {_fmt_n(agg.message_count)}")
    lines.append(f"  Input tokens:      {_fmt_n(total.input_tokens)}")
    lines.append(f"  Output tokens:     {_fmt_n(total.output_tokens)}")
    lines.append(f"  Cache read:        {_fmt_n(total.cache_read)}")
    lines.append(f"  Cache create:      {_fmt_n(total.cache_creation)}")
    lines.append(f"  Total (all):       {_fmt_n(total.total_tokens)}")
    lines.append(f"  Cache hit rate:    {agg.cache_hit_rate * 100:.1f}%")
    lines.append("")
    lines.append(f"  Estimated cost:    ${total_cost:.3f}")
    lines.append(f"  Pricing synced:    {pricing.last_synced}")

    if budget_verdict is not None:
        lines.append("")
        lines.append(f"BUDGET (phase {budget_verdict.phase}):")
        if budget_verdict.ok:
            lines.append(f"  ✓ PASS: cost ${budget_verdict.cost_usd:.3f} "
                         f"({budget_verdict.cost_pct:.0f}% of hard-cap ${budget_verdict.cost_hard_cap:.3f})")
        else:
            lines.append(f"  ✘ BREACH:")
            for b in budget_verdict.breaches:
                lines.append(f"    - {b}")
        if budget_verdict.cache_hit_rate < budget_verdict.cache_fail_below:
            lines.append(f"  ⚠ Cache hit rate {budget_verdict.cache_hit_rate * 100:.1f}% "
                         f"below floor {budget_verdict.cache_fail_below * 100:.0f}%")

    lines.append("")
    lines.append(w)
    return "\n".join(lines)
