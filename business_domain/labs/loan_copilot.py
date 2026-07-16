#!/usr/bin/env python3
"""
AI Loan Copilot applicant evaluation script.
Calculates Debt-to-Income ratios and checks credit score bounds.
"""

import sys

def evaluate_applicant(income: float, debt: float, credit_score: int):
    print("=== Running Loan Application Credit Audit ===")
    
    # Calculate DTI ratio
    dti = debt / income
    print(f"Monthly Income: ${income:.2f} | Monthly Debt: ${debt:.2f}")
    print(f"Calculated DTI Ratio: {dti:.2%}")
    print(f"Applicant Credit Score: {credit_score}")
    
    # Approval rules
    if dti <= 0.43 and credit_score >= 660:
        print("Status: APPROVED")
    else:
        print("Status: FLAGGED FOR MANUAL REVIEW")
    print("=============================================")

def main():
    evaluate_applicant(6000.00, 1800.00, 720)
    sys.exit(0)

if __name__ == "__main__":
    main()
