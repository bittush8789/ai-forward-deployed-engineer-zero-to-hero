import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc, precision_recall_curve

def generate_churn_dataset(n_users=1000, seed=42):
    """Generates customer usage records with correlated churn labels."""
    np.random.seed(seed)
    
    # Features
    contract_months = np.random.choice([1, 12, 24], size=n_users, p=[0.6, 0.3, 0.1])
    monthly_charges = np.random.normal(loc=70, scale=20, size=n_users)
    monthly_charges = np.clip(monthly_charges, 20, 150)
    
    support_calls = np.random.poisson(lam=1.5, size=n_users)
    
    # Categorical payment method
    pay_method = np.random.choice(["Credit_Card", "Electronic_Check", "Bank_Transfer"], size=n_users, p=[0.4, 0.4, 0.2])
    
    # Calculate churn probability based on parameters
    # Contract: month-to-month (1) increases churn risk
    # Support calls: increases risk significantly
    # Monthly charges: higher charge increases risk
    # Electronic check: increases risk slightly
    z = -1.5 - 0.05 * contract_months + 0.015 * monthly_charges + 0.75 * support_calls
    z += np.where(pay_method == "Electronic_Check", 0.4, -0.2)
    
    prob_churn = 1 / (1 + np.exp(-z))
    churned = np.random.binomial(1, prob_churn)
    
    return pd.DataFrame({
        "contract_months": contract_months,
        "monthly_charges": monthly_charges,
        "support_calls": support_calls,
        "payment_method": pay_method,
        "churn": churned
    })

def evaluate_business_value(probs, y_true, threshold):
    """Calculates net business value saved based on custom utility matrix.
    
    Cost Matrix:
    - CLV (Customer Lifetime Value) = $150
    - Retention Incentive Cost = $15
    - Acceptance rate of incentive = 75%
    
    Formulas:
    - TP (Predict Churn, True Churn): We spend $15, customer accepts 75% of the time, saving CLV.
      Net value = 0.75 * ($150 - $15) + 0.25 * (-$150) = $101.25 - $37.50 = +$63.75
    - FP (Predict Churn, No Churn): We waste $15 incentive on customer who would have stayed anyway.
      Net value = -$15.00
    - FN (Predict No Churn, True Churn): Customer churns, we lose CLV.
      Net value = -$150.00
    - TN (Predict No Churn, No Churn): Customer stays organically.
      Net value = $0.00
    """
    preds = (probs >= threshold).astype(int)
    
    tp = sum(1 for t, p in zip(y_true, preds) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, preds) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, preds) if t == 1 and p == 0)
    tn = sum(1 for t, p in zip(y_true, preds) if t == 0 and p == 0)
    
    # Net Financial Utility
    net_value = (tp * 63.75) + (fp * -15.00) + (fn * -150.00)
    return net_value, tp, fp, fn, tn

