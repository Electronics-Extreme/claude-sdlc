---
doc: skill/references/required-reads.md
status: signed
signed_by: AI Project Setup v2.0.0 on 2026-04-23
required_for: [phase-1-artifact-authoring, phase-2-artifact-authoring, phase-3-slice, phase-3-refactor, phase-4-test-authoring, phase-4-test-execution, phase-5-deploy-prep, phase-5-release-cutting, phase-6-CR-authoring, phase-6-CR-implementation, phase-6-incident-response, phase-6-routine-maintenance]
cite_as: RR
---

# Required reads per task-type

Canonical manifest referenced by Core rule 1.
Task-type names are validated against `config/task-types.yaml`.

**Rule**: when working on a task-type listed here, load EVERY file in
`must_read` — not a subset, not a judgment call. State which docs authorized
the change in your opening message using the `must_cite_in_opening` template.

```yaml
reads:
  phase-1-artifact-authoring:
    must_read:
      - docs/sdlc/01_requirement/stakeholders.md           # who needs what
      - docs/sdlc/01_requirement/glossary.md               # domain terms
      - docs/sdlc/01_requirement/assumptions_and_constraints.md
      - docs/sdlc/01_requirement/srs.md                    # existing scope
      - docs/sdlc/01_requirement/functional_requirements.md
      - docs/sdlc/01_requirement/non_functional_requirements.md
      - docs/sdlc/01_requirement/use_cases.md
      - docs/sdlc/01_requirement/acceptance_criteria.md
    must_cite_in_opening:
      - "docs/sdlc/01_requirement/<file>.md §<section> — <name of FR/NFR/UC>"
      - "Linked to: <stakeholder / goal>"

  phase-2-artifact-authoring:
    must_read:
      - docs/sdlc/01_requirement/functional_requirements.md     # WHAT authorizing HOW
      - docs/sdlc/01_requirement/non_functional_requirements.md
      - docs/sdlc/01_requirement/acceptance_criteria.md
      - docs/sdlc/02_design/architecture.md
      - docs/sdlc/02_design/data_model.md
      - docs/sdlc/02_design/api_design.md
      - docs/sdlc/02_design/trade_offs.md
    must_cite_in_opening:
      - "docs/sdlc/01_requirement/<file>.md §<section> — <FR/NFR satisfied>"
      - "docs/sdlc/02_design/<file>.md §<section> — <design element>"

  phase-3-slice:
    must_read:
      - docs/sdlc/01_requirement/functional_requirements.md     # FR-### authorizing slice
      - docs/sdlc/01_requirement/acceptance_criteria.md         # AC-### to satisfy
      - docs/sdlc/02_design/architecture.md                      # module context
      - docs/sdlc/02_design/api_design.md                        # if touching endpoints
      - docs/sdlc/02_design/data_model.md                        # if touching persistence
      - docs/sdlc/03_implementation/coding_standards.md         # ALWAYS — style, naming, errors
      - docs/sdlc/03_implementation/module_breakdown.md         # file-to-doc authoritative map
      - docs/sdlc/04_testing/test_cases.md                       # TC-### to author/update
    must_cite_in_opening:
      - "docs/sdlc/01_requirement/<file>.md §<section> — <FR authorizing slice>"
      - "docs/sdlc/02_design/<file>.md §<section> — <design section>"
      - "docs/sdlc/03_implementation/coding_standards.md §<section>"
      - "docs/sdlc/03_implementation/module_breakdown.md → <file path>"
      - "Slice: <one-sentence scope>"

  phase-3-refactor:
    must_read:
      - docs/sdlc/01_requirement/acceptance_criteria.md
      - docs/sdlc/02_design/architecture.md
      - docs/sdlc/03_implementation/coding_standards.md
      - docs/sdlc/03_implementation/module_breakdown.md
      - docs/sdlc/03_implementation/code_review_checklist.md    # what "quality" means here
    must_cite_in_opening:
      - "Refactor of <module> with no behavior change"
      - "docs/sdlc/03_implementation/coding_standards.md §<section> — improvements applied"
      - "AC-### still satisfied: <how>"

  phase-4-test-authoring:
    must_read:
      - docs/sdlc/01_requirement/functional_requirements.md
      - docs/sdlc/01_requirement/acceptance_criteria.md         # AC-### source for TC-###
      - docs/sdlc/04_testing/test_plan.md                        # strategy
      - docs/sdlc/04_testing/test_cases.md                       # existing TCs
      - docs/sdlc/04_testing/test_data.md                        # fixtures
    must_cite_in_opening:
      - "AC-### → TC-### being authored"
      - "docs/sdlc/04_testing/test_plan.md §<section>"

  phase-4-test-execution:
    must_read:
      - docs/sdlc/04_testing/test_plan.md
      - docs/sdlc/04_testing/test_cases.md
      - docs/sdlc/04_testing/test_report.md
      - docs/sdlc/04_testing/defect_log.md
    must_cite_in_opening:
      - "Running suite per docs/sdlc/04_testing/test_plan.md §<section>"

  phase-5-deploy-prep:
    must_read:
      - docs/sdlc/05_deployment/deployment_plan.md
      - docs/sdlc/05_deployment/rollback_plan.md
      - docs/sdlc/05_deployment/runbook.md
      - docs/sdlc/05_deployment/smoke_tests.md
      - docs/sdlc/05_deployment/go_live_checklist.md
      - docs/sdlc/05_deployment/release_notes.md               # adopter project; NOT kit CHANGELOG
    must_cite_in_opening:
      - "docs/sdlc/05_deployment/<file>.md §<section> — <change>"

  phase-5-release-cutting:
    must_read:
      - docs/VERSIONING.md                           # kit-only; adopters adapt
      - CHANGELOG.md                                  # kit-only
      - docs/sdlc/05_deployment/release_notes.md                # adopter-project
    must_cite_in_opening:
      - "Bumping <current> → <new> per docs/VERSIONING.md"
      - "CHANGELOG [Unreleased] section audited"

  phase-6-CR-authoring:
    must_read:
      - docs/sdlc/06_maintenance/change_requests.md             # template + prior CRs
      - docs/sdlc/06_maintenance/maintenance_plan.md
    must_cite_in_opening:
      - "Drafting CR-<YYYY>-<NNN>: <title>"
      - "Class: <minor | major | breaking>"

  phase-6-CR-implementation:
    must_read:
      - docs/sdlc/06_maintenance/change_requests.md             # CR to implement
      - docs/VERSIONING.md                            # classification rubric
      - (CR's affected requirement/design/implementation docs)
    must_cite_in_opening:
      - "Implementing CR-<ID> — signed <date> by <approvers>"
      - "Affected docs: <list from CR §Affected>"

  phase-6-incident-response:
    must_read:
      - docs/sdlc/06_maintenance/incident_log.md
      - docs/sdlc/05_deployment/runbook.md
      - docs/sdlc/06_maintenance/monitoring.md
      - docs/sdlc/06_maintenance/sla_and_slo.md
    must_cite_in_opening:
      - "Incident: <one-line description>"
      - "SLO affected: <NFR-###>"
      - "Following protocols/hotfix.md"

  phase-6-routine-maintenance:
    must_read:
      - docs/sdlc/06_maintenance/maintenance_plan.md
      - docs/sdlc/06_maintenance/monitoring.md
      - docs/sdlc/06_maintenance/eol_policy.md
    must_cite_in_opening:
      - "Routine task: <type>"
```

## What "MUST" means here

Failure to load a listed file before starting = Core rule 1 violation = refused.

If a task truly needs a file not listed, that's a signal to amend this manifest
(via a CR) rather than silently expand the read set.
