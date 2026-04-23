"""HTML standalone report — single file, no external URLs."""
from __future__ import annotations

import html

from ..normalizer import Aggregate, Transcript
from ..pricing import Pricing


_CSS = """
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
         max-width: 900px; margin: 2em auto; color: #222; background: #fafafa; padding: 0 1em; }
  h1 { border-bottom: 2px solid #2a7ae4; padding-bottom: 0.3em; }
  table { border-collapse: collapse; width: 100%; margin: 1em 0; }
  th, td { text-align: left; padding: 0.4em 0.8em; border-bottom: 1px solid #eee; }
  th { background: #eef; }
  td.num { text-align: right; font-variant-numeric: tabular-nums; }
  tr.total { font-weight: bold; background: #fff4e0; }
  .ok  { color: #2a8039; font-weight: bold; }
  .bad { color: #a41f1f; font-weight: bold; }
  .meta { color: #666; font-size: 0.9em; }
  .breach { background: #ffe8e8; padding: 0.5em; border-left: 3px solid #a41f1f; }
</style>
"""


def format_html(*, transcript: Transcript, agg: Aggregate, pricing: Pricing,
                phase: str | None = None, budget_verdict=None) -> str:
    esc = html.escape

    rows: list[str] = []
    total_cost = 0.0

    def row(agent: str, u, cost: float) -> str:
        return (f"<tr><td>{esc(agent)}</td><td><code>{esc(u.model)}</code></td>"
                f"<td class='num'>{u.input_tokens:,}</td>"
                f"<td class='num'>{u.output_tokens:,}</td>"
                f"<td class='num'>{u.cache_read:,}</td>"
                f"<td class='num'>${cost:.3f}</td></tr>")

    if agg.main:
        c = pricing.cost_of(input_tokens=agg.main.input_tokens, output_tokens=agg.main.output_tokens,
                            cache_read=agg.main.cache_read, cache_creation=agg.main.cache_creation,
                            model=agg.main.model)
        total_cost += c
        rows.append(row("main", agg.main, c))
    for aid, u in sorted(agg.subagents.items()):
        c = pricing.cost_of(input_tokens=u.input_tokens, output_tokens=u.output_tokens,
                            cache_read=u.cache_read, cache_creation=u.cache_creation, model=u.model)
        total_cost += c
        rows.append(row(aid, u, c))

    total = agg.total_usage
    rows.append(
        f"<tr class='total'><td colspan='2'>TOTAL</td>"
        f"<td class='num'>{total.input_tokens:,}</td>"
        f"<td class='num'>{total.output_tokens:,}</td>"
        f"<td class='num'>{total.cache_read:,}</td>"
        f"<td class='num'>${total_cost:.3f}</td></tr>"
    )

    budget_html = ""
    if budget_verdict is not None:
        if budget_verdict.ok:
            budget_html = (
                f"<p class='ok'>✓ Budget PASS (phase {esc(budget_verdict.phase)}): "
                f"${budget_verdict.cost_usd:.3f} = {budget_verdict.cost_pct:.0f}% of hard-cap "
                f"${budget_verdict.cost_hard_cap:.3f}</p>"
            )
        else:
            items = "".join(f"<li>{esc(b)}</li>" for b in budget_verdict.breaches)
            budget_html = (
                f"<div class='breach'><p class='bad'>✘ Budget BREACH "
                f"(phase {esc(budget_verdict.phase)}):</p><ul>{items}</ul></div>"
            )

    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<title>SDLC Metrics — {esc(str(transcript.source_path.name))}</title>
{_CSS}
</head><body>
<h1>SDLC Metrics</h1>
<p class="meta">
  Source: <code>{esc(str(transcript.source_path))}</code> ·
  Harness: <code>{esc(transcript.harness)}</code> ·
  Phase: <code>{esc(phase or 'unknown')}</code> ·
  Messages: {agg.message_count}
</p>
<table>
<thead><tr><th>Agent</th><th>Model</th><th>Input</th><th>Output</th><th>Cache-read</th><th>Cost</th></tr></thead>
<tbody>
{"".join(rows)}
</tbody>
</table>
<p class="meta">Cache hit rate: <strong>{agg.cache_hit_rate * 100:.1f}%</strong> ·
Pricing synced: {esc(pricing.last_synced)}</p>
{budget_html}
</body></html>
"""
