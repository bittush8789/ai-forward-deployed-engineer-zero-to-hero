#!/usr/bin/env python3
"""
Manufacturing anomaly detection and predictive maintenance trigger.
Scans machine telemetry logs and flags warnings.
"""

import sys

def audit_machine_telemetry(vibration_g: float, temp_c: float):
    print("=== SCADA Telemetry Anomaly Detection ===")
    print(f"Spindle Vibration: {vibration_g}g | Temperature: {temp_c}°C")
    
    # Simple threshold rules
    vibration_limit = 2.5
    temp_limit = 80.0
    
    if vibration_g > vibration_limit or temp_c > temp_limit:
        print("Status: WARNING! Anomaly detected. Scheduling repair order.")
    else:
        print("Status: NORMAL. Machinery operating within limits.")
    print("===========================================")

def main():
    audit_machine_telemetry(3.1, 72.5)
    sys.exit(0)

if __name__ == "__main__":
    main()
