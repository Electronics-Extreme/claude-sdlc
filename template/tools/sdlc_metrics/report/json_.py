"""JSON report formatter (schema v1)."""
from __future__ import annotations

import json
from dataclasses import asdict

from ..normalizer import Aggregate, Transcript, Usage
from ..pricing import Pricing


def _usage_dict(u: Usage, cost: float) -> dict:
    return {
        "input_tokens": u.input_tokens,
        "output_tokens": u.output_tokens,
        "cache_read": u.cache_read,
        "cache_creation": u.cache_creation,
        "total_input": u.total_input,
        "total_tokens": u.total_tokens,
        "model": u.model,
        "cost_usd": round(cost, 6),
    }


def format_json(*, transcript: Transcript, agg: Aggregate, pricing: Pricing,
                phase: str | None = None, budget_verdict=None) -> str:
    total_cost = 0.0
    main_dict = None
    if agg.main:
        c = pricing.cost_of(
            input_tokens=agg.main.input_tokens,
            output_tokens=agg.main.output_tokens,
            cache_read=agg.main.cache_read,
            cache_creation=agg.main.cache_creation,
            model=agg.main.model,
        )
        total_cost += c
        main_dict = _usage_dict(agg.main, c)

    subagents = {}
    for agent_id, u in sorted(agg.subagents.items()):
        c = pricing.cost_of(
            input_tokens=u.input_tokens,
            output_tokens=u.output_tokens,
            cache_read=u.cache_read,
            cache_creation=u.cache_creation,
            model=u.model,
        )
        total_cost += c
        subagents[agent_id] = _usage_dict(u, c)

    per_model = {}
    for model, u in agg.per_model.items():
        c = pricing.cost_of(
            input_tokens=u.input_tokens,
            output_tokens=u.output_tokens,
            cache_read=u.cache_read,
            cache_creation=u.cache_creation,
            model=u.model,
        )
        per_model[model] = _usage_dict(u, c)

    out = {
        "schema_version": 1,
        "source_path": str(transcript.source_path),
        "harness": transcript.harness,
        "phase": phase,
        "message_count": agg.message_count,
        "main": main_dict,
        "subagents": subagents,
        "models": per_model,
        "totals": {
            "input_tokens": agg.total_usage.input_tokens,
            "output_tokens": agg.total_usage.output_tokens,
            "cache_read": agg.total_usage.cache_read,
            "cache_creation": agg.total_usage.cache_creation,
            "total_tokens": agg.total_usage.total_tokens,
            "cache_hit_rate": round(agg.cache_hit_rate, 4),
            "cost_usd": round(total_cost, 6),
        },
        "pricing_synced": pricing.last_synced,
    }

    if budget_verdict is not None:
        out["budget"] = asdict(budget_verdict)

    return json.dumps(out, indent=2, sort_keys=True)
