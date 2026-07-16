# Practice Tasks: Module 6 - OTIF Delivery Metrics

This document outlines step-by-step tasks to configure On-Time In-Full (OTIF) calculators.

---

## Task 1: Calculate OTIF Metric
*   **Goal**: Write a Python script to calculate OTIF rates based on delivery logs.
*   **Step-by-Step Instructions**:
    1. Create a script `calculate_otif.py`:
       ```python
       # /tmp/calculate_otif.py
       import sys

       def calculate_otif(total_deliveries: int, on_time_in_full: int):
           otif = on_time_in_full / total_deliveries
           print(f"Calculated OTIF Rate: {otif:.2%}")
           
           if otif >= 0.95:
               print("PASS: OTIF meets service agreement target (95%).")
               sys.exit(0)
           else:
               print("FAIL: OTIF rate below target. Action required.")
               sys.exit(1)

       if __name__ == '__main__':
           # Test with 100 deliveries, 96 on-time and in-full (OTIF = 96%)
           calculate_otif(100, 96)
       ```
       Write this file to disk:
       ```bash
       tee /tmp/calculate_otif.py << 'EOF'
       import sys

       def calculate_otif(total_deliveries: int, on_time_in_full: int):
           otif = on_time_in_full / total_deliveries
           print(f"Calculated OTIF Rate: {otif:.2%}")
           
           if otif >= 0.95:
               print("PASS: OTIF meets service agreement target (95%).")
               sys.exit(0)
           else:
               print("FAIL: OTIF rate below target. Action required.")
               sys.exit(1)

       if __name__ == '__main__':
           calculate_otif(100, 96)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/calculate_otif.py
       ```
*   **Verification**:
    Verify the script runs successfully.
