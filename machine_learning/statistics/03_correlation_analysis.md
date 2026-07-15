# Module 3: Correlation Analysis (Practical ML Focus)

Correlation analysis is the study of how variables move in relation to one another. In Machine Learning, understanding correlation is vital for feature selection, identifying redundant features, and discovering hidden relationships.

---

## 1. Concept Explanation

### Covariance
Covariance measures the directional relationship between two random variables.
* **Positive Covariance**: As $X$ increases, $Y$ tends to increase.
* **Negative Covariance**: As $X$ increases, $Y$ tends to decrease.
* **Formula**:
  $$\text{Cov}(X, Y) = \frac{1}{N-1} \sum_{i=1}^{N} (x_i - \mu_X)(y_i - \mu_Y)$$
* **Limitation**: The magnitude of covariance is dependent on the scale of the variables. For example, the covariance between height (in meters) and weight is different from height (in centimeters) and weight. It is not standard.

### Pearson Correlation Coefficient ($r$)
Pearson correlation standardizes covariance by dividing it by the product of the standard deviations of both variables. It measures the **linear** relationship.
* **Formula**:
  $$r = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y}$$
* **Range**: $-1$ to $+1$.
  * $+1$: Perfect positive linear correlation.
  * $0$: No linear correlation.
  * $-1$: Perfect negative linear correlation.
* **Assumption**: It assumes the variables are normally distributed and have a linear relationship. It is highly sensitive to outliers.

### Spearman Rank Correlation ($\rho$)
Spearman correlation measures the **monotonic** relationship between two variables. It does this by ranking the values of each variable and calculating the Pearson correlation on those ranks.
* **Range**: $-1$ to $+1$.
* **Benefits**:
  * It does not assume normality.
  * It can capture non-linear, monotonic relationships (e.g., as $X$ increases, $Y$ increases, but not at a constant rate).
  * It is highly robust to outliers.

---

## 2. Why It Matters in ML

1. **Multicollinearity**: If two independent variables are highly correlated (e.g., $r > 0.85$), they are redundant. Multicollinearity makes linear regression coefficients unstable and makes it difficult to interpret feature importances. We drop one of the redundant features.
2. **Feature Selection**: Identifying which features are highly correlated with the target variable ($y$) gives a quick set of candidate predictors.
3. **Model Debugging**: Visualizing feature correlations via Seaborn heatmaps is a fast way to verify that your data isn't leaking information (e.g., a "Customer ID" column accidentally being correlated with the target label).

---

## 3. Business Example

**Scenario**: A real estate portal wants to build a predictive pricing tool. They have features:
* `living_area_sqft`
* `number_of_rooms`
* `price`
* `year_built`
* `lot_size`
* `heating_bill_cents`

* **The Problem**: Both `living_area_sqft` and `number_of_rooms` are highly correlated ($r = 0.92$). Keeping both features in a linear pricing model results in weird, contradictory coefficients (e.g., rooms having a negative coefficient while area is positive).
* **The Solution**:
  1. Identify the correlation between `living_area_sqft` and `number_of_rooms`.
  2. Drop `number_of_rooms` since `living_area_sqft` contains more granular variation.
  3. Ensure the selected features have high correlation with the target variable `price` but low correlation with each other.

---

## 4. Dataset Example

Typical feature correlation matrix structure:

| Feature | Price | Living Area | Rooms | Year Built |
|---|---|---|---|---|
| **Price** | 1.00 | 0.85 | 0.72 | 0.15 |
| **Living Area** | 0.85 | 1.00 | 0.92 | 0.08 |
| **Rooms** | 0.72 | 0.92 | 1.00 | 0.02 |
| **Year Built** | 0.15 | 0.08 | 0.02 | 1.00 |

Here, `Living Area` and `Rooms` are redundant ($0.92$). We keep `Living Area` since it has a higher correlation with `Price` ($0.85$ vs $0.72$).

---

## 5. Python Example

