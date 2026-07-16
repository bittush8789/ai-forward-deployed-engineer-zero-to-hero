#!/usr/bin/env python3
"""
BRD Structure Validation Parser script.
Scans document files for required sections.
"""

import sys

def validate_brd(content: str):
    print("=== Running BRD Compliance Audit ===")
    
    required_keys = ["Business Objectives", "Functional Requirements", "Non-Functional Requirements", "Acceptance Criteria"]
    
    missing = []
    for key in required_keys:
        if key not in content:
            missing.append(key)
            
    if not missing:
        print("Status: COMPLIANT")
    else:
        print(f"Status: NON-COMPLIANT (Missing sections: {missing})")
    print("====================================")

def main():
    sample_content = """
    # Enterprise Search Project Specifications
    ## Business Objectives
    - Improve data discovery speed across files.
    ## Functional Requirements
    - Match user search words to documents.
    - Render citations mapping matches.
    ## Non-Functional Requirements
    - Enforce sub-2 second response latency.
    """
    validate_brd(sample_content)
    sys.exit(0)

if __name__ == "__main__":
    main()
