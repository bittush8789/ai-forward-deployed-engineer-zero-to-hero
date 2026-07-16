# Practice Tasks: Module 4 - Safety Stock Optimization

This document outlines step-by-step tasks to configure safety stock rules.

---

## Task 1: Calculate Safety Stock Threshold
*   **Goal**: Write a Python script to calculate safety stock thresholds based on average daily sales and lead times.
*   **Step-by-Step Instructions**:
    1. Create a script `safety_stock.py`:
       ```python
       # /tmp/safety_stock.py
       import sys

       def calculate_safety_stock(avg_daily_sales: int, lead_time_days: int):
           # Simple formula: average daily sales multiplied by lead time
           safety_stock = avg_daily_sales * lead_time_days
           print(f"Calculated Safety Stock Threshold: {safety_stock} units")
           
           if safety_stock > 0:
               print("PASS: Threshold calculation complete.")
               sys.exit(0)
           else:
               print("FAIL: Invalid safety stock calculated.")
               sys.exit(1)

       if __name__ == '__main__':
           calculate_safety_stock(50, 5) # 50 units/day * 5 days lead time
       ```
       Write this file to disk:
       ```bash
       tee /tmp/safety_stock.py << 'EOF'
       import sys

       def calculate_safety_stock(avg_daily_sales: int, lead_time_days: int):
           safety_stock = avg_daily_sales * lead_time_days
           print(f"Calculated Safety Stock Threshold: {safety_stock} units")
           
           if safety_stock > 0:
               print("PASS: Threshold calculation complete.")
               sys.exit(0)
           else:
               print("FAIL: Invalid safety stock calculated.")
               sys.exit(1)

       if __name__ == '__main__':
           calculate_safety_stock(50, 5)
       EOF
       ```
    2. Run the script:
       ```bash
       python3 /tmp/safety_stock.py
       ```
*   **Verification**:
    Verify the script runs successfully.
