---
doc: PRIVACY.md
status: signed
signed_by: Thanin Piromward on 2026-04-23
required_for: [phase-6-CR-implementation]
cite_as: PRIV
---

# Privacy

## Zero telemetry. Zero analytics. Zero beacons.

This kit performs no network I/O except for two explicitly user-invoked workflows:

1. **Pricing sync** (`scripts/pricing_sync.py`, optional) — fetches up-to-date Claude
   API prices from Anthropic's public docs. Runs only when you invoke it manually or
   via the scheduled `pricing-sync.yml` GitHub Actions workflow. Disable by removing
   the workflow file.
2. **Harness marketplace installs** (user-initiated via each harness's CLI) — e.g.
   `/plugin install` in Claude Code. These are harness-level operations; the kit
   itself issues no such calls.

Every other operation is local. No tracking pixels. No analytics endpoints. No
referral URLs. No cloud service dependencies. No phone-home on bootstrap, install,
sign-off, or any agent session.

## Data handling

- **Your project's phase docs, code, transcripts, reconciliation reports, history
  databases** — stay in your project directory. Never uploaded.
- **`tools/sdlc-metrics/` history** — stored in local SQLite (`.metrics/history.db`
  by default). Never transmitted.
- **Hook-injected context (SessionStart contract load)** — delivered to your agent
  as process stdout/JSON; never leaves your machine via the kit.
- **CI runs** — run on your chosen CI provider under your account. The kit has no
  CI infrastructure of its own.

## Secrets hygiene

The `scripts/check_residue.py` guard scans committed docs for
placeholder residue. It does NOT scan for secrets — use dedicated tooling
(`git-secrets`, `trufflehog`, or GitHub secret scanning) for that.

The `tools/sdlc-metrics/` analyzer includes a secrets pre-filter (per
NFR-METRICS-SEC-1) that refuses to process transcripts matching common credential
patterns (AWS keys, GitHub tokens, etc.). Detection is local, fail-closed, and
advisory — not a substitute for org-wide secrets management.

## Airgap-compatible

After `config/pricing.yaml` is populated, the full kit runs with no network access.
CI has an `airgap` job that disables networking and runs the script suite to
verify this property on every push (NFR-PRIVACY-AIRGAP-1).

## Compliance posture

- **Anonymous adoption metrics**: NOT COLLECTED. Adoption data is a nice-to-have;
  privacy trust is load-bearing for enterprise adoption. We chose the latter.
- **Opt-in telemetry**: NOT OFFERED. Even opt-in creates a network code path to
  maintain and audit. Zero is cleaner.
- **Voluntary surveys**: conducted through GitHub Discussions only. Participation
  is opt-in per discussion thread. No PII collected beyond what GitHub exposes.

## Reporting privacy concerns

File an issue at the kit's GitHub tracker tagged `privacy`. Maintainers will
respond within 7 business days.

## Change history

Amendments to this policy go through the CR process (`docs/sdlc/06_maintenance/change_requests.md`).
Any CR that adds an outbound network request MUST update this file in the same
commit, or it fails the PR check.

- 2026-04-23 — Initial draft.
