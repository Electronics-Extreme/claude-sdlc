#!/usr/bin/env python3
"""Bulk-add doc frontmatter to existing phase docs.

Infers `status` from file contents:
  - Contains {{PLACEHOLDER}} residue → status: template
  - Clean + has "Signed off by ... on YYYY-MM-DD" → status: signed (extract signer)
  - Clean but no sign-off line → status: draft

Usage:
  python3 scripts/add_frontmatter.py --dry-run   # show what would change
  python3 scripts/add_frontmatter.py --write     # apply
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _python_check import require_python_311  # noqa: E402

require_python_311()


SCAN_ROOTS = ["docs/sdlc", "skill"]

PLACEHOLDER_RE = re.compile(r"\{\{[^}]*\}\}")
SIGNOFF_RE = re.compile(r"Signed off by ([A-Za-z][A-Za-z\s\.\-']+?) on (\d{4}-\d{2}-\d{2})")

# Heuristic cite_as mapping per file basename.
CITE_AS = {
    "srs.md": "SRS",
    "functional_requirements.md": "FR",
    "non_functional_requirements.md": "NFR",
    "use_cases.md": "UC",
    "acceptance_criteria.md": "AC",
    "stakeholders.md": "STK",
    "glossary.md": "GL",
    "assumptions_and_constraints.md": "AS",
    "architecture.md": "ARC",
    "data_model.md": "DM",
    "database_design.md": "DB",
    "api_design.md": "API",
    "sequence_diagrams.md": "SEQ",
    "ui_design.md": "UI",
    "trade_offs.md": "TO",
    "coding_standards.md": "CS",
    "module_breakdown.md": "MB",
    "development_plan.md": "DEV",
    "branching_and_commits.md": "BR",
    "code_review_checklist.md": "CRC",
    "build_and_run.md": "BAR",
    "traceability_matrix.md": "TM",
    "task_list.md": "TL",
    "test_plan.md": "TP",
    "test_cases.md": "TC",
    "test_data.md": "TD",
    "test_report.md": "TR",
    "defect_log.md": "DL",
    "uat_plan.md": "UAT",
    "deployment_plan.md": "DP",
    "release_notes.md": "RN",
    "rollback_plan.md": "RB",
    "runbook.md": "RBK",
    "smoke_tests.md": "SMK",
    "go_live_checklist.md": "GLC",
    "maintenance_plan.md": "MP",
    "incident_log.md": "IL",
    "change_requests.md": "CR",
    "sla_and_slo.md": "SLA",
    "monitoring.md": "MON",
    "eol_policy.md": "EOL",
    "README.md": "README",
    "SKILL.md": "SKILL",
    "bootstrap.md": "BOOT",
    "reconciliation.md": "REC",
    "traceability-matrix.md": "TM",
}

PHASE_REQUIRED_FOR: dict[str, list[str]] = {
    "docs/sdlc/01_requirement":    ["phase-1-artifact-authoring"],
    "docs/sdlc/02_design":         ["phase-2-artifact-authoring", "phase-3-slice"],
    "docs/sdlc/03_implementation": ["phase-3-slice", "phase-3-refactor"],
    "docs/sdlc/04_testing":        ["phase-4-test-authoring", "phase-4-test-execution"],
    "docs/sdlc/05_deployment":     ["phase-5-deploy-prep", "phase-5-release-cutting"],
    "docs/sdlc/06_maintenance":    ["phase-6-CR-authoring", "phase-6-CR-implementation", "phase-6-routine-maintenance"],
}


def _infer_status(text: str) -> tuple[str, str | None]:
    """Returns (status, signed_by_or_None)."""
    if PLACEHOLDER_RE.search(text):
        return "template", None
    m = SIGNOFF_RE.search(text)
    if m:
        return "signed", f"{m.group(1).strip()} on {m.group(2)}"
    return "draft", None


def _build_frontmatter(rel: Path, text: str) -> str:
    status, signed_by = _infer_status(text)
    doc = rel.as_posix()

    # required_for: use phase-dir segment. Phase docs live under docs/sdlc/0X_*.
    if rel.parts[:2] == ("docs", "sdlc") and len(rel.parts) >= 3:
        phase_dir = rel.parts[2]
    else:
        phase_dir = rel.parts[0] if rel.parts else ""
    if phase_dir in PHASE_REQUIRED_FOR:
        required_for = PHASE_REQUIRED_FOR[phase_dir]
    elif phase_dir == "skill":
        required_for = ["phase-3-slice", "phase-6-CR-implementation"]
    else:
        required_for = []

    cite_as = CITE_AS.get(rel.name, "")

    lines = ["---", f"doc: {doc}", f"status: {status}"]
    if signed_by:
        lines.append(f"signed_by: {signed_by}")
    if required_for:
        items = ", ".join(f'"{x}"' for x in required_for)
        lines.append(f"required_for: [{items}]")
    if cite_as:
        lines.append(f"cite_as: {cite_as}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def process(repo_root: Path, write: bool) -> tuple[int, int]:
    changed = 0
    skipped = 0
    for root_name in SCAN_ROOTS:
        root = repo_root / root_name
        if not root.exists():
            continue
        for path in root.rglob("*.md"):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if text.startswith("---\n"):
                skipped += 1
                continue

            rel = path.relative_to(repo_root)
            fm = _build_frontmatter(rel, text)
            new_text = fm + text

            if write:
                path.write_text(new_text, encoding="utf-8")
            else:
                status_line = fm.split("\n")[2]
                print(f"would add frontmatter to {rel}: {status_line}")
            changed += 1
    return changed, skipped


def main(argv: list[str]) -> int:
    mode = argv[1] if len(argv) > 1 else "--dry-run"
    if mode not in ("--dry-run", "--write"):
        print("usage: add_frontmatter.py [--dry-run|--write]", file=sys.stderr)
        return 2
    repo_root = Path(__file__).resolve().parent.parent
    write = mode == "--write"
    changed, skipped = process(repo_root, write)
    print(f"\n{'wrote' if write else 'would change'} {changed} file(s); {skipped} already have frontmatter.")
    if not write and changed:
        print("Re-run with --write to apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
