# Post-Deploy Smoke Tests

Run these after every production deployment. If any fails → rollback.

## Automated Checks (must all pass)

| ID        | Check                                        | How                           | Pass criterion         |
|-----------|----------------------------------------------|-------------------------------|------------------------|
| SM-01     | Health endpoint                              | `GET /healthz`                | 200, `ok: true`        |
| SM-02     | Version endpoint matches deployed tag        | `GET /version`                | equals deploy tag      |
| SM-03     | DB connectivity                              | health endpoint deep check    | reports db `up`        |
| SM-04     | Cache connectivity                           | health endpoint deep check    | reports cache `up`     |
| SM-05     | Auth — valid token accepted                  | signed synthetic request      | 200                    |
| SM-06     | Auth — invalid token rejected                | bad token request             | 401                    |
| SM-07     | Signup flow (read-only synthetic)            | contract test                 | 201 on synthetic path  |
| SM-08     | Critical external dependency reachable       | {{...}}                       | reachable              |

## Manual Eyeball (within 15 min)

- [ ] Open production URL in a browser — loads, no console errors
- [ ] Log in as test account — reaches dashboard
- [ ] Check top dashboards — no new anomalies
- [ ] Check alerts — none firing

## Automation

- Lives in `tests/smoke/` and runs from the deployment pipeline.
- On failure → aborts promotion, pages on-call, kicks off rollback per `rollback_plan.md`.
