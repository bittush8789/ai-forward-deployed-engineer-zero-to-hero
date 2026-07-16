#!/usr/bin/env python3
"""
Project 5: Enterprise AI Automation Platform (Multi-Agent Orchestrator)
Skills Focus: Multi-Agent Systems, Supervisor Review Nodes, Security Governance.

This script implements a multi-agent automation platform with security 
governance gates. A Supervisor coordinates operations between a Security Auditor 
and a Compliance Officer to approve financial transactions.
"""

import json

class SecurityAuditorAgent:
    def evaluate_risk(self, amount):
        print(f"[Security Auditor] Auditing transaction amount: ${amount}...")
        
        # Risk rule
        if amount > 5000:
            risk = "HIGH"
            notes = "Transaction exceeds standard $5,000 threshold. Requires manual approval."
        else:
            risk = "LOW"
            notes = "Amount lies within standard operating boundaries."
            
        return {"risk_rating": risk, "notes": notes}

class ComplianceOfficerAgent:
    def verify_account(self, account_id):
        print(f"[Compliance Officer] Auditing account status for ID: {account_id}...")
        
        # Simulated database lookup
        kyc_status = "COMPLETED"
        return {"kyc_status": kyc_status, "audit_status": "CLEAR"}

class EnterpriseAutomationPlatform:
    def __init__(self):
        self.auditor = SecurityAuditorAgent()
        self.compliance = ComplianceOfficerAgent()

    def run_transaction_pipeline(self, sender_id, recipient_id, amount):
        print("Starting Multi-Agent Transaction Pipeline...")
        print(f" - Sender: {sender_id}, Recipient: {recipient_id}, Amount: ${amount}")
        print("="*60)
        
        # Step 1: Security Auditor Node
        risk_result = self.auditor.evaluate_risk(amount)
        print(f"[SYSTEM] Security Auditor Report: {json.dumps(risk_result)}")
        
        # Step 2: Compliance Officer Node
        compliance_result = self.compliance.verify_account(sender_id)
        print(f"[SYSTEM] Compliance Officer Report: {json.dumps(compliance_result)}")
        
        # Step 3: Supervisor Decision Node with Human-in-the-loop trigger
        print("\n[Supervisor] Reviewing compliance and risk records to draft final decision...")
        
        if risk_result["risk_rating"] == "HIGH":
            status = "SUSPENDED"
            action_required = "[REQUIRES_HUMAN_SIGN_OFF]"
            rationale = "Transaction suspended. High risk rating detected. Human verification required."
        elif compliance_result["kyc_status"] != "COMPLETED":
            status = "SUSPENDED"
            action_required = "[REQUIRES_KYC_VERIFICATION]"
            rationale = "Sender has incomplete KYC registration profiles."
        else:
            status = "APPROVED"
            action_required = "None"
            rationale = "Transaction matches all compliance and risk policies."
            
        decision = {
            "pipeline_status": status,
            "required_action": action_required,
            "decision_rationale": rationale
        }
        
        print("\n" + "="*50)
        print(f"Final Pipeline Decision:\n{json.dumps(decision, indent=2)}")
        print("="*50)
        
        return decision

def main():
    print("Project 5: Enterprise AI Automation Platform (Security Governance Gates)")
    print("="*60)
    
    platform = EnterpriseAutomationPlatform()
    
    # Run high risk scenario (testing Human-in-the-loop trigger)
    platform.run_transaction_pipeline(
        sender_id="ACC-4890",
        recipient_id="ACC-0129",
        amount=12500.00
    )

if __name__ == "__main__":
    main()