```python
import numpy as np
import pandas as pd

# 1. Create simulated real estate data
np.random.seed(42)
n_houses = 100
living_area = np.random.normal(2000, 500, n_houses)
rooms = (living_area / 400) + np.random.normal(0, 0.5, n_houses)
rooms = np.round(np.clip(rooms, 1, 8))
year_built = np.random.randint(1950, 2022, n_houses)
price = 50 * living_area + 15000 * rooms - 200 * (2026 - year_built) + np.random.normal(0, 10000, n_houses)

df = pd.DataFrame({
    "price": price,
    "living_area": living_area,
    "rooms": rooms,
    "year_built": year_built
})

# 2. Compute Pearson Correlation
pearson_matrix = df.corr(method="pearson")
print("Pearson Correlation Matrix:")
print(pearson_matrix.round(2))

# 3. Compute Spearman Rank Correlation
spearman_matrix = df.corr(method="spearman")
print("\nSpearman Correlation Matrix:")
print(spearman_matrix.round(2))

# 4. Programmatic Multicollinearity Filtering
# Find pairs of features with correlation > 0.85
corr_matrix = df.drop(columns=["price"]).corr().abs()
upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.85)]

print(f"\nHighly collinear features identified for exclusion: {to_drop}")
```

---

## 6. Mini Project Context: House Price Prediction Feature Analysis

In `projects/project2_house_prices/`, you will:
1. Load a multi-feature housing dataset.
2. Build a full correlation analysis pipeline that outputs Pearson and Spearman matrices.
3. Automatically plot a correlation heatmap using Seaborn and save it as an image.
4. Filter out redundant collinear features and select the top predictive variables.

---

## 7. Interview Questions

1. **What is the difference between Pearson and Spearman correlation? When would you prefer Spearman?**
   *Answer*: Pearson measures the linear relationship between two variables, assuming they are normally distributed. Spearman measures the monotonic relationship by calculating Pearson on the ranks of the data. You prefer Spearman when the variables have a non-linear relationship (e.g., exponential growth) or when your dataset contains non-normal distributions or extreme outliers.
2. **If two features have a correlation of 0, does that mean they are completely independent?**
   *Answer*: No. A correlation of 0 means there is no *linear* (Pearson) or *monotonic* (Spearman) relationship. However, they could still have a strong non-linear relationship. For example, $Y = X^2$ has a Pearson correlation near 0 over the range $[-10, 10]$, even though $Y$ is completely dependent on $X$.
3. **What is Multicollinearity, and why is it problematic for linear regression?**
   *Answer*: Multicollinearity occurs when two or more independent variables are highly correlated. This is problematic because it makes the estimates of regression coefficients unstable and highly sensitive to small changes in the model. It becomes impossible to identify which feature is truly driving the prediction.

---

## 8. Common Mistakes

- **Confusing Correlation with Causation**: Just because Ice Cream Sales and Shark Attacks are highly correlated ($r = 0.88$) does not mean eating ice cream causes shark attacks. Both are driven by a confounding variable: warm summer temperatures.
- **Relying solely on Pearson for non-linear relations**: A feature could have a critical non-linear relation with the target, but its Pearson correlation score is near 0. Always visualize your relationships with scatter plots.
- **Keeping both highly correlated features in linear models**: This leads to model instability. Keep the one that has a cleaner collection process or a higher univariate correlation with the target.

---

## 9. Production Usage & MLOps

During model training runs (CI/CD pipelines):
* Run automatic check scripts that measure the correlation of all input features. If a new dataset contains features with a correlation $> 0.95$ to the target, raise a **data leakage warning**. This often happens when target labels or post-event metrics are accidentally included in the training features.

---

## 10. AI FDE Perspective

In enterprise settings, business stakeholders love correlation heatmaps because they are highly visual. 

As an FDE, you should use correlation matrices during client presentations to validate their domain beliefs (e.g., "Yes, our data confirms that your high-value customers are highly correlated with marketing campaign X") and to push back on client requests to throw 500 uncleaned columns into a black-box model. It keeps the model lean, explainable, and cost-efficient to run in production.
