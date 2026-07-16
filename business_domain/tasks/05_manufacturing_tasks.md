# Practice Tasks: Module 5 - OEE Metric Calculations

This document outlines step-by-step tasks to configure OEE (Overall Equipment Effectiveness) calculators.

---

## Task 1: Calculate OEE Metric
*   **Goal**: Write a Python script to calculate OEE based on availability, performance, and quality.
*   **Step-by-Step Instructions**:
    1. Create a script `calculate_oee.py`:
       ```python
       # /tmp/calculate_oee.py
       import sys

       def calculate_oee(availability: float, performance: float, quality: float):
           oee = availability * performance * quality
           print(f"Calculated OEE: {oee:.2%}")
           
           if oee >= 0.85:
               print("PASS: OEE meets world-class manufacturing standard (85%).")
               sys.exit(0)
           else:
               print("FAIL: OEE below target. Action required.")
               sys.exit(1)

       if __name__ == '__main__':
           # Test with Availability 90%, Performance 95%, Quality 99% (OEE = 84.6%)
           calculate_oee(0.90, 0.95, 0.99)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/calculate_oee.py << 'EOF'
       import sys

       def calculate_oee(availability: float, performance: float, quality: float):
           oee = availability * performance * quality
           print(f"Calculated OEE: {oee:.2%}")
           
           if oee >= 0.85:
               print("PASS: OEE meets world-class manufacturing standard (85%).")
               sys.exit(0)
           else:
               print("FAIL: OEE below target. Action required.")
               sys.exit(1)

       if __name__ == '__main__':
           calculate_oee(0.90, 0.95, 0.99)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/calculate_oee.py
       ```
*   **Verification**:
    Verify the script runs successfully.
