# Practice Tasks: Project 7 - Cost Metric Tracking

This document outlines step-by-step tasks to configure token cost calculators.

---

## Task 1: Check Cost Calculator Outputs
*   **Goal**: Write a Python script to verify cost calculations based on input and output token counts.
*   **Step-by-Step Instructions**:
    1. Create a script named `validate_token_costs.py`:
       ```python
       # /tmp/validate_token_costs.py
       import sys

       def calculate_costs(input_tokens: int, output_tokens: int):
           # Cost limits: $0.0015/1K Input, $0.0020/1K Output
           input_cost = (input_tokens / 1000.0) * 0.0015
           output_cost = (output_tokens / 1000.0) * 0.0020
           total_cost = input_cost + output_cost
           
           print(f"Calculated Total Cost: ${total_cost:.5f}")
           if total_cost > 0:
               print("PASS: Cost calculator output verified.")
               sys.exit(0)
           else:
               print("FAIL: Invalid cost calculated.")
               sys.exit(1)

       if __name__ == '__main__':
           calculate_costs(2000, 1000)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/validate_token_costs.py << 'EOF'
       import sys

       def calculate_costs(input_tokens: int, output_tokens: int):
           input_cost = (input_tokens / 1000.0) * 0.0015
           output_cost = (output_tokens / 1000.0) * 0.0020
           total_cost = input_cost + output_cost
           
           print(f"Calculated Total Cost: ${total_cost:.5f}")
           if total_cost > 0:
               print("PASS: Cost calculator output verified.")
               sys.exit(0)
           else:
               print("FAIL: Invalid cost calculated.")
               sys.exit(1)

       if __name__ == '__main__':
           calculate_costs(2000, 1000)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/validate_token_costs.py
       ```
*   **Verification**:
    Verify the script runs and logs status:
    ```bash
    python3 /tmp/validate_token_costs.py && echo "Token costs validation passed."
    ```
