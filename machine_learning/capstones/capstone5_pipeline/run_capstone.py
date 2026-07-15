import os
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def generate_raw_pipeline_data(n_samples=500, seed=42):
    """Generates a raw, uncleaned client dataset containing missing fields."""
    np.random.seed(seed)
    
    age = np.random.normal(loc=38, scale=12, size=n_samples)
    age = np.clip(np.round(age), 18, 90)
    
    # Missing ages
    age[np.random.choice(range(n_samples), size=20, replace=False)] = np.nan
    
    income = np.random.normal(loc=65000, scale=20000, size=n_samples)
    income = np.clip(income, 10000, 200000)
    
    account_type = np.random.choice(["Personal", "Business", np.nan], size=n_samples, p=[0.7, 0.25, 0.05])
    
    # Label logic
    z = -1.5 + 0.02 * np.nan_to_num(age, nan=38) + 0.000015 * income
    z += np.where(account_type == "Business", 0.5, -0.2)
    prob_premium = 1 / (1 + np.exp(-z))
    is_premium = np.random.binomial(1, prob_premium)
    
    return pd.DataFrame({
        "age": age,
        "income": income,
        "account_type": account_type,
        "is_premium": is_premium
    })

def check_feature_drift(baseline_stats, current_batch):
    """Simple MLOps drift checking mechanism."""
    print("\n[MLOps Monitor] Running feature drift checks on current batch...")
    drift_detected = False
    
    for col in baseline_stats.index:
        baseline_mean = baseline_stats[col]
        current_mean = current_batch[col].mean()
        
        # Prevent division by zero
        if baseline_mean == 0: continue
        pct_change = abs(current_mean - baseline_mean) / baseline_mean
        
        print(f"Feature: {col:<10} | Baseline Mean: {baseline_mean:>9.2f} | Batch Mean: {current_mean:>9.2f} | Shift: {pct_change*100:>5.2f}%")
        
        if pct_change > 0.15:
            print(f"  [!] DRIFT ALERT: Feature '{col}' shifted by {pct_change*100:.2f}% (exceeds threshold 15%)")
            drift_detected = True
            
    if not drift_detected:
        print("  [OK] All features within safe boundaries.")
        
    return drift_detected

def main():
    print("====================================================")
    print("Capstone 5: End-to-End Production ML Pipeline")
    print("====================================================\n")
    
    os.makedirs("models", exist_ok=True)
    
    # 1. Load data
    print("[Step 1] Ingesting raw, dirty client records...")
    df = generate_raw_pipeline_data()
    print(f"Loaded {len(df)} records. Features count: {df.shape[1]-1}")
    print("Pre-cleaning Null Values count:")
    print(df.isnull().sum(), "\n")
    
    X = df.drop(columns=["is_premium"])
    y = df["is_premium"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    # 2. Pipeline Architecture
    print("[Step 2] Defining Scikit-Learn ColumnTransformer pipeline structure...")
    num_cols = ["age", "income"]
    cat_cols = ["account_type"]
    
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
    
    full_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42))
    ])
    
    # 3. Fit Pipeline
    print("[Step 3] Fitting pipeline (calculating imputation statistics & training model)...")
    full_pipeline.fit(X_train, y_train)
    
    # Calculate baseline stats for monitoring later
    baseline_stats = X_train[num_cols].mean()
    
    # 4. Serialize Model
    print("\n[Step 4] Serializing model pipeline to disk using joblib...")
    model_path = "models/premium_class_pipeline.joblib"
    joblib.dump(full_pipeline, model_path)
    print(f"Model successfully saved to: {model_path}\n")
    
    # 5. Reload and Inference on raw request
    print("[Step 5] Loading serialized pipeline for mock API serving...")
    loaded_pipeline = joblib.load(model_path)
    
    # Mocking incoming client request with raw, dirty inputs
    raw_json_request = pd.DataFrame({
        "age": [np.nan],  # Missing value
        "income": [120000.00],
        "account_type": ["Business"]
    })
    
    prediction = loaded_pipeline.predict(raw_json_request)[0]
    prob = loaded_pipeline.predict_proba(raw_json_request)[0, 1]
    
    print("\n--- Mock API Inference ---")
    print(f"Incoming Request: age=NaN, income=$120,000, account_type='Business'")
    print(f"Pipeline Predicted Category: {'PREMIUM' if prediction==1 else 'STANDARD'}")
    print(f"Classification Confidence:   {prob*100:.2f}%\n")
    
    # 6. MLOps Monitoring simulation
    print("[Step 6] Simulating MLOps pipeline monitoring...")
    # Simulate a new batch of customers where average income shifted upwards (e.g. a luxury cohort)
    drifted_batch = pd.DataFrame({
        "age": np.random.normal(loc=38, scale=12, size=100),
        "income": np.random.normal(loc=82000, scale=15000, size=100) # shifted from 65k to 82k
    })
    
    check_feature_drift(baseline_stats, drifted_batch)

if __name__ == "__main__":
    main()
