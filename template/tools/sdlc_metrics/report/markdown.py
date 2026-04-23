"""Markdown report formatter — PR-comment ready."""
from __future__ import annotations

from ..normalizer import Aggregate, Transcript
from ..pricing import Pricing


def format_markdown(*, transcript: Transcript, agg: Aggregate, pricing: Pricing,
                    phase: str | None = None, budget_verdict=None) -> str:
    lines: list[str] = []
    lines.append("### SDLC Metrics")
    lines.append("")
    if phase:
        lines.append(f"**Phase**: `{phase}` · **Harness**: `{transcript.harness}` · **Messages**: {agg.message_count}")
    lines.append("")
    lines.append("| Agent | Model | Input | Output | Cache-read | Cost (USD) |")
    lines.append("|---|---|---:|---:|---:|---:|")

    total_cost = 0.0
    if agg.main:
        u = agg.main
        c = pricing.cost_of(
            input_tokens=u.input_tokens,
            output_tokens=u.output_tokens,
            cache_read=u.cache_read,
            cache_creation=u.cache_creation,
            model=u.model,
        )
        total_cost += c
        lines.append(f"| main | `{u.model}` | {u.input_tokens:,} | {u.output_tokens:,} | {u.cache_read:,} | ${c:.3f} |")

    for agent_id, u in sorted(agg.subagents.items()):
        c = pricing.cost_of(
            input_tokens=u.input_tokens,
            output_tokens=u.output_tokens,
            cache_read=u.cache_read,
            cache_creation=u.cache_creation,
            model=u.model,
        )
        total_cost += c
        lines.append(f"| `{agent_id}` | `{u.model}` | {u.input_tokens:,} | {u.output_tokens:,} | {u.cache_read:,} | ${c:.3f} |")

    lines.append(f"| **TOTAL** | — | {agg.total_usage.input_tokens:,} | {agg.total_usage.output_tokens:,} | {agg.total_usage.cache_read:,} | **${total_cost:.3f}** |")
    lines.append("")
    lines.append(f"**Cache hit rate**: {agg.cache_hit_rate * 100:.1f}%")
    lines.append(f"**Pricing synced**: {pricing.last_synced}")

    if budget_verdict is not None:
        lines.append("")
        lines.append(f"**Budget** (phase `{budget_verdict.phase}`): ")
        if budget_verdict.ok:
            lines.append(f"✓ PASS (${budget_verdict.cost_usd:.3f} = {budget_verdict.cost_pct:.0f}% of ${budget_verdict.cost_hard_cap:.3f} hard-cap)")
        else:
            lines.append("✘ BREACH:")
            for b in budget_verdict.breaches:
                lines.append(f"- {b}")
    return "\n".join(lines)
