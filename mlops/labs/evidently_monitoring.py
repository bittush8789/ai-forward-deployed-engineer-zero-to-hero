#!/usr/bin/env python3
"""
Evidently AI Data Drift Monitor validation script.
"""

import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def main():
    # 1. Create mock baseline and production data
    baseline = pd.DataFrame({"latency": [10.2, 12.5, 14.1, 9.8, 11.5]})
    production = pd.DataFrame({"latency": [20.5, 25.1, 30.2, 18.9, 22.4]})
    
    # 2. Run evidently report
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=baseline, current_data=production)
    
    # 3. Save report as HTML
    report.save_html("/tmp/evidently_drift_report.html")
    print("Success: Evidently AI Data Drift report generated at /tmp/evidently_drift_report.html")

if __name__ == "__main__":
    main()
