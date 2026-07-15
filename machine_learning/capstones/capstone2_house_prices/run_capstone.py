import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def generate_house_prices_dataset(n_samples=500, seed=42):
    """Generates synthetic housing dataset with continuous features."""
    np.random.seed(seed)
    
    sqft_living = np.random.normal(loc=2000, scale=600, size=n_samples)
    sqft_living = np.clip(sqft_living, 500, 6000)
    
    bathrooms = np.round(sqft_living / 800 + np.random.normal(0, 0.3, n_samples))
    bathrooms = np.clip(bathrooms, 1, 5)
    
    age = np.random.randint(0, 80, size=n_samples)
    
    # Non-linear price relationship
    price = 80000 + 150 * sqft_living + 25000 * bathrooms - 800 * age + np.random.normal(0, 20000, n_samples)
    # Add skewness by multiplying luxury homes price
    high_value_idx = np.where(sqft_living > 2800)[0]
    price[high_value_idx] *= np.random.uniform(1.5, 2.5, len(high_value_idx))
    
    price = np.clip(price, 40000, None)
    
    return pd.DataFrame({
        "sqft_living": sqft_living,
        "bathrooms": bathrooms,
        "age": age,
        "price": price
    })

def main():
    print("====================================================")
    print("Capstone 2: House Price Prediction Platform")
    print("====================================================\n")
    
    os.makedirs("figures", exist_ok=True)
    
    # 1. Ingest
    print("[Step 1] Ingesting housing records...")
    df = generate_house_prices_dataset()
    print(f"Loaded {len(df)} records. Raw Price Skewness: {df['price'].skew():.2f}\n")
    
    # 2. Train-Test Split with Log-Target
    X = df.drop(columns=["price"])
    # Apply log-transformation to normalize the target
    y = np.log(df["price"]) 
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    # Scale Features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 3. Model Training
    print("[Step 2] Fitting Linear Regression and Random Forest Regressor on log-target...")
    
    # Linear Regression
    lr = LinearRegression()
    lr.fit(X_train_scaled, y_train)
    y_pred_lr_log = lr.predict(X_test_scaled)
    
    # Random Forest Regressor
    rf = RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42)
    rf.fit(X_train_scaled, y_train)
    y_pred_rf_log = rf.predict(X_test_scaled)
    
    # 4. Invert Target back to original space: exp(log_y)
    y_test_orig = np.exp(y_test)
    y_pred_lr = np.exp(y_pred_lr_log)
    y_pred_rf = np.exp(y_pred_rf_log)
    
    # 5. Evaluate Metrics
    print("\n[Step 3] Computing regression metrics (MAE, RMSE, R2)...")
    
    # OLS Metrics
    lr_mae = mean_absolute_error(y_test_orig, y_pred_lr)
    lr_rmse = np.sqrt(mean_squared_error(y_test_orig, y_pred_lr))
    lr_r2 = r2_score(y_test_orig, y_pred_lr)
    
    # RF Metrics
    rf_mae = mean_absolute_error(y_test_orig, y_pred_rf)
    rf_rmse = np.sqrt(mean_squared_error(y_test_orig, y_pred_rf))
    rf_r2 = r2_score(y_test_orig, y_pred_rf)
    
    print("\n--- Regression Model Comparison Table ---")
    print(f"{'Model Name':<20} | {'MAE ($)':<12} | {'RMSE ($)':<12} | {'R2 Score':<10}")
    print("-" * 62)
    print(f"{'Linear (Log-OLS)':<20} | ${lr_mae:<11.2f} | ${lr_rmse:<11.2f} | {lr_r2:<10.4f}")
    print(f"{'Random Forest':<20} | ${rf_mae:<11.2f} | ${rf_rmse:<11.2f} | {rf_r2:<10.4f}")
    
    # 6. Plotting Predictions vs Actuals
    print("\n[Step 4] Saving comparison scatter plot...")
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test_orig, y_pred_rf, color="#06b6d4", alpha=0.5, label="Random Forest Predictions")
    plt.plot([y_test_orig.min(), y_test_orig.max()], [y_test_orig.min(), y_test_orig.max()], 
             color="#ec4899", linestyle="--", lw=2, label="Ideal Line (Perfect Fit)")
             
    plt.title("Actual vs. Predicted House Prices (Random Forest)", fontsize=13, pad=15)
    plt.xlabel("Actual Price ($)", fontsize=11)
    plt.ylabel("Predicted Price ($)", fontsize=11)
    plt.legend(loc="upper left")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    
    plot_path = "figures/house_price_predictions.png"
    plt.savefig(plot_path)
    plt.close()
    
    print(f"Saved actual vs. predicted scatter plot to: [figures/house_price_predictions.png](file:///{os.path.abspath(plot_path)})")

if __name__ == "__main__":
    main()
