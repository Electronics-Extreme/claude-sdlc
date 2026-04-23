#!/usr/bin/env python3
"""SDLC Metrics CLI entry point.

Subcommands:
  analyze       — parse a transcript, print token/cost breakdown
  budget-check  — analyze + enforce per-phase budget (exit 1 on breach)
  trend         — show history over last N runs
  adapters      — list registered adapters + implementation status
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from _python_check import require_python_311  # noqa: E402

require_python_311()


# Local package imports (module-relative)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sdlc_metrics.adapters import all_adapters, find_adapter  # type: ignore  # noqa: E402
from sdlc_metrics import budgets as budgets_mod  # type: ignore  # noqa: E402
from sdlc_metrics import history as history_mod  # type: ignore  # noqa: E402
from sdlc_metrics.aggregator import aggregate  # type: ignore  # noqa: E402
from sdlc_metrics.errors import (  # type: ignore  # noqa: E402
    BudgetBreachError, ConfigError, PricingMissingError, SecretsDetectedError,
)
from sdlc_metrics.pricing import load_pricing  # type: ignore  # noqa: E402
from sdlc_metrics.report import (  # type: ignore  # noqa: E402
    format_html, format_json, format_markdown, format_text,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _run_analyze(path: Path, fmt: str, phase_override: str | None,
                 budget_check: bool = False) -> int:
    repo = _repo_root()
    pricing = load_pricing(repo)

    adapter = find_adapter(path)
    if adapter is None:
        print(f"error: no adapter can parse {path}. Try: analyze.py adapters --list",
              file=sys.stderr)
        return 1
    try:
        transcript = adapter.parse(path)
    except SecretsDetectedError as e:
        print(f"error: {e}", file=sys.stderr)
        return 3

    agg = aggregate(transcript)

    phase = phase_override or transcript.phase_hint

    verdict = None
    if budget_check or phase:
        # Compute cost once
        total_cost = 0.0
        if agg.main:
            total_cost += pricing.cost_of(
                input_tokens=agg.main.input_tokens, output_tokens=agg.main.output_tokens,
                cache_read=agg.main.cache_read, cache_creation=agg.main.cache_creation,
                model=agg.main.model,
            )
        for u in agg.subagents.values():
            total_cost += pricing.cost_of(
                input_tokens=u.input_tokens, output_tokens=u.output_tokens,
                cache_read=u.cache_read, cache_creation=u.cache_creation,
                model=u.model,
            )
        total_tokens = agg.total_usage.total_tokens

        if budget_check:
            if phase is None:
                print("error: budget-check requires --phase or an auto-detected phase marker.",
                      file=sys.stderr)
                return 2
            budgets = budgets_mod.load_budgets(repo)
            pbudget = budgets.for_phase(phase)
            if pbudget is None:
                print(f"error: no budget defined for phase {phase} in config/budgets.yaml",
                      file=sys.stderr)
                return 2
            verdict = budgets_mod.evaluate(
                phase=phase,
                actual_cost=total_cost,
                actual_tokens=total_tokens,
                actual_cache_hit=agg.cache_hit_rate,
                budget=pbudget,
            )

    if fmt == "text":
        out = format_text(transcript=transcript, agg=agg, pricing=pricing,
                          phase=phase, budget_verdict=verdict)
    elif fmt == "json":
        out = format_json(transcript=transcript, agg=agg, pricing=pricing,
                          phase=phase, budget_verdict=verdict)
    elif fmt == "markdown":
        out = format_markdown(transcript=transcript, agg=agg, pricing=pricing,
                              phase=phase, budget_verdict=verdict)
    elif fmt == "html":
        out = format_html(transcript=transcript, agg=agg, pricing=pricing,
                          phase=phase, budget_verdict=verdict)
    else:
        print(f"error: unknown format {fmt}", file=sys.stderr)
        return 2

    print(out)

    # Record to history
    try:
        session_bytes = path.read_bytes()
        session_hash = hashlib.sha256(session_bytes).hexdigest()[:16]
        total_cost_for_hist = 0.0
        if agg.main:
            total_cost_for_hist += pricing.cost_of(
                input_tokens=agg.main.input_tokens, output_tokens=agg.main.output_tokens,
                cache_read=agg.main.cache_read, cache_creation=agg.main.cache_creation,
                model=agg.main.model,
            )
        for u in agg.subagents.values():
            total_cost_for_hist += pricing.cost_of(
                input_tokens=u.input_tokens, output_tokens=u.output_tokens,
                cache_read=u.cache_read, cache_creation=u.cache_creation,
                model=u.model,
            )
        history_mod.record(
            db_path=history_mod.default_db_path(repo),
            phase=phase,
            adapter=transcript.harness,
            session_hash=session_hash,
            total_tokens=agg.total_usage.total_tokens,
            cost_usd=total_cost_for_hist,
            cache_hit_rate=agg.cache_hit_rate,
            budget_verdict=(
                "pass" if (verdict and verdict.ok) else
                "fail" if (verdict and not verdict.ok) else
                "none"
            ),
        )
    except OSError:
        # Non-fatal — history is best-effort
        pass

    if verdict and not verdict.ok:
        return 1
    return 0


def _run_trend(phase: str | None, last: int) -> int:
    repo = _repo_root()
    runs = history_mod.trend(db_path=history_mod.default_db_path(repo), phase=phase, last=last)
    if not runs:
        print("(no history yet)")
        return 0
    print(f"{'ts':<26} {'phase':<6} {'adapter':<14} {'tokens':>10} {'cost':>8} {'cache%':>7} {'verdict':<8}")
    print("-" * 86)
    for r in runs:
        print(f"{r.ts:<26} {(r.phase or '—'):<6} {r.adapter:<14} "
              f"{r.total_tokens:>10,} ${r.cost_usd:>7.3f} "
              f"{r.cache_hit_rate * 100:>6.1f}% {r.budget_verdict:<8}")
    return 0


def _run_adapters() -> int:
    adapters = all_adapters()
    print(f"{'Adapter':<18} {'Status':<20} {'can_parse() lookup'}")
    print("-" * 60)
    for cls in adapters:
        status = "IMPLEMENTED" if cls.__name__ == "ClaudeCodeAdapter" else "STUB (PR welcome)"
        print(f"{cls.name:<18} {status:<20} {cls.__module__}")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="sdlc-metrics",
        description="Phase-aware token/cost analyzer + budget gate.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    pa = sub.add_parser("analyze", help="analyze a transcript")
    pa.add_argument("path")
    pa.add_argument("--format", choices=["text", "json", "markdown", "html"], default="text")
    pa.add_argument("--phase", help="override detected phase (e.g. '03')")

    pb = sub.add_parser("budget-check", help="analyze + check against budget")
    pb.add_argument("path")
    pb.add_argument("--phase", help="phase override (required if no marker in transcript)")
    pb.add_argument("--format", choices=["text", "json", "markdown", "html"], default="text")

    pt = sub.add_parser("trend", help="show run history")
    pt.add_argument("--phase", help="filter by phase")
    pt.add_argument("--last", type=int, default=10)

    sub.add_parser("adapters", help="list registered adapters + status")

    args = parser.parse_args(argv[1:])

    try:
        if args.cmd == "analyze":
            return _run_analyze(Path(args.path), args.format, args.phase)
        if args.cmd == "budget-check":
            return _run_analyze(Path(args.path), args.format, args.phase, budget_check=True)
        if args.cmd == "trend":
            return _run_trend(args.phase, args.last)
        if args.cmd == "adapters":
            return _run_adapters()
    except PricingMissingError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except ConfigError as e:
        print(f"config error: {e}", file=sys.stderr)
        return 2
    except BudgetBreachError as e:
        print(f"budget breach: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
