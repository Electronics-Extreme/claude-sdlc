# Stakeholders

| ID    | Role               | Name     | Interest / Concern                      | Influence | Sign-off? |
|-------|--------------------|----------|-----------------------------------------|-----------|-----------|
| SH-01 | Product Owner      | {{...}}  | Feature scope, ROI                      | High      | Yes       |
| SH-02 | End User           | {{...}}  | Usability, task efficiency              | Medium    | No        |
| SH-03 | Tech Lead          | {{...}}  | Feasibility, maintainability            | High      | Yes       |
| SH-04 | QA Lead            | {{...}}  | Testability, quality gates              | High      | Yes       |
| SH-05 | Security Officer   | {{...}}  | Compliance, data protection             | High      | Yes       |
| SH-06 | Operations / SRE   | {{...}}  | Deployability, observability            | Medium    | Yes       |
| SH-07 | Legal / Compliance | {{...}}  | Regulatory fit                          | Medium    | Conditional |

## User Classes

### UC-01 — {{Primary user type}}
- **Volume**: {{expected count}}
- **Technical skill**: {{low / medium / high}}
- **Primary goals**: {{...}}
- **Pain points today**: {{...}}

### UC-02 — {{Admin / operator}}
- **Volume**: {{...}}
- **Primary goals**: {{...}}

## RACI (high-level)

| Activity              | Responsible | Accountable | Consulted   | Informed |
|-----------------------|-------------|-------------|-------------|----------|
| Requirements sign-off | Tech Lead   | Product Owner | QA, Security | All    |
| Design sign-off       | Architect   | Tech Lead   | QA, Security | PO     |
| Release sign-off      | SRE         | Tech Lead   | QA, PO      | All      |
