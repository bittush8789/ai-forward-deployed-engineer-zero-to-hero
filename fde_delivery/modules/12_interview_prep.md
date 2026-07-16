# Module 12: Scenario-Based AI FDE Interview Preparation

This module compiles scenario-based questions and model answers for AI Forward Deployed Engineer (FDE) interviews.

---

## 1. Discovery & Requirement Workshops

### Q1: How do you handle a business lead who demands a feature that IT opposes due to security rules?
*   **Answer**: "Acknowledge both perspectives: the business lead's focus on speed and the IT lead's focus on compliance. Set up a review meeting to discuss the feature's data access needs, explore secure alternative approaches (e.g., API authentication, data masking), and help the teams reach a compromise."

### Q2: What criteria do you use to prioritize AI opportunities during discovery?
*   **Answer**: "Evaluate use cases using a prioritization matrix based on two axes: Technical Feasibility (data availability, model readiness) and Business Value (time saved, revenue growth, cost reduction). Prioritize quick wins (high value, high feasibility) first."

---

## 2. Technical Consulting & Solution Design

### Q1: How do you explain the trade-offs of build vs buy for an LLM deployment?
*   **Answer**: "Analyze the trade-offs: building offers maximum customization and data control but carries high upfront costs and long timelines, while buying provides faster time-to-market and lower initial costs but limited customization. Recommend a hybrid approach (using commercial APIs with custom vector databases) to balance speed and customization."

### Q2: How do you design a RAG system to enforce document access controls?
*   **Answer**: "Integrate the RAG microservice with the client's identity provider (e.g., Active Directory, Keycloak). Extract the user's access roles from the token, and append those role filters directly to the vector search queries to ensure users only retrieve authorized documents."

---

## 3. PoC & Enterprise Integrations

### Q1: What are the risks of using mock APIs during the PoC phase, and how do you mitigate them?
*   **Answer**: "The primary risk is that mock APIs mask connection, latency, or schema mismatch issues that occur during production integration. Mitigate this by validating actual API schemas early, and scheduling integrations as soon as the core feasibility is verified."

---

## 4. Rollout & Customer Success

### Q1: How do you handle low user adoption of a newly deployed AI tool?
*   **Answer**: "Review usage logs and survey users to identify issues (usability problems, lack of training, resistance). Address usability issues with developers, schedule additional training sessions, and partner with change champions to support the transition."

### Q2: What metrics do you present during a Quarterly Business Review (QBR)?
*   **Answer**: "Focus on business outcomes and ROI: reduction in task cycle times, operational cost savings, accuracy improvements, and active usage statistics (MAU). Keep technical model metrics secondary."
