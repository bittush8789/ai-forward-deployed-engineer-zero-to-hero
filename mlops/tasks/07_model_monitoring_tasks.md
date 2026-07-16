# Practice Tasks: Module 7 - Evidently AI Drift Detection

This document outlines step-by-step tasks to calculate numerical data drift using Evidently AI.

---

## Task 1: Generate Data Drift Report
*   **Goal**: Compare training and production data distributions and output an HTML report.
*   **Step-by-Step Instructions**:
    1. Write a Python script `compute_drift.py`:
       ```python
       # /tmp/compute_drift.py
       import pandas as pd
       from evidently.report import Report
       from evidently.metric_preset import DataDriftPreset

       # Baseline
       ref_data = pd.DataFrame({"age": [25, 30, 45, 50, 23, 38]})
       # Shifted distribution
       curr_data = pd.DataFrame({"age": [65, 70, 80, 55, 68, 72]})

       report = Report(metrics=[DataDriftPreset()])
       report.run(reference_data=ref_data, current_data=curr_data)
       report.save_html("/tmp/drift_report.html")
       print("Data drift report generated: /tmp/drift_report.html")
       ```
       Write this file to disk:
       ```bash
       tee /tmp/compute_drift.py << 'EOF'
       import pandas as pd
       from evidently.report import Report
       from evidently.metric_preset import DataDriftPreset

       ref_data = pd.DataFrame({"age": [25, 30, 45, 50, 23, 38]})
       curr_data = pd.DataFrame({"age": [65, 70, 80, 55, 68, 72]})

       report = Report(metrics=[DataDriftPreset()])
       report.run(reference_data=ref_data, current_data=curr_data)
       report.save_html("/tmp/drift_report.html")
       print("Data drift report generated: /tmp/drift_report.html")
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/compute_drift.py
       ```
*   **Verification**:
    Verify the HTML report has been generated:
    ```bash
    ls -l /tmp/drift_report.html
    ```
