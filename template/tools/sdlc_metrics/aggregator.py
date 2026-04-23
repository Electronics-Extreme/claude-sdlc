"""Roll up a Transcript into an Aggregate (per-subagent + per-model + totals)."""
from __future__ import annotations

from collections import defaultdict

from .normalizer import Aggregate, Message, Transcript, Usage


def aggregate(transcript: Transcript) -> Aggregate:
    agg = Aggregate()

    main_ins = main_out = main_cr = main_cc = 0
    main_model: str | None = None

    per_agent: dict[str, dict[str, int | str]] = defaultdict(
        lambda: {"input": 0, "output": 0, "cache_read": 0, "cache_create": 0, "model": "unknown"}
    )
    per_model: dict[str, dict[str, int]] = defaultdict(
        lambda: {"input": 0, "output": 0, "cache_read": 0, "cache_create": 0}
    )

    for msg in transcript.messages:
        agg.message_count += 1
        u = msg.usage
        if u is None:
            continue
        if msg.agent_id is None and msg.role == "assistant":
            main_ins += u.input_tokens
            main_out += u.output_tokens
            main_cr  += u.cache_read
            main_cc  += u.cache_creation
            main_model = u.model
            pm = per_model[u.model]
            pm["input"] += u.input_tokens
            pm["output"] += u.output_tokens
            pm["cache_read"] += u.cache_read
            pm["cache_create"] += u.cache_creation
        elif msg.agent_id is not None:
            pa = per_agent[msg.agent_id]
            pa["input"] = int(pa["input"]) + u.input_tokens
            pa["output"] = int(pa["output"]) + u.output_tokens
            pa["cache_read"] = int(pa["cache_read"]) + u.cache_read
            pa["cache_create"] = int(pa["cache_create"]) + u.cache_creation
            pa["model"] = u.model
            pm = per_model[u.model]
            pm["input"] += u.input_tokens
            pm["output"] += u.output_tokens
            pm["cache_read"] += u.cache_read
            pm["cache_create"] += u.cache_creation

    if main_ins or main_out or main_cr or main_cc:
        agg.main = Usage(
            input_tokens=main_ins,
            output_tokens=main_out,
            cache_read=main_cr,
            cache_creation=main_cc,
            model=main_model or "unknown",
        )
    for agent_id, d in per_agent.items():
        agg.subagents[agent_id] = Usage(
            input_tokens=int(d["input"]),
            output_tokens=int(d["output"]),
            cache_read=int(d["cache_read"]),
            cache_creation=int(d["cache_create"]),
            model=str(d["model"]),
        )
    for model, d in per_model.items():
        agg.per_model[model] = Usage(
            input_tokens=int(d["input"]),
            output_tokens=int(d["output"]),
            cache_read=int(d["cache_read"]),
            cache_creation=int(d["cache_create"]),
            model=model,
        )
    return agg
