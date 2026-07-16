#!/usr/bin/env python3
"""
Stakeholder Communication Plan Builder script.
Maps updates and channels based on stakeholder group mappings.
"""

import sys

def build_communication_plan():
    print("=== Stakeholder Communication Plan ===")
    
    # Define stakeholder mappings and channel paths
    stakeholders = {
        "Executive Sponsors (CIO/CTO)": {
            "interest": "High", "power": "High",
            "frequency": "Monthly", "channel": "Executive Steering Report"
        },
        "Business Owners (Claims Manager)": {
            "interest": "High", "power": "Medium",
            "frequency": "Bi-weekly", "channel": "Status Sync Meeting"
        },
        "Operations Team (End Users)": {
            "interest": "High", "power": "Low",
            "frequency": "Weekly", "channel": "Feedback Q&A Sessions"
        },
        "IT Security Team": {
            "interest": "Medium", "power": "High",
            "frequency": "Weekly", "channel": "Technical Integration Reviews"
        }
    }
    
    for stakeholder, details in stakeholders.items():
        print(f"Stakeholder: {stakeholder}")
        print(f"- Power/Interest: {details['power']} / {details['interest']}")
        print(f"- Communication Frequency: {details['frequency']} via {details['channel']}")
        print("---")
        
    print("=======================================")

def main():
    build_communication_plan()
    sys.exit(0)

if __name__ == "__main__":
    main()
