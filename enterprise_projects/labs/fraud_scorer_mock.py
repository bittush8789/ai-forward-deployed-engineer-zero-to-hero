#!/usr/bin/env python3
"""
Real-time transaction fraud scoring and metrics simulator.
Logs score distributions and alerts.
"""

import sys

def score_transaction(amount: float, location_changed: bool):
    print("=== Fraud Scoring Telemetry Engine ===")
    print(f"Transaction Value: ${amount:,.2f} | Location Change: {location_changed}")
    
    # Simple scoring weight rules
    base_score = 10
    if location_changed:
        base_score += 40
    if amount > 1000.00:
        base_score += 35
        
    print(f"Calculated Risk Score: {base_score}/100")
    
    # Audit logic
    if base_score >= 80:
        print("Alert Status: BLOCKED (Suspicious risk threshold met)")
    else:
        print("Alert Status: APPROVED")
    print("======================================")

def main():
    # Test high risk transaction
    score_transaction(1200.00, True)
    sys.exit(0)

if __name__ == "__main__":
    main()
