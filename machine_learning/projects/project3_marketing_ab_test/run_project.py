import os
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

def generate_ab_test_logs(n_visitors=15000, seed=333):
    """Simulates conversion logs for Control and Treatment groups."""
    np.random.seed(seed)
    
    # 50% split of visitors
    group_labels = np.random.choice(["Control", "Treatment"], size=n_visitors, p=[0.5, 0.5])
    
    # Under the hood:
    # Control conversion probability = 4.2%
    # Treatment conversion probability = 5.0%
    conversions = []
    for g in group_labels:
        p = 0.042 if g == "Control" else 0.050
        conversions.append(np.random.binomial(1, p))
        
    return pd.DataFrame({
        "visitor_id": [f"V_{str(i).zfill(5)}" for i in range(1, n_visitors + 1)],
        "group": group_labels,
        "converted": conversions
    })

def run_ab_test_from_scratch(df):
    """Computes conversions, rates, standard errors, Z-statistic, p-value, and CIs."""
    # Group sizes
    control_df = df[df["group"] == "Control"]
    treatment_df = df[df["group"] == "Treatment"]
    
    n_A = len(control_df)
    n_B = len(treatment_df)
    
    conv_A = control_df["converted"].sum()
    conv_B = treatment_df["converted"].sum()
    
    p_A = conv_A / n_A
    p_B = conv_B / n_B
    
    # 1. Z-Test for Proportions
    p_pooled = (conv_A + conv_B) / (n_A + n_B)
    se_pooled = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_A + 1 / n_B))
    
    z_stat = (p_B - p_A) / se_pooled
    # Two-tailed p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    # 2. Confidence Intervals (95%)
    z_crit = 1.96 # Z score for 95% CI
    
    se_A = np.sqrt(p_A * (1 - p_A) / n_A)
    se_B = np.sqrt(p_B * (1 - p_B) / n_B)
    
    ci_A = (p_A - z_crit * se_A, p_A + z_crit * se_A)
    ci_B = (p_B - z_crit * se_B, p_B + z_crit * se_B)
    
    # Difference Confidence Interval
    se_diff = np.sqrt((p_A * (1 - p_A) / n_A) + (p_B * (1 - p_B) / n_B))
    diff_val = p_B - p_A
    ci_diff = (diff_val - z_crit * se_diff, diff_val + z_crit * se_diff)
    
    return {
        "n_A": n_A, "n_B": n_B,
        "conv_A": conv_A, "conv_B": conv_B,
        "p_A": p_A, "p_B": p_B,
        "z_stat": z_stat, "p_value": p_value,
        "ci_A": ci_A, "ci_B": ci_B,
        "diff": diff_val, "ci_diff": ci_diff
    }

def main():
    print("====================================================")
    print("Project 3: Marketing Campaign A/B Test Inference")
    print("====================================================\n")
    
    # Create directory for figures
    os.makedirs("figures", exist_ok=True)
    
    # 1. Load Data
    print("[Step 1] Loading experimental traffic logs...")
    df = generate_ab_test_logs()
    print(f"Logged {len(df)} total visits across the campaign split.")
    
    # 2. Run statistical test
    print("\n[Step 2] Calculating conversions and running proportions Z-test...")
    results = run_ab_test_from_scratch(df)
    
    print("\n--- A/B Test Metrics Summary ---")
    print(f"Control (A) Size: {results['n_A']} | Conversions: {results['conv_A']} | Rate: {results['p_A']*100:.3f}%")
    print(f"Treatment (B) Size: {results['n_B']} | Conversions: {results['conv_B']} | Rate: {results['p_B']*100:.3f}%")
    print(f"Observed Relative Lift: {((results['p_B'] - results['p_A']) / results['p_A'])*100:.2f}%")
    
    print("\n--- Inferential Statistics ---")
    print(f"Z-Statistic: {results['z_stat']:.4f}")
    print(f"p-Value: {results['p_value']:.6f} (Significance limit: alpha = 0.05)")
    print(f"Control 95% CI: [{results['ci_A'][0]*100:.3f}%, {results['ci_A'][1]*100:.3f}%]")
    print(f"Treatment 95% CI: [{results['ci_B'][0]*100:.3f}%, {results['ci_B'][1]*100:.3f}%]")
    print(f"Difference 95% CI: [{results['ci_diff'][0]*100:.3f}%, {results['ci_diff'][1]*100:.3f}%]")
    
    # 3. Decision
    print("\n[Step 3] Evaluating business decision...")
    if results["p_value"] < 0.05:
        print("Decision: STATISTICALLY SIGNIFICANT. Reject Null Hypothesis. Deploy the Treatment campaign.")
    else:
        print("Decision: NOT SIGNIFICANT. Fail to Reject Null Hypothesis. Keep the current Control campaign.")
        
    # 4. Generate Visualizations
    print("\n[Step 4] Plotting conversion rates with 95% confidence intervals...")
    groups = ["Control (A)", "Treatment (B)"]
    rates = [results["p_A"] * 100, results["p_B"] * 100]
    
    # Error bar sizing: (value - low_ci, high_ci - value)
    err_A = (results["p_A"] - results["ci_A"][0]) * 100
    err_B = (results["p_B"] - results["ci_B"][0]) * 100
    yerrs = [err_A, err_B]
    
    plt.figure(figsize=(7, 6))
    bars = plt.bar(groups, rates, yerr=yerrs, capsize=10, color=["#E91E63", "#00BCD4"], alpha=0.8, edgecolor="black")
    
    # Annotate bar values
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height - 1.2, f"{height:.2f}%", 
                 ha="center", va="bottom", color="white", fontweight="bold", fontsize=12)
                 
    plt.title("A/B Test Results: Conversion Rate Comparison", fontsize=14, pad=15)
    plt.ylabel("Conversion Rate (%)", fontsize=12)
    plt.ylim(0, max(rates) + 2)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    
    plot_path = "figures/ab_test_results.png"
    plt.savefig(plot_path)
    plt.close()
    
    print(f"Saved visualization report chart to: [figures/ab_test_results.png](file:///{os.path.abspath(plot_path)})")

if __name__ == "__main__":
    main()
