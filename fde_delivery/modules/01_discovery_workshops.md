# Module 1: AI FDE Discovery Workshops & Alignment Frameworks

## 1. Fundamentals & Enterprise Frameworks
Discovery workshops assess the client's current operations, align stakeholders on a shared future state, and identify high-value AI opportunities.

```
+-------------------------------------------------------------------------------------------------+
|                                    Discovery Workshop Flow                                      |
|                                                                                                 |
|   +-------------------+      +-------------------+      +-------------------+                   |
|   | 1. Current State  | ---> |  2. Future State  | ---> |  3. AI Scoping    |                   |
|   |   (As-Is flow)    |      |   (To-Be flow)    |      | (Feasibility/ROI) |                   |
|   +---------+---------+      +---------+---------+      +---------+---------+                   |
|             |                          |                          |                             |
|             v                          v                          v                             |
|    Map current manual         Design streamlined         Prioritize use cases                   |
|    process bottlenecks        workflows with AI          on value matrix                        |
+-------------------------------------------------------------------------------------------------+
```

### Discovery Methodologies
*   **As-Is Process Mapping**: Documenting step-by-step manual workflows and identifying bottlenecks.
*   **To-Be Design**: Designing streamlined workflows that incorporate AI capabilities.
*   **Use Case Prioritization**: Evaluating identified use cases based on technical feasibility and business value to determine priorities.

---

## 2. Consulting Methodologies & Communication
*   **Executive Alignment**: Aligning sponsors on project goals, metrics, and resource requirements.
*   **User Discovery**: Conducting interviews with front-line users to understand their daily operational challenges.

---

## 3. Workshop Templates & Deliverables

### Discovery Workshop Agenda Template
*   **09:00 - 09:30**: Executive Alignment (Project goals, scope, and KPIs).
*   **09:30 - 11:30**: As-Is Process Mapping (Walk through current workflows and pain points).
*   **11:30 - 12:30**: To-Be Visioning (Brainstorming AI-powered workflows).
*   **13:30 - 15:00**: Technical Discovery (Data access, integrations, and security).
*   **15:00 - 16:30**: Use Case Prioritization & Roadmap definition.

---

## 4. Discovery Questions
*   "What manual steps in this workflow take the most time?" (Identifies automation targets).
*   "What databases or file systems contain the required data?" (Maps integration needs).
*   "What compliance or security rules restrict data access?" (Identifies governance bounds).

---

## 5. Stakeholder & Executive Conversations
*   **Executive Sponsor Meeting**: "We are here to align on the strategic metrics (e.g., cycle time reduction) that this AI solution must deliver to justify implementation."
*   **Business User Session**: "Walk me through your daily workflow. Show me where you copy-paste data or wait for approvals."

---

## 6. Success Metrics & Risk Management
*   **Success Metrics**: Clear alignment on target KPIs, a defined To-Be process map, and prioritized use cases.
*   **Risk**: Proceeding without IT or compliance representation, leading to integration issues later. Mitigate by requiring IT stakeholder attendance.

---

## 7. Real Case Studies & Mistakes

### Case Study: Insurance Claims Workshop at Zurich
Zurich Insurance conducted discovery workshops to design an AI claims assistant. By involving claims managers, IT leads, and compliance officers, they mapped the intake process, identified data access requirements, and established a roadmap, leading to a successful implementation.

### Common Mistakes
*   Failing to involve IT and security teams during discovery, leading to security objections later.
*   Focusing workshops on model metrics (accuracy, F1 score) rather than business outcomes (cycle times, cost savings).

---

## 8. FDE Interview Questions
*   **Q**: "How do you handle disagreement between the business lead and IT lead during a discovery workshop?"
*   **Answer**: "Acknowledge both perspectives: the business lead's focus on operational speed and the IT lead's focus on security. Use a prioritization matrix to evaluate options based on feasibility and business value to find a compromise."

---

## 9. AI FDE Perspective
As an AI Forward Deployed Engineer (FDE), you lead discovery workshops:
*   Document current data schemas and check API access early.
*   Verify whether the target database is accessible via API:
    ```python
    # Secure API ping script
    # requests.get("https://internal-db.corp.local/health", verify=True)
    ```
Ensure data access issues are identified early to prevent project delays.
