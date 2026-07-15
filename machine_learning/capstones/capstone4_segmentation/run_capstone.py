import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

def generate_segmentation_data(n_customers=300, seed=42):
    """Generates customer profiles with distinct hidden clusters."""
    np.random.seed(seed)
    
    # We will simulate 3 distinct customer groups:
    # Group 1: Bargain Hunters (high purchase frequency, low basket size, high returns)
    # Group 2: VIPs (low frequency, massive basket size, low returns)
    # Group 3: Average shoppers (moderate metrics)
    
    n_bargain = int(n_customers * 0.5)
    n_vip = int(n_customers * 0.25)
    n_avg = n_customers - n_bargain - n_vip
    
    # Bargain
    freq_b = np.random.normal(loc=35, scale=5, size=n_bargain)
    basket_b = np.random.normal(loc=25, scale=5, size=n_bargain)
    return_b = np.random.normal(loc=0.35, scale=0.08, size=n_bargain)
    
    # VIP
    freq_v = np.random.normal(loc=6, scale=1.5, size=n_vip)
    basket_v = np.random.normal(loc=450, scale=60, size=n_vip)
    return_v = np.random.normal(loc=0.03, scale=0.01, size=n_vip)
    
    # Average
    freq_a = np.random.normal(loc=15, scale=3, size=n_avg)
    basket_a = np.random.normal(loc=110, scale=20, size=n_avg)
    return_a = np.random.normal(loc=0.10, scale=0.03, size=n_avg)
    
    freq = np.concatenate([freq_b, freq_v, freq_a])
    basket = np.concatenate([basket_b, basket_v, basket_a])
    return_rate = np.concatenate([return_b, return_v, return_a])
    
    # Shuffle together
    indices = np.arange(n_customers)
    np.random.shuffle(indices)
    
    return pd.DataFrame({
        "customer_id": [f"C_{str(i).zfill(4)}" for i in range(1, n_customers + 1)],
        "purchase_frequency": freq[indices],
        "average_basket": basket[indices],
        "return_rate": return_rate[indices]
    })

def main():
    print("====================================================")
    print("Capstone 4: Customer Segmentation & PCA Engine")
    print("====================================================\n")
    
    os.makedirs("figures", exist_ok=True)
    
    # 1. Ingest Data
    print("[Step 1] Loading user behavioral matrices...")
    df = generate_segmentation_data()
    print(f"Dataset Loaded: {len(df)} customer records.")
    print("Sample records:")
    print(df.head(), "\n")
    
    X = df.drop(columns=["customer_id"])
    
    # 2. Standardize Features
    print("[Step 2] Applying standard scaling (K-Means distance prerequisite)...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 3. K-Means Clustering (K=3)
    print("[Step 3] Fitting K-Means Clustering (K=3)...")
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    df["cluster"] = clusters
    
    # Calculate quality metrics
    sil = silhouette_score(X_scaled, clusters)
    print(f"Clustering Complete | Silhouette Score: {sil:.4f} (Ideal: closer to 1.0)\n")
    
    # 4. Dimensionality Reduction (PCA to 2 components)
    print("[Step 4] Running PCA to project features into 2D space...")
    pca = PCA(n_components=2)
    pca_coords = pca.fit_transform(X_scaled)
    df["pca_x"] = pca_coords[:, 0]
    df["pca_y"] = pca_coords[:, 1]
    
    print(f"Explained Variance by PCA 1: {pca.explained_variance_ratio_[0]*100:.2f}%")
    print(f"Explained Variance by PCA 2: {pca.explained_variance_ratio_[1]*100:.2f}%")
    print(f"Cumulative Explained Variance: {sum(pca.explained_variance_ratio_)*100:.2f}%\n")
    
    # 5. Cluster Characterization Summary
    print("[Step 5] Analyzing cluster profiles (Mean Values)...")
    profile = df.groupby("cluster").agg({
        "purchase_frequency": "mean",
        "average_basket": "mean",
        "return_rate": "mean",
        "customer_id": "count"
    }).rename(columns={"customer_id": "count"})
    
    print("\n--- Cluster Profile Summary ---")
    print(profile.round(2))
    
    # 6. Plotting Cluster Scatters in PCA space
    print("\n[Step 6] Saving cluster visualization scatter plot...")
    plt.figure(figsize=(10, 7))
    colors = ["#ec4899", "#06b6d4", "#8b5cf6"]
    labels = ["Cluster 0 (Bargain Hunters)", "Cluster 1 (VIP Clients)", "Cluster 2 (Average Shoppers)"]
    
    for i in range(3):
        cluster_data = df[df["cluster"] == i]
        plt.scatter(cluster_data["pca_x"], cluster_data["pca_y"], 
                    c=colors[i], label=labels[i], alpha=0.75, s=60, edgecolors="black", linewidths=0.5)
                    
    # Draw Centroids in PCA space
    centroids_scaled = kmeans.cluster_centers_
    centroids_pca = pca.transform(centroids_scaled)
    plt.scatter(centroids_pca[:, 0], centroids_pca[:, 1], 
                c="white", marker="X", s=200, label="Centroids", edgecolors="black", linewidths=1.5)
                
    plt.title("Customer Segments projected in 2D PCA Space", fontsize=13, pad=15)
    plt.xlabel(f"Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)", fontsize=11)
    plt.ylabel(f"Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)", fontsize=11)
    plt.legend(loc="upper right")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    
    plot_path = "figures/customer_clusters.png"
    plt.savefig(plot_path)
    plt.close()
    
    print(f"Saved cluster scatter plot to: [figures/customer_clusters.png](file:///{os.path.abspath(plot_path)})")

if __name__ == "__main__":
    main()
