# Module 2: AI Requirement Gathering, BRD/FRD Schemas & Scoping

## 1. Fundamentals & Enterprise Frameworks
Requirements engineering translates business goals into functional and non-functional specifications.

```
+-------------------------------------------------------------------------------------------------+
|                                    Requirements Hierarchy                                       |
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                                  Business Requirements                                  |   |
|   |   - Strategic goals (e.g., reduce customer churn by 10% in Q3)                           |   |
|   +---------------------------------------+-------------------------------------------------+   |
|                                           |                                                     |
|                                           v (User Actions)                                      |
|   +---------------------------------------+-------------------------------------------------+   |
|   |                                    User Requirements                                    |   |
|   |   - User actions and scenarios (e.g., search medical guidelines using natural queries)  |   |
|   +-------------------+-------------------------------------------------+-------------------+   |
|                       |                                                 |                       |
|                       v (System Functions)                              v (System Constraints)  |
|   +-------------------+---------------------+     +---------------------+-------------------+   |
|   |             Functional Requirements     |     |           Non-Functional Requirements   |   |
|   |   - System tasks (e.g., return page     |     |   - System constraints (e.g., sub-2     |   |
|   |     citations for search results)       |     |     second latency, HIPAA compliance)   |   |
|   +-----------------------------------------+     +-----------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

### Requirements Matrix
*   **Business Requirements (BRD)**: Strategic goals (e.g., reduce customer churn by 10%).
*   **Functional Requirements (FRD)**: System tasks (e.g., return page citations for search results).
*   **Non-Functional Requirements (NFR)**: System constraints (e.g., latency, throughput, compliance).

---

## 2. Consulting Methodologies & Prioritization
*   **Prioritization Framework (MoSCoW)**:
    *   **Must Have**: Critical requirements (e.g., SSO authentication).
    *   **Should Have**: Important but not critical requirements (e.g., chat history exports).
    *   **Could Have**: Nice-to-have features (e.g., custom UI themes).
    *   **Won't Have**: Out of scope for the current release.

---

## 3. Workshop Templates & Deliverables

### Business Requirements Document (BRD) Template
*   **Objective**: Outline project goals and scope.
*   **Target KPIs**: Define metrics to track success.
*   **Functional Scope**: List required system capabilities.
*   **Non-Functional Scope**: Define latency, scale, and security constraints.

---

## 4. Discovery Questions
*   "What are the target SLAs for response times?" (Defines latency NFRs).
*   "What volume of concurrent queries must the system support?" (Defines throughput NFRs).
*   "What data governance or retention rules apply?" (Defines compliance NFRs).

---

## 5. Stakeholder Conversations
*   **User Interview**: "Describe the steps you take when a query fails. What information do you need to resolve it?"
*   **Technical Stakeholder Meeting**: "We need to document the API rate limits and authentication protocols for the target database."

---

## 6. Success Metrics & Risk Management
*   **Success Metrics**: A signed BRD/FRD, a prioritized requirements matrix, and defined acceptance criteria.
*   **Risk**: Scope creep due to poorly defined requirements. Mitigate by enforcing strict change-control processes.

---

## 7. Real Case Studies & Mistakes

### Case Study: RAG Platform Requirements at HSBC
HSBC gathered requirements to deploy an enterprise RAG platform. By defining functional constraints (document citations) and non-functional requirements (HIPAA compliance, sub-2 second response latency), they mapped specifications to guide development.

### Common Mistakes
*   Failing to define non-functional requirements (like latency and throughput limits) early.
*   Allowing scope creep by not defining boundaries in the BRD.

---

## 8. FDE Interview Questions
*   **Q**: "How do you manage a client request for a new feature that is not in the approved BRD?"
*   **Answer**: "Acknowledge the value of the new feature. Document it as a potential update, evaluate its impact on project scope and timelines, and present the trade-offs to the steering committee for review."

---

## 9. AI FDE Perspective
As an AI Forward Deployed Engineer (FDE), you document requirements:
*   Ensure latency budgets are aligned across components.
*   Verify that model response latency meets target SLAs:
    ```python
    # Latency check wrapper
    # start_time = time.time()
    # response = model.predict(query)
    # latency = time.time() - start_time
    ```
Ensure performance benchmarks are defined in the requirements.
