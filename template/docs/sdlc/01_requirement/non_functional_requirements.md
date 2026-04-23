# Non-Functional Requirements (NFRs)

Every NFR has a **measurable target** and a **verification method**. If you can't measure it, rewrite it.

## Categories

### Performance

| ID         | Requirement                                                   | Target          | Verification     |
|------------|---------------------------------------------------------------|-----------------|------------------|
| NFR-PRF-01 | 95th percentile API latency under nominal load                | ≤ 200 ms        | Load test        |
| NFR-PRF-02 | System supports concurrent users                              | ≥ 1,000         | Load test        |
| NFR-PRF-03 | Page first contentful paint                                   | ≤ 1.5 s (p75)   | Lighthouse CI    |

### Availability & Reliability

| ID         | Requirement                         | Target         | Verification       |
|------------|-------------------------------------|----------------|--------------------|
| NFR-AVL-01 | Monthly uptime                      | ≥ 99.9%        | Monitoring report  |
| NFR-AVL-02 | RPO (data loss window)              | ≤ 5 minutes    | Backup test        |
| NFR-AVL-03 | RTO (recovery time)                 | ≤ 30 minutes   | DR drill           |

### Security

| ID         | Requirement                                                       | Target                  | Verification    |
|------------|-------------------------------------------------------------------|-------------------------|-----------------|
| NFR-SEC-01 | All data in transit encrypted                                     | TLS 1.2+                | Scan            |
| NFR-SEC-02 | Passwords stored hashed with per-user salt                        | Argon2id / bcrypt ≥ 12  | Code review     |
| NFR-SEC-03 | Authenticate before any sensitive op                              | 100% endpoints          | Pen test        |
| NFR-SEC-04 | Third-party dependencies scanned                                  | 0 critical CVEs         | CI gate         |

### Usability & Accessibility

| ID         | Requirement                         | Target               | Verification     |
|------------|-------------------------------------|----------------------|------------------|
| NFR-USA-01 | Core flows WCAG compliance          | 2.2 AA               | Axe audit        |
| NFR-USA-02 | Keyboard-only navigation            | All critical flows   | Manual test      |

### Maintainability

| ID         | Requirement                         | Target               | Verification     |
|------------|-------------------------------------|----------------------|------------------|
| NFR-MNT-01 | Unit test coverage for core modules | ≥ 80% lines          | Coverage report  |
| NFR-MNT-02 | Build reproducible from source      | Deterministic hash   | CI               |

### Compliance / Legal

| ID         | Requirement                         | Target               | Verification     |
|------------|-------------------------------------|----------------------|------------------|
| NFR-CMP-01 | {{e.g. GDPR / HIPAA / PCI-DSS}}     | {{scope}}            | Audit            |

### Observability

| ID         | Requirement                                         | Target                 | Verification |
|------------|-----------------------------------------------------|------------------------|--------------|
| NFR-OBS-01 | Structured logs for every request                   | 100% endpoints         | Log review   |
| NFR-OBS-02 | Metrics: request rate, error rate, latency, saturation | Exposed via Prometheus | Dashboard    |
