import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, precision_recall_curve, f1_score, precision_score, recall_score

def generate_fraud_dataset(n_samples=1000, seed=42):
    """Generates an imbalanced transactional dataset with fraud labels (5% fraud)."""
    np.random.seed(seed)
    
    # Features
    transaction_amount = np.random.exponential(scale=100, size=n_samples)
    transaction_amount = np.clip(transaction_amount, 2, 5000)
    
    user_failed_logins = np.random.poisson(lam=0.5, size=n_samples)
    
    is_foreign_country = np.random.binomial(1, p=0.08, size=n_samples)
    
    # Fraud probability mapping
    z = -3.5 + 0.0015 * transaction_amount + 1.2 * user_failed_logins + 1.8 * is_foreign_country
    prob_fraud = 1 / (1 + np.exp(-z))
    fraud_label = np.random.binomial(1, prob_fraud)
    
    return pd.DataFrame({
        "transaction_amount": transaction_amount,
        "failed_logins": user_failed_logins,
        "is_foreign": is_foreign_country,
        "is_fraud": fraud_label
    })

def main():
    print("====================================================")
    print("Capstone 3: Transactional Fraud Detection System")
    print("====================================================\n")
    
    os.makedirs("figures", exist_ok=True)
    
    # 1. Ingest Imbalanced Data
    print("[Step 1] Loading transactional logs...")
    df = generate_fraud_dataset()
    print(f"Transactions Ingested: {len(df)} | Fraud Count: {df['is_fraud'].sum()} ({df['is_fraud'].mean()*100:.2f}%)\n")
    
    X = df.drop(columns=["is_fraud"])
    y = df["is_fraud"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    
    # 2. Scaling Continuous Features
    print("[Step 2] Processing features (Standard Scaling numerical columns)...")
    scaler = StandardScaler()
    scaled_cols = ["transaction_amount", "failed_logins"]
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    
    X_train_scaled[scaled_cols] = scaler.fit_transform(X_train[scaled_cols])
    X_test_scaled[scaled_cols] = scaler.transform(X_test[scaled_cols])
    
    # 3. Model Fit with Class Weight Balance
    print("\n[Step 3] Fitting Random Forest Classifier with balanced class weights...")
    model = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # 4. Predict Probabilities
    probs = model.predict_proba(X_test_scaled)[:, 1]
    
    # 5. Threshold Tuning for Fraud Decision
    print("\n[Step 4] Scanning classification thresholds to maximize F1-score...")
    thresholds = np.linspace(0.1, 0.9, 9)
    best_threshold = 0.5
    max_f1 = 0.0
    
    print("\n--- Decision Threshold Grid Performance ---")
    print(f"{'Threshold':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10}")
    print("-" * 47)
    
    for t in thresholds:
        preds = (probs >= t).astype(int)
        precision = precision_score(y_test, preds, zero_division=0)
        recall = recall_score(y_test, preds, zero_division=0)
        f1 = f1_score(y_test, preds, zero_division=0)
        print(f"{t:<10.2f} | {precision*100:<9.1f}% | {recall*100:<9.1f}% | {f1*100:<9.1f}%")
        if f1 > max_f1:
            max_f1 = f1
            best_threshold = t
            
    print("-" * 47)
    print(f"Optimal Threshold: {best_threshold:.2f} | Maximum F1-Score: {max_f1*100:.2f}%\n")
    
    # 6. Evaluation metrics curves plotting
    print("[Step 5] Saving Precision-Recall curve visualizations...")
    precisions, recalls, pr_thresholds = precision_recall_curve(y_test, probs)
    
    plt.figure(figsize=(8, 6))
    plt.plot(recalls, precisions, color="#ec4899", lw=3, label="PR Curve")
    plt.axvline(recall_score(y_test, (probs >= best_threshold).astype(int)), color="#8b5cf6", linestyle=":", 
                label=f"Recall at Opt Threshold ({best_threshold:.2f})")
                
    plt.title("Precision-Recall Curve for Fraud Classifier", fontsize=13, pad=15)
    plt.xlabel("Recall (Fraction of fraud caught)", fontsize=11)
    plt.ylabel("Precision (Fraction of correct alerts)", fontsize=11)
    plt.xlim([0.0, 1.05])
    plt.ylim([0.0, 1.05])
    plt.legend(loc="lower left")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    
    plot_path = "figures/fraud_precision_recall.png"
    plt.savefig(plot_path)
    plt.close()
    
    print(f"Saved Precision-Recall curve plot to: [figures/fraud_precision_recall.png](file:///{os.path.abspath(plot_path)})")

if __name__ == "__main__":
    main()
