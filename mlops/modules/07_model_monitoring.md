# Module 7: Model Monitoring & Drift Detection

## 1. Architecture Deep Dive

Model Monitoring is the practice of tracking the performance, reliability, and data distributions of machine learning models running in production. It identifies degradation before it impacts business outcomes.

```
+-------------------------------------------------------------------------------------------------+
|                                     Model Inference Pods                                        |
|    - Serve predictions. Log inputs, predictions, and metadata as payload JSON streams          |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v (JSON Stream / Kafka Event)
+-----------------------------------------------+-------------------------------------------------+
|                                        Data Logging Pipeline                                    |
|    - Collects inference payloads and logs them to a database or object storage                 |
+---------------------------------------+-------------------------------------------------+-------+
                                        |                                                 |
                                        v (Scrape / Fetch Targets)                        v (Batch Analysis)
+---------------------------------------+-------------------------------------------------+-------+
|                            Evidently AI / WhyLabs                                       |       |
|    - Compares production payload distributions against baseline training data           |       |
|    - Computes data drift and concept drift statistical metrics                          |       |
+---------------------------------------+-------------------------------------------------+       |
                                        |                                                         |
                                        v (Metrics Export: Prometheus format)                     v
+---------------------------------------+---------------------------------------------------------+
|                                    Prometheus / Grafana                                         |
|    - Prometheus: Scrapes and stores time-series metric statistics                               |
|    - Grafana: Renders real-time dashboards and fires alerts to PagerDuty/Slack                  |
+-------------------------------------------------------------------------------------------------+
```

### Types of Drift
*   **Data Drift**: A shift in the statistical distribution of model input features (e.g., a change in customer age profiles or location distributions).
*   **Concept Drift**: A shift in the relationship between input features and target labels (e.g., customer behavior changing during a global event, rendering previous predictions invalid).

---

## 2. Internal Working

### Statistical Drift Test Algorithms
*   **Kolmogorov-Smirnov (KS) Test**: Used for numerical features. It computes a p-value by comparing the cumulative distribution functions of baseline and target datasets. If p-value < 0.05, drift is assumed.
*   **Population Stability Index (PSI)**: Used to measure changes in categorical feature distributions over time. A PSI value > 0.2 indicates significant distribution shift.
*   **Wasserstein Distance (Earth Mover's Distance)**: Measures the distance between two probability distributions.

---

## 3. Production Use Cases

### Real-Time Financial Fraud Monitoring
Tracking inference inputs and prediction latency. If features like "transaction amount" deviate from the baseline distribution or if latency exceeds 50ms, the system triggers alerts.

### Predictive Model Performance Audits
Comparing live inputs against training baselines to detect feature drift, allowing teams to plan automated model retraining schedules.

---

## 4. Governance Considerations

### Regulatory Compliance & Audit Logs
In regulated industries (such as banking or healthcare), organizations must document model performance audits.
*   **Performance Audits**: Run regular drift checks (using tools like Evidently AI) and export the reports as PDFs to document model health and compliance.

---

## 5. Security Best Practices

### Restricting Access to Metrics Endpoints
*   Do not expose metrics endpoints (`/metrics`) to the public internet. Use network policies to restrict access to the Prometheus server.
*   Use HTTPS and basic authentication for all monitoring dashboards.

---

## 6. Scalability Patterns

### Distributed Logging using Kafka
Under high-volume request loads (e.g., millions of predictions per day), logging payloads synchronously can slow down inference.
*   Route prediction payloads asynchronously to a **Kafka** topic.
*   Use a consumer pool to parse payloads and write them to cold storage (such as Parquet on S3) for batch drift analysis.

---

## 7. Reliability Patterns

### Alert Threshold Tuning (Avoiding Alert Fatigue)
Avoid setting alert thresholds too low. A single anomalous request should not trigger a pager alert. Use sliding-window averages to evaluate drift before triggering warnings.

---

## 8. Cost Optimization

### Downsampling Metrics Retention
Raw payload logs can consume large volumes of storage.
*   Configure storage lifecycle rules to downsample and retain raw logs for only 14 days, while keeping aggregated metric statistics in Prometheus for longer periods.

---

## 9. Hands-On Labs

### Lab 9.1: Installing Prometheus and Grafana on Ubuntu
Run these commands to configure Prometheus and Grafana locally.
```bash
# 1. Install Prometheus
sudo apt-get update
sudo apt-get install -y prometheus

# 2. Add Grafana GPG key and repository
sudo apt-get install -y apt-transport-https software-properties-common wget
wget -q -O - https://packages.grafana.com/gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/grafana.key > /dev/null
echo "deb [signed-by=/usr/share/keyrings/grafana.key] https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

# 3. Install and start Grafana
sudo apt-get update
sudo apt-get install -y grafana
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

### Lab 9.2: Running Drift Detection in Python using Evidently AI
Write a Python script to compare baseline and production datasets and detect data drift.
```python
# /tmp/drift_monitor.py
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# 1. Generate baseline (training) and production datasets
X, y = make_classification(n_samples=1000, n_features=5, random_state=42)
baseline_df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(5)])

