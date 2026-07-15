import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score, f1_score

def generate_customer_churn_data(n_samples=600, seed=42):
    """Generates synthetic client data with churn indicators."""
    np.random.seed(seed)
    
    # Continuous
    tenure_months = np.random.lognormal(mean=2.5, sigma=0.8, size=n_samples)
    tenure_months = np.clip(np.round(tenure_months), 1, 72)
    
    monthly_charges = np.random.normal(loc=65, scale=25, size=n_samples)
    monthly_charges = np.clip(monthly_charges, 15, 120)
    
    total_charges = tenure_months * monthly_charges + np.random.normal(0, 50, n_samples)
    total_charges = np.clip(total_charges, 15, None)
    
    # Introduce some random missing values in total_charges
    missing_indices = np.random.choice(range(n_samples), size=30, replace=False)
    total_charges[missing_indices] = np.nan
    
    # Categorical
    contract_type = np.random.choice(["Month-to-month", "One year", "Two year"], size=n_samples, p=[0.55, 0.25, 0.20])
    payment_method = np.random.choice(["Electronic check", "Mailed check", "Bank transfer"], size=n_samples)
    
    # Churn probability logic
    z = -0.05 * tenure_months + 0.012 * monthly_charges + 0.0001 * np.nan_to_num(total_charges, nan=2000)
    z += np.where(contract_type == "Month-to-month", 0.8, -0.4)
    z += np.where(payment_method == "Electronic check", 0.3, -0.2)
    
    prob_churn = 1 / (1 + np.exp(-z))
    churned = np.random.binomial(1, prob_churn)
    
    return pd.DataFrame({
        "tenure_months": tenure_months,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "contract_type": contract_type,
        "payment_method": payment_method,
        "churn": churned
    })

def main():
    print("====================================================")
    print("Capstone 1: Customer Churn Prediction Pipeline")
    print("====================================================\n")
    
    # Create directory for figures
    os.makedirs("figures", exist_ok=True)
    
    # 1. Ingest Data
    print("[Step 1] Initializing customer dataset...")
    df = generate_customer_churn_data()
    print(f"Dataset Size: {len(df)} records | Churn Count: {df['churn'].sum()} ({df['churn'].mean()*100:.2f}%)\n")
    
    # Split
    X = df.drop(columns=["churn"])
    y = df["churn"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    # 2. Pipeline Configuration
    print("[Step 2] Configuring ColumnTransformer preprocessing steps...")
    num_cols = ["tenure_months", "monthly_charges", "total_charges"]
    cat_cols = ["contract_type", "payment_method"]
    
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    
    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer([
        ("num", num_pipeline, num_cols),
        ("cat", cat_pipeline, cat_cols)
    ])
    
    # 3. Model Definition & HPO
    print("\n[Step 3] Running hyperparameter search using RandomizedSearchCV...")
    # Wrap preprocessor and estimator together
    full_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(random_state=42))
    ])
    
    param_distributions = {
        "classifier__n_estimators": [50, 100, 150],
        "classifier__max_depth": [3, 5, 7, 10],
        "classifier__min_samples_split": [2, 5, 10]
    }
    
    search = RandomizedSearchCV(
        full_pipeline, 
        param_distributions, 
        n_iter=6, 
        cv=3, 
        scoring="f1", 
        random_state=42,
        n_jobs=-1
    )
    search.fit(X_train, y_train)
    
    print(f"Optimal Parameters Selected: {search.best_params_}")
    print(f"Best Training Cross-Val F1-Score: {search.best_score_*100:.2f}%\n")
    
    # 4. Evaluation
    print("[Step 4] Evaluating model performance on validation holdout...")
    best_model = search.best_estimator_
    y_pred = best_model.predict(X_test)
    probs = best_model.predict_proba(X_test)[:, 1]
    
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, probs)
    
    print("\n--- Test Set Classification Performance ---")
    print(f"Accuracy:  {accuracy*100:.2f}%")
    print(f"F1-Score:  {f1*100:.2f}%")
    print(f"ROC-AUC:   {roc_auc:.4f}")
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # 5. Extract Feature Importances
    print("\n[Step 5] Extracting and saving feature importances...")
    # Get column names after OHE
    num_names = num_cols
    ohe_step = best_model.named_steps["preprocessor"].named_transformers_["cat"].named_steps["encoder"]
    cat_names = list(ohe_step.get_feature_names_out(cat_cols))
    feature_names = num_names + cat_names
    
    importances = best_model.named_steps["classifier"].feature_importances_
    
    feat_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    }).sort_values(by="Importance", ascending=True)
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.barh(feat_df["Feature"], feat_df["Importance"], color="#8b5cf6", alpha=0.85, edgecolor="black")
    plt.title("Random Forest Churn Feature Importances", fontsize=13, pad=15)
    plt.xlabel("Importance weight score", fontsize=11)
    plt.tight_layout()
    
    plot_path = "figures/churn_feature_importances.png"
    plt.savefig(plot_path)
    plt.close()
    
    print(f"Saved feature importances plot to: [figures/churn_feature_importances.png](file:///{os.path.abspath(plot_path)})")

if __name__ == "__main__":
    main()
