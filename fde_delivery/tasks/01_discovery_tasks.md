# Practice Tasks: Module 1 - Discovery Workshop Checklists

This document outlines step-by-step tasks to configure discovery workshop agendas and questionnaires.

---

## Task 1: Create Discovery Questionnaire
*   **Goal**: Create a structured JSON questionnaire defining discovery targets.
*   **Step-by-Step Instructions**:
    1. Create a questionnaire file `discovery_q.json` in `/tmp/`:
       ```json
       # /tmp/discovery_q.json
       {
         "workshop_goals": [
           "Identify current manual bottlenecks",
           "Define target success KPIs",
           "Map data source locations"
         ],
         "questions": [
           "What is the average time to process a document?",
           "What file formats are used to store data?",
           "What compliance or security guidelines apply?"
         ]
       }
       ```
       Write this file to disk:
       ```bash
       tee /tmp/discovery_q.json << 'EOF'
       {
         "workshop_goals": [
           "Identify current manual bottlenecks",
           "Define target success KPIs",
           "Map data source locations"
         ],
         "questions": [
           "What is the average time to process a document?",
           "What file formats are used to store data?",
           "What compliance or security guidelines apply?"
         ]
       }
       EOF
       ```
    2. Write a Python script to parse the questionnaire:
       ```python
       # /tmp/parse_discovery.py
       import json
       import sys

       def verify_questions():
           with open("/tmp/discovery_q.json", "r") as f:
               data = json.load(f)
           
           print("Workshop Objectives:")
           for goal in data["workshop_goals"]:
               print(f"- {goal}")
           print("\nTarget Questionnaire:")
           for q in data["questions"]:
               print(f"- {q}")
           sys.exit(0)

       if __name__ == '__main__':
           verify_questions()
       ```
       Write this script:
       ```bash
       tee /tmp/parse_discovery.py << 'EOF'
       import json
       import sys

       def verify_questions():
           with open("/tmp/discovery_q.json", "r") as f:
               data = json.load(f)
           
           print("Workshop Objectives:")
           for goal in data["workshop_goals"]:
               print(f"- {goal}")
           print("\nTarget Questionnaire:")
           for q in data["questions"]:
               print(f"- {q}")
           sys.exit(0)
       EOF
       ```
    3. Run the script:
       ```bash
       python3 /tmp/parse_discovery.py
       ```
*   **Verification**:
    Verify the script exit status is 0:
    ```bash
    python3 /tmp/parse_discovery.py && echo "Discovery questionnaire validated."
    ```
