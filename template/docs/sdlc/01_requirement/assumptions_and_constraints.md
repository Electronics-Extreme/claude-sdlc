# Assumptions & Constraints

Capture what you're *taking for granted* and what *limits you*. These are the hidden forces behind every decision downstream.

## Assumptions

Things believed true without proof. If any turn out false, re-open requirements.

| ID    | Assumption                                              | Impact if wrong                    | Owner    |
|-------|---------------------------------------------------------|-------------------------------------|----------|
| AS-01 | {{Users have stable broadband}}                         | {{Offline mode becomes mandatory}} | {{...}}  |
| AS-02 | {{Third-party payment gateway remains available}}       | {{Need fallback provider}}         | {{...}}  |
| AS-03 | {{Data volume grows ≤ 10% monthly}}                     | {{Scale-out plan needed sooner}}   | {{...}}  |

## Constraints

Non-negotiable limits: budget, time, tech, regulatory, organizational.

| ID    | Type         | Constraint                                              | Source       |
|-------|--------------|---------------------------------------------------------|--------------|
| CN-01 | Budget       | {{Cloud spend ≤ $X/month}}                              | Finance      |
| CN-02 | Schedule     | {{GA by YYYY-MM-DD}}                                    | Product      |
| CN-03 | Technology   | {{Must run on existing K8s cluster}}                    | Platform     |
| CN-04 | Regulatory   | {{Data must reside in {{region}}}}                      | Legal        |
| CN-05 | Organizational | {{No new vendor contracts this FY}}                   | Procurement  |

## Dependencies (external)

| ID    | Depends on                         | Criticality | Contact   | Fallback        |
|-------|------------------------------------|-------------|-----------|-----------------|
| DP-01 | {{Auth provider X}}                | High        | {{...}}   | {{...}}         |
| DP-02 | {{Internal team Y API}}            | Medium      | {{...}}   | {{...}}         |
