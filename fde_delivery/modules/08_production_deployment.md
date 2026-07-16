# Module 8: Production Deployment, Go-Live Governance & Rollback Strategies

## 1. Fundamentals & Enterprise Frameworks
Production deployment manages release schedules, risk validation, and rollback strategies during rollout.

```
+-------------------------------------------------------------------------------------------------+
|                                     Deployment Pipeline                                         |
|                                                                                                 |
|   +-------------------+      +-------------------+      +-------------------+                   |
|   | 1. Readiness Check| ---> |  2. Canary Run    | ---> |  3. Full Rollout  |                   |
|   | (Verify checks)   |      | (Route 10% load)  |      | (Route 100% load) |                   |
|   +---------+---------+      +---------+---------+      +---------+---------+                   |
|             |                          |                          |                             |
|             v                          v                          v                             |
|    Verify database and        Monitor error logs         Enable access to all                   |
|    SSO health status          for performance drops      production users                       |
+-------------------------------------------------------------------------------------------------+
```

### Rollout Strategies
*   **Canary Deployment**: Route 5-10% of traffic to the new version to monitor performance before full rollout.
*   **Blue-Green Deployment**: Maintain two identical production environments (Blue and Green) to allow rapid switching and rollback.
*   **Phased Rollout**: Scale user base gradually over time (e.g., department by department).

---

## 2. Consulting Methodologies & Go-Live Reviews
*   **Go-Live Checklist**: Defining verification tasks (e.g., verifying database health and SSO status) before deployment.
*   **Rollback Strategy**: Establishing rollback procedures if error thresholds are exceeded.

---

## 3. Workshop Templates & Deliverables

### Go-Live Checklist Template
*   **Infrastructure Health**: Verify that Kubernetes node pools and databases are active.
*   **SSO Integration**: Test authentication loops with test users.
*   **Telemetry Verification**: Verify that Prometheus metrics are logging correctly.
*   **Rollback Scenarios**: Document commands to trigger rollback.

---

## 4. Discovery Questions
*   "What are the target windows for system maintenance?" (Defines deployment windows).
*   "What error rate triggers a rollback?" (Defines rollback thresholds).
*   "Who is the point of contact for database operations?" (Identifies key support contacts).

---

## 5. Stakeholder Conversations
*   **Go-Live Readiness Review**: "We have completed canary testing. System latency is stable, and error rates are under target thresholds."
*   **Incident Sync**: "The error rate exceeded limits during rollout. We have triggered the rollback plan to restore the stable version."

---

## 6. Success Metrics & Risk Management
*   **Success Metrics**: A signed deployment plan, a verified go-live checklist, and a documented rollback strategy.
*   **Risk**: Rollout failure due to configuration differences across environments. Mitigate by automating deployments using Infrastructure as Code (IaC).

---

## 7. Real Case Studies & Mistakes

### Case Study: Assistant Rollout at Allianz
Allianz deployed an internal AI assistant. By using canary deployments and verifying go-live checklists, they monitored performance and scaled access to 50,000 employees without service interruptions.

### Common Mistakes
*   Deploying changes without a validated rollback plan.
*   Running updates during peak traffic hours, increasing outage risks.

---

## 8. FDE Interview Questions
*   **Q**: "How do you rollback a Kubernetes deployment if errors increase after rollout?"
*   **Answer**: "Run the rollback command (`kubectl rollout undo deployment/ml-api-service`) to revert to the previous version and restore stable operations."

---

## 9. AI FDE Perspective
As an AI Forward Deployed Engineer (FDE), you manage deployments:
*   Document data schemas and deployment parameters early.
*   Verify Kubernetes rollout statuses during execution:
    ```bash
    # Check deployment rollout status
    # kubectl rollout status deployment/ml-api-service
    ```
Ensure performance benchmarks are aligned with system capacities.
