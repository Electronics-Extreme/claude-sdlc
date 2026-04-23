"""Run history store (SQLite). Local-only, per NFR-PRIVACY-NOLOGGING-1."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True, slots=True)
class RunRecord:
    id: int
    ts: str
    phase: str | None
    adapter: str
    session_hash: str
    total_tokens: int
    cost_usd: float
    cache_hit_rate: float
    budget_verdict: str  # pass | fail | warn | none


_DDL = """
CREATE TABLE IF NOT EXISTS runs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ts              TEXT NOT NULL,
    phase           TEXT,
    adapter         TEXT NOT NULL,
    session_hash    TEXT NOT NULL,
    total_tokens    INTEGER NOT NULL,
    cost_usd        REAL NOT NULL,
    cache_hit_rate  REAL NOT NULL,
    budget_verdict  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_runs_phase_ts ON runs(phase, ts);
"""


def _conn(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(db_path)
    c.executescript(_DDL)
    return c


def default_db_path(repo_root: Path) -> Path:
    return repo_root / ".metrics" / "history.db"


def record(*, db_path: Path, phase: str | None, adapter: str, session_hash: str,
           total_tokens: int, cost_usd: float, cache_hit_rate: float,
           budget_verdict: str) -> int:
    with _conn(db_path) as c:
        c.execute(
            "BEGIN IMMEDIATE",
        )
        cur = c.execute(
            "INSERT INTO runs(ts, phase, adapter, session_hash, total_tokens, "
            "cost_usd, cache_hit_rate, budget_verdict) VALUES (?,?,?,?,?,?,?,?)",
            (
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
                phase,
                adapter,
                session_hash,
                int(total_tokens),
                float(cost_usd),
                float(cache_hit_rate),
                budget_verdict,
            ),
        )
        c.commit()
        return int(cur.lastrowid or 0)


def trend(*, db_path: Path, phase: str | None = None, last: int = 10) -> list[RunRecord]:
    with _conn(db_path) as c:
        if phase:
            rows = c.execute(
                "SELECT id, ts, phase, adapter, session_hash, total_tokens, "
                "cost_usd, cache_hit_rate, budget_verdict FROM runs "
                "WHERE phase=? ORDER BY ts DESC LIMIT ?",
                (phase, last),
            ).fetchall()
        else:
            rows = c.execute(
                "SELECT id, ts, phase, adapter, session_hash, total_tokens, "
                "cost_usd, cache_hit_rate, budget_verdict FROM runs "
                "ORDER BY ts DESC LIMIT ?",
                (last,),
            ).fetchall()
    return [RunRecord(*r) for r in rows]


def prune(*, db_path: Path, keep: int = 500) -> int:
    with _conn(db_path) as c:
        total = c.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
        if total <= keep:
            return 0
        to_delete = total - keep
        c.execute(
            "DELETE FROM runs WHERE id IN ("
            "SELECT id FROM runs ORDER BY ts ASC LIMIT ?)",
            (to_delete,),
        )
        c.commit()
        return int(to_delete)
