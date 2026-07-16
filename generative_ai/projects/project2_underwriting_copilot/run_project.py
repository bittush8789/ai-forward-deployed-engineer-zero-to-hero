#!/usr/bin/env python3
"""
Project 2: Insurance Underwriting Copilot (Function Calling & Structured Outputs)
Skills Focus: Tool Binding Schemas, JSON Schema Validation, Policy Rules Audit.

This script demonstrates how an FDE builds a structured extraction pipeline for
commercial property underwriting. It defines a tool schema to fetch building hazards, 
validates the LLM-generated arguments, and evaluates compliance with underwriting rules.
"""

import json

# Define the Tool Schema mapping for function calling
HAZARD_TOOL_SCHEMA = {
    "name": "fetch_building_hazard_data",
    "description": "Fetches fire and structural hazard ratings for a property based on age and roof type.",
    "parameters": {
        "type": "object",
        "properties": {
            "building_age": {"type": "integer", "description": "Age of the building in years."},
            "roof_material": {"type": "string", "enum": ["wood", "asphalt", "tile", "metal"], "description": "Material of the roof."}
        },
        "required": ["building_age", "roof_material"]
    }
}

class UnderwritingEvaluator:
    def fetch_building_hazard_data(self, building_age, roof_material):
        """Simulated external underwriting database utility."""
        print(f"[TOOL CALLED] Running database query for Age: {building_age}, Roof: {roof_material}...")
        
        # Core risk rules
        fire_score = 1
        structural_score = 1
        
        if building_age > 50:
            structural_score += 2
        if roof_material == "wood":
            fire_score += 3
        elif roof_material == "asphalt":
            fire_score += 1
            
        return {
            "fire_risk_rating": fire_score,
            "structural_risk_rating": structural_score,
            "notes": "Completed historical hazard query scan."
        }

    def validate_tool_arguments(self, raw_args_str):
        """Validates that model-generated parameters conform to the JSON schema."""
        try:
            args = json.loads(raw_args_str)
            
            # Check required fields
            for field in HAZARD_TOOL_SCHEMA["parameters"]["required"]:
                if field not in args:
                    raise ValueError(f"Missing required parameter: {field}")
            
            # Check enums
            valid_roofs = HAZARD_TOOL_SCHEMA["parameters"]["properties"]["roof_material"]["enum"]
            if args["roof_material"] not in valid_roofs:
                raise ValueError(f"Invalid roof material: '{args['roof_material']}'. Must be one of {valid_roofs}")
                
            return True, args
        except Exception as e:
            return False, str(e)

    def generate_underwriting_decision(self, hazard_report):
        """Compiles final structured JSON output representing the underwriting decision."""
        fire_rating = hazard_report["fire_risk_rating"]
        struct_rating = hazard_report["structural_risk_rating"]
        
        # Logic rule verification
        if fire_rating >= 4 or struct_rating >= 3:
            status = "DECLINE"
            rationale = "Property risk limits exceeded. Fire and/or structural hazard scores too high."
        else:
            status = "APPROVE"
            rationale = "Property risks lie within standard coverage guidelines."
            
        decision = {
            "underwriting_status": status,
            "scorecard": {
                "fire_score": fire_rating,
                "structural_score": struct_rating
            },
            "decision_rationale": rationale
        }
        return decision

def main():
    print("Project 2: Insurance Underwriting Copilot (Function Calling & Structured Outputs)")
    print("="*60)
    
    evaluator = UnderwritingEvaluator()
    
    # Mock LLM API extraction scenario
    print("Scenario A: Processing application with wood roof built in 1960 (66 years old)")
    mock_llm_json_args = '{"building_age": 66, "roof_material": "wood"}'
    print(f"Model Tool Call Arguments: {mock_llm_json_args}")
    
    # 1. Validate JSON parameters
    valid, parsed_args = evaluator.validate_tool_arguments(mock_llm_json_args)
    if not valid:
        print(f"[ERROR] Tool validation failed: {parsed_args}")
        return
        
    print("[SUCCESS] Arguments conform to schema.")
    
    # 2. Execute external tool call
    hazards = evaluator.fetch_building_hazard_data(
        parsed_args["building_age"], 
        parsed_args["roof_material"]
    )
    print(f"Tool Observation: {json.dumps(hazards)}")
    
    # 3. Generate structured underwriting decision
    decision = evaluator.generate_underwriting_decision(hazards)
    print(f"\nFinal Underwriting Decision JSON:\n{json.dumps(decision, indent=2)}")
    print("="*60)

if __name__ == "__main__":
    main()
