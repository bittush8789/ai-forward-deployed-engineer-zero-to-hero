#!/usr/bin/env python3
"""
Safety Guardrails Input/Output Validation Lab.
"""

from pydantic import BaseModel, Field, ValidationError

class OutputSchema(BaseModel):
    summary: str = Field(description="Summarized description")
    token_cost_calculated: float = Field(description="Cost metrics mapping")

def run_guardrails_check(raw_input_json: str):
    print(f"Validating JSON output: {raw_input_json}")
    try:
        data = OutputSchema.model_validate_json(raw_input_json)
        print(f"Validation Passed: Summary = '{data.summary}', Cost = ${data.token_cost_calculated}")
    except ValidationError as e:
        print(f"Validation Failed: {e}")

def main():
    # 1. Schema compliant json
    run_guardrails_check('{"summary": "LLMOps platform scaling complete.", "token_cost_calculated": 0.0025}')
    # 2. Schema violating json (missing cost)
    run_guardrails_check('{"summary": "Incomplete data."}')

if __name__ == "__main__":
    main()
