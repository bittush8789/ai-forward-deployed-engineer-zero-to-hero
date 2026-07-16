#!/usr/bin/env python3
"""
AI Claims Assistant mock validation script.
Checks incoming claims against policy coverage thresholds.
"""

import sys

class ClaimsAssistant:
    def __init__(self, max_claim_limit=5000.00):
        self.max_claim_limit = max_claim_limit

    def validate_claim(self, claim_id: str, amount: float) -> bool:
        print(f"Auditing Claim ID: {claim_id} | Amount: ${amount:.2f}")
        
        # Flag claims exceeding limit for manual review
        if amount > self.max_claim_limit:
            print("Audit: Claim exceeds threshold limit. Flagged for manual review.")
            return False
        else:
            print("Audit: Claim approved automatically.")
            return True

def main():
    print("=== Initializing AI Claims Assistant Validation ===")
    assistant = ClaimsAssistant()
    
    # Test auto approval
    assistant.validate_claim("CLM_2001", 1200.00)
    print("---")
    # Test manual review trigger
    assistant.validate_claim("CLM_2002", 7500.00)
    print("====================================================")
    sys.exit(0)

if __name__ == "__main__":
    main()
