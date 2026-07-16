#!/usr/bin/env python3
"""
Retail SKU demand forecasting and safety stock tuning script.
"""

import sys

def run_demand_forecast(sku_id: str, last_month_sales: int):
    print("=== SKU Demand Forecasting & Inventory Tuning ===")
    print(f"SKU ID: {sku_id} | Past Month Sales: {last_month_sales} units")
    
    # Simple forecast: project 10% increase next month due to seasonality
    projected_sales = int(last_month_sales * 1.10)
    print(f"Projected Next Month Sales: {projected_sales} units")
    
    # Calculate recommended safety stock (5 days coverage: average daily sales * 5)
    daily_avg = projected_sales / 30
    recommended_safety = int(daily_avg * 5)
    print(f"Recommended Safety Stock level: {recommended_safety} units")
    print("=================================================")

def main():
    run_demand_forecast("SKU_90210_JEANS", 1200)
    sys.exit(0)

if __name__ == "__main__":
    main()
