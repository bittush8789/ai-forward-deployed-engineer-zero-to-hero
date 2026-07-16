#!/usr/bin/env python3
"""
Project 3: Insurance Claims Assistant
Skills Focus: Domain Prompting, Structured Outputs, Response Validation.

This script demonstrates how an FDE sets up a prompt to extract structured insurance
claim details from customer incident logs. The prompt enforces output strictly adhering
to a JSON schema, which is then programmatically verified.
"""

import json

# Define the Domain Specific system prompt
CLAIMS_SYSTEM_PROMPT = """You are an Insurance Claim Intake Analyst.
Your task is to extract claims metadata from customer transcripts.

You must output your findings ONLY as a raw, valid JSON object.
Do not include any conversational text, markdown wrapping (such as ```json), or notes.

The JSON schema must contain exactly these keys:
{
  "policyholder_name": string or null (full name of the customer),
  "claim_type": "Auto" | "Home" | "Life" | "Unclassified",
  "incident_date": string or null (in YYYY-MM-DD format),
  "damage_description": string (brief summary of what occurred),
  "estimated_loss_reported": float or null (numeric value only)
}
"""

CLAIMS_USER_TEMPLATE = """Extract info from the following client statement:

<statement>
{transcript}
</statement>

JSON Output:"""

class InsuranceClaimsAssistant:
    def __init__(self, system_prompt, user_template):
        self.system_prompt = system_prompt
        self.user_template = user_template

    def assemble_prompt(self, transcript):
        return self.user_template.format(transcript=transcript)

    def validate_json_schema(self, response_str):
        """Simulates schema and data format validation."""
        try:
            # Attempt to parse raw JSON
            data = json.loads(response_str.strip())
            
            # Check mandatory keys
            required_keys = [
                "policyholder_name",
                "claim_type",
                "incident_date",
                "damage_description",
                "estimated_loss_reported"
            ]
            for key in required_keys:
                if key not in data:
                    return False, f"Missing key: '{key}'"
            
            # Check claim_type values
            valid_types = ["Auto", "Home", "Life", "Unclassified"]
            if data["claim_type"] not in valid_types:
                return False, f"Invalid claim_type: '{data['claim_type']}'"
                
            return True, data
        except json.JSONDecodeError as e:
            return False, f"Failed to parse JSON: {str(e)}"

    def mock_inference(self, transcript):
        """Generates mock LLM output representing the target structured format."""
        # Simple simulated extraction logic
        transcript_lower = transcript.lower()
        
        if "car" in transcript_lower or "crash" in transcript_lower:
            mock_llm_output = {
                "policyholder_name": "Arthur Dent",
                "claim_type": "Auto",
                "incident_date": "2026-05-12",
                "damage_description": "Rear-end collision at traffic light causing rear bumper breakage.",
                "estimated_loss_reported": 3200.00
            }
        elif "pipe" in transcript_lower or "water" in transcript_lower:
            mock_llm_output = {
                "policyholder_name": "Tricia McMillan",
                "claim_type": "Home",
                "incident_date": "2026-07-01",
                "damage_description": "Water line burst in the upstairs guest bathroom flooding the kitchen ceiling.",
                "estimated_loss_reported": 8500.50
            }
        else:
            mock_llm_output = {
                "policyholder_name": None,
                "claim_type": "Unclassified",
                "incident_date": None,
                "damage_description": "Client reported a problem but details are insufficient to identify claim categories.",
                "estimated_loss_reported": None
            }
            
        return json.dumps(mock_llm_output)

def main():
    assistant = InsuranceClaimsAssistant(CLAIMS_SYSTEM_PROMPT, CLAIMS_USER_TEMPLATE)
    
    print("Insurance Claims Structured Output Simulator")
    print("="*60)
    
    transcripts = [
        "My name is Arthur Dent. On May 12, 2026, my car was rear-ended at a light. The repairs are estimated to be $3,200.",
        "I need help with billing. I am not sure when my premium is due next month."
    ]
    
    for idx, transcript in enumerate(transcripts):
        print(f"\n--- Scenario {idx+1} ---")
        print(f"Customer Statement: '{transcript}'")
        
        # Assemble Prompt
        assembled = assistant.assemble_prompt(transcript)
        
        # Run Mock Inference
        raw_output = assistant.mock_inference(transcript)
        print(f"Raw Model Output:\n{raw_output}")
        
        # Run Schema Validation
        success, result = assistant.validate_json_schema(raw_output)
        if success:
            print("[SUCCESS] Output successfully parsed and validated against schema!")
            print(f"Verified Dictionary: {json.dumps(result, indent=2)}")
        else:
            print(f"[FAILED] Validation error: {result}")
        print("="*60)

if __name__ == "__main__":
    main()
