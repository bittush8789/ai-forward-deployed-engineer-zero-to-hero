import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_customer_data(n_customers=500, n_outliers=15, seed=42):
    """Generates realistic customer monthly spend data with explicit outliers."""
    np.random.seed(seed)
    # Log-normal distribution representing typical retail spend
    typical_spend = np.random.lognormal(mean=5.2, sigma=0.5, size=n_customers - n_outliers) * 10
    
    # Add large outliers (e.g. wholesale purchases, enterprise clients, or data errors)
    outlier_spend = np.random.uniform(low=5000, high=15000, size=n_outliers)
    
    # Combine
    all_spend = np.concatenate([typical_spend, outlier_spend])
    np.random.shuffle(all_spend)
    
    customer_ids = [f"C_{str(i).zfill(4)}" for i in range(1, n_customers + 1)]
    
    return pd.DataFrame({
        "customer_id": customer_ids,
        "monthly_spend": all_spend
    })

def calculate_metrics_from_scratch(values):
    """Calculates mean, median, variance, std dev, and quartiles from scratch."""
    n = len(values)
    sorted_vals = sorted(values)
    
    # Mean
    mean_val = sum(sorted_vals) / n
    
    # Median
    if n % 2 == 1:
        median_val = sorted_vals[n // 2]
    else:
        median_val = (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2.0
        
    # Variance & Standard Deviation (Sample)
    squared_diffs = [(x - mean_val) ** 2 for x in sorted_vals]
    variance_val = sum(squared_diffs) / (n - 1)
    std_dev_val = variance_val ** 0.5
    
    # Quartiles (linear interpolation equivalent to pandas default)
    def get_percentile(p):
        idx = p * (n - 1)
        low_idx = int(np.floor(idx))
        high_idx = int(np.ceil(idx))
        if low_idx == high_idx:
            return sorted_vals[low_idx]
        return sorted_vals[low_idx] + (idx - low_idx) * (sorted_vals[high_idx] - sorted_vals[low_idx])
        
    q1 = get_percentile(0.25)
    q3 = get_percentile(0.75)
    iqr = q3 - q1
    
    return {
        "mean": mean_val,
        "median": median_val,
        "variance": variance_val,
        "std_dev": std_dev_val,
        "q1": q1,
        "q3": q3,
        "iqr": iqr
    }

def main():
    print("====================================================")
    print("Project 1: Customer Spending & Outlier Analysis")
    print("====================================================\n")
    
    # Create output directory for figures if it doesn't exist
    os.makedirs("figures", exist_ok=True)
    
    # 1. Load Data
    print("[Step 1] Ingesting and simulating customer spend dataset...")
    df = generate_customer_data()
    print(f"Loaded {len(df)} customer records successfully.")
    print("First 5 records:")
    print(df.head(), "\n")
    
    # 2. Calculate statistics from scratch
    print("[Step 2] Calculating statistics from scratch vs pandas...")
    spend_list = df["monthly_spend"].tolist()
    scratch = calculate_metrics_from_scratch(spend_list)
    
    # Compare with pandas
    pd_mean = df["monthly_spend"].mean()
    pd_median = df["monthly_spend"].median()
    pd_std = df["monthly_spend"].std()
    pd_q1 = df["monthly_spend"].quantile(0.25)
    pd_q3 = df["monthly_spend"].quantile(0.75)
    
    print("\n--- Statistical Comparison Table ---")
    print(f"{'Metric':<20} | {'Scratch Value':<15} | {'Pandas Value':<15}")
    print("-" * 56)
    print(f"{'Mean':<20} | ${scratch['mean']:<14.2f} | ${pd_mean:<14.2f}")
    print(f"{'Median':<20} | ${scratch['median']:<14.2f} | ${pd_median:<14.2f}")
    print(f"{'Std Deviation':<20} | ${scratch['std_dev']:<14.2f} | ${pd_std:<14.2f}")
    print(f"{'Q1 (25th Percent)':<20} | ${scratch['q1']:<14.2f} | ${pd_q1:<14.2f}")
    print(f"{'Q3 (75th Percent)':<20} | ${scratch['q3']:<14.2f} | ${pd_q3:<14.2f}")
    print(f"{'IQR':<20} | ${scratch['iqr']:<14.2f} | ${pd_q3 - pd_q1:<14.2f}")
    
    # 3. Detect Outliers
    print("\n[Step 3] Running Tukey IQR Outlier Detection...")
    iqr = scratch["iqr"]
    q1 = scratch["q1"]
    q3 = scratch["q3"]
    
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outliers = df[(df["monthly_spend"] < lower_bound) | (df["monthly_spend"] > upper_bound)]
    clean_df = df[(df["monthly_spend"] >= lower_bound) & (df["monthly_spend"] <= upper_bound)]
    
    print(f"Lower Outlier Boundary: ${lower_bound:.2f}")
    print(f"Upper Outlier Boundary: ${upper_bound:.2f}")
    print(f"Identified Outliers count: {len(outliers)} ({len(outliers)/len(df)*100:.2f}% of data)")
    print("\nTop 5 Outlier Customers:")
    print(outliers.sort_values(by="monthly_spend", ascending=False).head())
    
    # 4. Generate Visualizations
    print("\n[Step 4] Generating distribution and box plots...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram of raw vs cleaned spend
    axes[0].hist(df["monthly_spend"], bins=30, alpha=0.6, label="Raw Spend", color="#E91E63")
    axes[0].hist(clean_df["monthly_spend"], bins=30, alpha=0.8, label="Cleaned Spend", color="#00BCD4")
    axes[0].set_title("Customer Spend Distribution")
    axes[0].set_xlabel("Monthly Spend ($)")
    axes[0].set_ylabel("Customer Count")
    axes[0].legend()
    axes[0].grid(True, linestyle="--", alpha=0.5)
    
    # Box plot
    axes[1].boxplot(df["monthly_spend"], vert=False, patch_artist=True,
                    boxprops=dict(facecolor="#00BCD4", color="#00BCD4"),
                    medianprops=dict(color="#E91E63", linewidth=2))
    axes[1].set_title("Spend Range & Outlier Identification")
    axes[1].set_xlabel("Monthly Spend ($)")
    axes[1].grid(True, linestyle="--", alpha=0.5)
    
    plt.tight_layout()
    plot_path = "figures/spend_analysis.png"
    plt.savefig(plot_path)
    plt.close()
    print(f"Saved visualization report chart to: [figures/spend_analysis.png](file:///{os.path.abspath(plot_path)})")
    
    # 5. Cleaned Metrics Summary
    print("\n[Step 5] Recalculating clean spend metrics...")
    clean_mean = clean_df["monthly_spend"].mean()
    clean_median = clean_df["monthly_spend"].median()
    clean_std = clean_df["monthly_spend"].std()
    
    print(f"Clean Mean Spend: ${clean_mean:,.2f} (shifted down from ${pd_mean:,.2f})")
    print(f"Clean Median Spend: ${clean_median:,.2f} (shifted from ${pd_median:,.2f})")
    print(f"Clean Std Dev Spend: ${clean_std:,.2f} (stabilized from ${pd_std:,.2f})")
    
if __name__ == "__main__":
    main()