def main():
    print("====================================================")
    print("Project 5: Customer Churn Prediction & Value Tuning")
    print("====================================================\n")
    
    os.makedirs("figures", exist_ok=True)
    
    # 1. Load Data
    print("[Step 1] Initializing customer cohort data...")
    df = generate_churn_dataset()
    print(f"Cohort size: {len(df)} users | Base churn rate: {df['churn'].mean()*100:.2f}%")
    
    # 2. Preprocessing & Feature Engineering
    print("\n[Step 2] Processing features (One-Hot Encoding & Scaling)...")
    # One-hot encoding categorical features
    df_encoded = pd.get_dummies(df, columns=["payment_method"], drop_first=True)
    
    X = df_encoded.drop(columns=["churn"])
    y = df_encoded["churn"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Scaling continuous numerical variables
    scaler = StandardScaler()
    scaled_cols = ["contract_months", "monthly_charges", "support_calls"]
    X_train[scaled_cols] = scaler.fit_transform(X_train[scaled_cols])
    X_test[scaled_cols] = scaler.transform(X_test[scaled_cols])
    
    # 3. Model Training
    print("\n[Step 3] Training Logistic Regression classifier...")
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    
    # Extract inference probabilities
    probs = model.predict_proba(X_test)[:, 1]
    
    # 4. Probabilistic Evaluations
    fpr, tpr, roc_thresholds = roc_curve(y_test, probs)
    roc_auc = auc(fpr, tpr)
    precision, recall, pr_thresholds = precision_recall_curve(y_test, probs)
    
    print(f"Model AUC-ROC Score: {roc_auc:.4f}")
    
    # 5. Financial Threshold Optimization Loop
    print("\n[Step 4] Running Business Value Optimization Loop...")
    thresholds = np.linspace(0.05, 0.95, 19)
    best_threshold = 0.50
    max_utility = -9999999
    utility_report = []
    
    print("\n--- Financial Threshold Scenarios ---")
    print(f"{'Threshold':<10} | {'TP':<5} | {'FP':<5} | {'FN':<5} | {'TN':<5} | {'Net Value Saved':<15}")
    print("-" * 59)
    
    # Baseline utility: Do nothing threshold (essentially 1.0 threshold where all are predicted non-churn)
    # Every actual churner triggers a -$150 loss.
    do_nothing_value = sum(y_test) * -150.00
    
    for t in thresholds:
        val, tp, fp, fn, tn = evaluate_business_value(probs, y_test, t)
        utility_report.append((t, val))
        print(f"{t:<10.2f} | {tp:<5} | {fp:<5} | {fn:<5} | {tn:<5} | ${val:,.2f}")
        if val > max_utility:
            max_utility = val
            best_threshold = t
            best_stats = (tp, fp, fn, tn)
            
    print("-" * 59)
    print(f"Do Nothing Cost Baseline: ${do_nothing_value:,.2f}")
    print(f"Maximum Saved Value: ${max_utility:,.2f} at Threshold: {best_threshold:.2f}")
    print(f"Net Financial Benefit: ${max_utility - do_nothing_value:,.2f}")
    
    # 6. Plotting Curves
    print("\n[Step 5] Plotting evaluation and utility curve...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # ROC Curve
    axes[0].plot(fpr, tpr, color="#E91E63", lw=2, label=f"ROC curve (AUC = {roc_auc:.2f})")
    axes[0].plot([0, 1], [0, 1], color="#757575", linestyle="--")
    axes[0].set_xlim([0.0, 1.0])
    axes[0].set_ylim([0.0, 1.05])
    axes[0].set_xlabel("False Positive Rate")
    axes[0].set_ylabel("True Positive Rate")
    axes[0].set_title("Receiver Operating Characteristic (ROC)")
    axes[0].legend(loc="lower right")
    axes[0].grid(True, linestyle="--", alpha=0.5)
    
    # Business Value Curve
    t_vals = [r[0] for r in utility_report]
    u_vals = [r[1] for r in utility_report]
    
    axes[1].plot(t_vals, u_vals, color="#00BCD4", lw=3, label="Projected Value ($)")
    axes[1].axvline(best_threshold, color="#E91E63", linestyle=":", label=f"Optimal Threshold ({best_threshold:.2f})")
    axes[1].axhline(do_nothing_value, color="#757575", linestyle="--", label="Do Nothing Baseline")
    axes[1].set_xlabel("Classification Threshold")
    axes[1].set_ylabel("Net Financial Utility ($)")
    axes[1].set_title("Business Value Curve vs. Decision Threshold")
    axes[1].legend(loc="lower center")
    axes[1].grid(True, linestyle="--", alpha=0.5)
    
    plt.tight_layout()
    plot_path = "figures/churn_prediction_analysis.png"
    plt.savefig(plot_path)
    plt.close()
    
    print(f"Saved visualization report chart to: [figures/churn_prediction_analysis.png](file:///{os.path.abspath(plot_path)})")

if __name__ == "__main__":
    main()
