# Module 2: Prompt Versioning & Git-Integrated Registries

## 1. Theory (40%)
Treating prompts as software requires enforcing **Prompt Version Control**. This enables change tracking, rollbacks, and auditability.

```
+-------------------------------------------------------------------------------------------------+
|                                       Prompt Version Control                                    |
|                                                                                                 |
|   +-------------------+      +-------------------+      +-------------------+                   |
|   |   Version 1.0     | ---> |   Version 1.1     | ---> |   Version 2.0     |                   |
|   |   (Base Prompt)   |      |   (Lacks safety)  |      |   (Approved)      |                   |
|   +---------+---------+      +---------+---------+      +---------+---------+                   |
|             ^                          |                          ^                             |
|             |                          v                          |                             |
|             +--------------------------+--------------------------+                             |
|                        (Rollback if safety fails)                                               |
+-------------------------------------------------------------------------------------------------+
```

### Core Concepts
*   **Version Control**: Tracking changes to prompt templates over time using SemVer (Semantic Versioning) or Git commit hashes.
*   **Rollback Strategy**: The ability to quickly revert a prompt template in production to a previous stable version if the new version fails.
*   **Approval Workflows**: Enforcing peer reviews and validation checks before promoting a prompt template.

---

## 2. Architecture Deep Dive

A production-grade prompt versioning architecture combines Git with a registry:
1.  **Git Source of Truth**: Prompts are stored as files in a Git repository.
2.  **Pull Request Pipeline**: Changes are reviewed, linted, and tested via CI pipelines.
3.  **Registry Synchronization**: Once merged, the pipeline synchronizes the updated prompts to the registry (such as LangSmith or LangFuse) and tags them.

---

## 3. Tool Comparison

| Feature | Git (Flat Files) | SaaS Prompt Registry |
|---|---|---|
| **Version Tracking** | Branch/Commit-based | Version index with DB mapping |
| **Audit Log** | Native `git log` | User audit logs |
| **Rollback Time** | Code deploy time (Slow) | API configuration shift (Sub-second) |
| **Testing Integration**| CI pipelines | UI playgrounds & automated test runs |

---

## 4. Tool Installation
Ensure Git and client SDKs are available:
```bash
sudo apt-get install -y git
pip install langfuse
```

---

## 5. Tool Setup
Configure your Git repository layout for prompts:
```bash
mkdir -p prompts-repo/prompts
cd prompts-repo
git init
```

---

## 6. CLI Commands
```bash
# Register changes in Git
git add prompts/
git commit -m "feat: update system instructions for safety rules"
git tag -a "v1.2.0" -m "Safety patch release"
```

---

## 7. Configuration Files
Define prompt version metadata in `prompts/classification_v2.json`:
```json
{
  "name": "classification_prompt",
  "version": "1.2.0",
  "tags": ["production"],
  "template": "Classify the following query: {user_query}. Categories: [Sales, TechSupport, General]."
}
```

---

## 8. API Examples
Retrieve prompts based on tags:
```python
# /tmp/prompt_versioning.py
import json

def get_production_prompt():
    # Simulating fetching the latest production-tagged prompt file
    path = "/tmp/classification_v2.json"
    with open(path, "r") as f:
        data = json.load(f)
    print(f"Loaded Prompt Name: {data['name']}")
    print(f"Active Version: {data['version']}")
    print(f"Template: {data['template']}")

if __name__ == '__main__':
    # Write mock file
    mock_data = {
      "name": "classification_prompt",
      "version": "1.2.0",
      "template": "Classify: {user_query}"
    }
    with open("/tmp/classification_v2.json", "w") as f:
        json.dump(mock_data, f)
        
    get_production_prompt()
```
Run verification:
```bash
python3 /tmp/prompt_versioning.py
```

---

## 9. Production Tasks

### Configuring Fallback Rollbacks
Configure your application deployment files to automatically default to a hardcoded local template if remote registry calls fail or time out.

---

## 10. Troubleshooting

### Task 10.1: Version Out of Sync
*   **Symptom**: The application retrieves version `1.1.0` even though version `1.2.0` was merged to Git.
*   **Root Cause**: The CD synchronization pipeline failed to run or the registry tag was not updated.
*   **Resolution Strategy**:
    *   Verify the sync pipeline execution logs in GitHub Actions.
    *   Manually push the tag update using the registry CLI:
        ```bash
        # Force registry synchronization
        ```

---

## 11. Monitoring
Configure alerts in Grafana when the age of the production prompt template in the registry exceeds 90 days without updates, to identify stale configurations.

---

## 12. Security
Restrict merge access to the prompt repository main branch using branch protection rules, requiring approvals from senior platform engineers.

---

## 13. Governance
Log the user, timestamp, and ticket ID associated with every prompt version change in the commit history to maintain a clear audit trail.

---

## 14. Real Enterprise Incidents

### Case Study: Untested Prompt Causing Model Failures
*   **Incident**: A developer updated a classification prompt to improve accuracy. The new version changed the output format, returning JSON instead of a plain string. The application parser crashed on the new output, causing downstream services to fail.
*   **Remediation**:
    *   Enforced schema validation checks on prompt outputs.
    *   Configured automated validation suites to test prompt updates before merging.

---

## 15. Interview Questions

### Q1: Why is Git-integrated prompt versioning preferred over manually modifying templates in a UI?
*   **Answer**: Git-integrated versioning ensures that prompt changes are reviewed, audited, and tested through standard CI/CD pipelines before deployment, preventing untested modifications from reaching production.

### Q2: Explain a rollback strategy for prompt templates.
*   **Answer**: Use environment tags (like `production`). If a new version fails, update the tag in the registry database to point to the previous stable version, reverting the change in sub-seconds without redeploying code.

---

## 16. Enterprise Case Studies

### Prompt Governance at Stripe
Stripe uses a Git-backed prompt registry to manage AI agents. By running regression tests on prompt updates and using manual approvals for production promotions, they prevent output format changes from breaking downstream parser configurations.
