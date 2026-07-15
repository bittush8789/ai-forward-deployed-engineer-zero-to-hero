import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_housing_data(n_samples=400, seed=101):
    """Generates synthetic housing dataset with correlation patterns."""
    np.random.seed(seed)
    
    # 1. Continuous Features
    sqft_living = np.random.normal(loc=1800, scale=600, size=n_samples)
    sqft_living = np.clip(sqft_living, 600, 5000)
    
    # Highly collinear features
    rooms = np.round(sqft_living / 450 + np.random.normal(0, 0.4, n_samples))
    rooms = np.clip(rooms, 1, 8)
    
    # Age of home (skewed distribution)
    age = np.random.exponential(scale=25, size=n_samples)
    age = np.clip(age, 0, 100)
    
    # Proximity variables
    distance_to_city_center = np.random.uniform(1.0, 30.0, size=n_samples)
    
    # Target variable: Price (Log-normally distributed)
    # Price is driven by area, rooms, age, distance
    base_price = 100000 + 120 * sqft_living + 15000 * rooms - 1200 * age - 2500 * distance_to_city_center
    noise = np.random.normal(0, 20000, n_samples)
    price = np.clip(base_price + noise, 50000, None)
    
    # Force heavy right skew on price by adding extreme luxury values
    luxury_indices = np.random.choice(range(n_samples), size=20, replace=False)
    price[luxury_indices] *= np.random.uniform(2.5, 4.0, size=20)
    
    return pd.DataFrame({
        "price": price,
        "sqft_living": sqft_living,
        "rooms": rooms,
        "age": age,
        "distance_to_city_center": distance_to_city_center
    })

def calculate_manual_pearson(x, y):
    """Calculates Pearson correlation between x and y from scratch."""
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    diff_x = x - mean_x
    diff_y = y - mean_y
    covariance = np.sum(diff_x * diff_y) / (len(x) - 1)
    std_x = np.std(x, ddof=1)
    std_y = np.std(y, ddof=1)
    return covariance / (std_x * std_y)

def main():
    print("====================================================")
    print("Project 2: House Price Feature Correlation Analysis")
    print("====================================================\n")
    
    # Create directory for figures
    os.makedirs("figures", exist_ok=True)
    
    # 1. Ingest Data
    print("[Step 1] Simulating housing dataset...")
    df = generate_housing_data()
    print(f"Generated {len(df)} home observations.")
    print("Sample records:")
    print(df.head(), "\n")
    
    # 2. Distribution Shape Analysis (Skewness & Kurtosis)
    print("[Step 2] Measuring distribution shapes...")
    for col in df.columns:
        skew = df[col].skew()
        kurt = df[col].kurtosis()
        print(f"Feature: {col:<25} | Skewness: {skew:>6.2f} | Kurtosis: {kurt:>6.2f}")
        
    # 3. Handle Skewed target variable
    print("\n[Step 3] Applying Logarithmic Transformation to target column 'price'...")
    df["log_price"] = np.log(df["price"])
    print(f"Price (Raw) Skewness: {df['price'].skew():.2f}")
    print(f"Price (Log) Skewness: {df['log_price'].skew():.2f} (Close to 0 = symmetric)")
    
    # 4. Correlation Matrices (Pearson vs Spearman)
    print("\n[Step 4] Computing correlation structures...")
    # Select original columns for core matrix
    core_cols = ["price", "sqft_living", "rooms", "age", "distance_to_city_center"]
    pearson_corr = df[core_cols].corr(method="pearson")
    spearman_corr = df[core_cols].corr(method="spearman")
    
    # Compare a single cell manually from scratch
    scratch_corr = calculate_manual_pearson(df["sqft_living"].values, df["price"].values)
    print(f"Manual Pearson (sqft_living vs price): {scratch_corr:.4f}")
    print(f"Pandas Pearson (sqft_living vs price): {pearson_corr.loc['sqft_living', 'price']:.4f}")
    
    # 5. Programmatic Collinearity Detection
    print("\n[Step 5] Screening for redundant features (Collinearity > 0.80)...")
    # Exclude target 'price' from feature list
    feature_df = df.drop(columns=["price", "log_price"])
    corr_matrix = feature_df.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    collinear_features = [col for col in upper.columns if any(upper[col] > 0.80)]
    
    print(f"Identified collinear features to exclude: {collinear_features}")
    if collinear_features:
        print(f"Recommendation: Drop 'rooms' because it is highly collinear with 'sqft_living' (r = {df['sqft_living'].corr(df['rooms']):.2f})")
        
    # 6. Plotting
    print("\n[Step 6] Saving visualization heatmaps and histograms...")
    # Set up plots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Raw vs Log Price distribution
    sns.histplot(df["price"], bins=30, ax=axes[0, 0], color="#E91E63", kde=True)
    axes[0, 0].set_title("Raw Price Distribution (Right-Skewed)")
    axes[0, 0].set_xlabel("Price ($)")
    
    sns.histplot(df["log_price"], bins=30, ax=axes[0, 1], color="#00BCD4", kde=True)
    axes[0, 1].set_title("Log-Transformed Price (Normal-like)")
    axes[0, 1].set_xlabel("Log(Price)")
    
    # Heatmaps
    sns.heatmap(pearson_corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=axes[1, 0])
    axes[1, 0].set_title("Pearson Correlation Matrix (Linear)")
    
    sns.heatmap(spearman_corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=axes[1, 1])
    axes[1, 1].set_title("Spearman Correlation Matrix (Monotonic)")
    
    plt.tight_layout()
    plot_path = "figures/housing_correlation_analysis.png"
    plt.savefig(plot_path)
    plt.close()
    
    print(f"Saved visualization report chart to: [figures/housing_correlation_analysis.png](file:///{os.path.abspath(plot_path)})")

if __name__ == "__main__":
    main()