# Introduce artificial data drift in the production dataset
X_prod, _ = make_classification(n_samples=500, n_features=5, random_state=24)
prod_df = pd.DataFrame(X_prod, columns=[f"feature_{i}" for i in range(5)])
prod_df["feature_0"] = prod_df["feature_0"] + 2.5 # Shift distribution

# 2. Configure and run the Evidently AI Drift Report
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=baseline_df, current_data=prod_df)

# 3. Save report output as HTML
report.save_html("/tmp/data_drift_report.html")
print("Data drift report generated: /tmp/data_drift_report.html")
```
Run the monitoring check:
```bash
pip install evidently pandas scikit-learn
python3 /tmp/drift_monitor.py
```

---

## 10. Troubleshooting Scenarios

### Task 10.1: Prometheus Fails to Scrape Endpoints
*   **Symptom**: Prometheus target page displays status `DOWN` or `Connection refused` for target endpoints.
*   **Root Cause**: The application metrics port is blocked by firewall rules, or the `/metrics` path is incorrect.
*   **Resolution Strategy**:
    *   Verify the metrics endpoint is reachable locally:
        ```bash
        curl http://localhost:8000/metrics
        ```
    *   Check `/etc/prometheus/prometheus.yml` configuration mappings:
        ```yaml
        # Ensure static config mappings match
        static_configs:
          - targets: ['localhost:8000']
        ```

### Task 10.2: Statistical Test Fails due to Small Sample Size
*   **Symptom**: Evidently AI throws a warning: `ValueError: Not enough data points to compute metric`.
*   **Root Cause**: The window size of the production dataset is too small to execute statistical tests (like the KS-test).
*   **Resolution Strategy**:
    *   Increase the sliding window size in the logging pipeline to gather sufficient samples before executing drift checks.

---

## 11. Real Production Incidents

### Case Study: False Drift Alerts during Holiday Season
*   **Incident**: An e-commerce recommendation model started triggering high-priority data drift alerts on Black Friday. The customer purchase values shifted significantly compared to baseline training data, triggering alerts. The model was working correctly, but the alerts woke up engineers, causing alert fatigue.
*   **Remediation**:
    *   Tuned alert thresholds and increased the evaluation window size.
    *   Configured separate baseline datasets for holiday seasons to prevent false positives.

---

## 12. Interview Questions

### Q1: What is the difference between Data Drift and Concept Drift?
*   **Answer**:
    *   **Data Drift**: A shift in the statistical distribution of model input features (e.g., changes in customer profiles).
    *   **Concept Drift**: A shift in the relationship between input features and target labels (e.g., changes in customer behavior rendering previous predictions invalid).

### Q2: How does the Population Stability Index (PSI) measure drift?
*   **Answer**: PSI measures the change in categorical feature distributions over time. A PSI value > 0.2 indicates significant distribution shift.

### Q3: Why is it bad practice to log prediction metrics synchronously?
*   **Answer**: Synchronous logging can slow down model inference latency. Route prediction payloads asynchronously to a queue (like Kafka) instead.

### Q4: Explain the purpose of the Kolmogorov-Smirnov (KS) test.
*   **Answer**: The KS-test computes a p-value by comparing the cumulative distribution functions of baseline and target datasets to detect numerical feature drift.

### Q5: How do you prevent false positives in drift alerts during seasonal events?
*   **Answer**: Tune alert thresholds, increase the evaluation window size, and configure separate baseline datasets for seasonal events.

---

## 13. Enterprise Case Studies

### Model Monitoring at Spotify
Spotify uses automated monitoring pipelines to track the recommendations model performance. By comparing weekly prediction statistics against baseline training data, they detect distribution shifts, triggering automated retraining pipelines to maintain recommendation quality.

---

## 14. AI FDE Perspective

### Deploying Model Monitoring in Air-Gapped Networks
As an AI Forward Deployed Engineer (FDE), you often deploy MLOps infrastructure in isolated, secure networks.
*   **Local Metric Routing**: Set up local **Prometheus** and **Grafana** servers within the secure network to aggregate metrics.
*   **Offline Notifications**: If integrations with Slack or external alerting tools are blocked, configure Alertmanager to send email alerts using local SMTP servers or write alerts to system logs:
    ```yaml
    # Alertmanager config logging to file
    receivers:
    - name: 'log-alerts'
      webhook_configs:
      - url: 'http://localhost:9099/alerts'
    ```
This ensures operators are notified of anomalies without needing external network connections.
