# Module 1.4: AI/ML Data Modeling

Welcome to **AI/ML Data Modeling**. Once raw data is cleaned and warehoused, it must be transformed into a format optimized for training Machine Learning models or serving inferences. Traditional relational models break down here; ML models require heavily denormalized, time-travel capable "Features."

---

## 1. Detailed Theory

### Feature Store Design
A Feature Store is a centralized repository that allows data scientists to discover, share, and manage ML features.
- **Offline Store**: High capacity, high latency. Used for generating large batches of training data. (e.g., Snowflake, BigQuery, S3).
- **Online Store**: Low capacity, ultra-low latency. Used for serving features in real-time during inference. (e.g., Redis, DynamoDB).
- **Feature Groups**: Groupings of related features, typically joined by a common primary key (e.g., `user_id`) and an `event_timestamp`.

### Time-Travel and Point-in-Time Correctness
When generating training data, you must prevent **data leakage** (using data from the future to predict the past). Your schema must support "Time Travel" to recreate the exact state of a feature at a specific timestamp.

### Training Data vs. Inference Schema
- **Training Data**: Huge, historical datasets (Offline Store). Models expect rows of features mapping to a target label.
- **Inference Schema**: A single JSON payload or a fast key-value lookup (Online Store) containing only the features needed *right now* to make a prediction.

### Metadata & Lineage
- **Model Metadata Schema**: Storing exactly which versions of which features were used to train a specific model version.
- **Experiment Tracking Schema**: Storing hyperparameters, metrics (F1, RMSE), and artifacts for different training runs (e.g., MLflow schemas).
- **Data Lineage**: Tracking the transformation path of a feature from the raw Bronze layer all the way to the ML model input.

---

## 2. Architecture Diagram: Feature Store Concept

```mermaid
flowchart TD
    Raw[Raw Data] -->|Spark Jobs| Offline[Offline Store\n(Data Warehouse / Lake)]
    Offline -->|Batch Extract| Train[Training Data Sets]
    Train --> ML[Train ML Model]
    
    Offline -->|Sync via Kafka/Airflow| Online[Online Store\n(Redis/DynamoDB)]
    App[Production App] -->|Request Prediction| API[Model API]
    API -->|Fetch Features| Online
    Online --> API
    API --> App
```

---

## 3. Production Use Cases

1. **Fraud Detection**: At the moment a user swipes a credit card, the Model API queries the Online Store for `num_transactions_last_5_min` and `avg_transaction_amt_30d` for that `user_id` to make a sub-50ms prediction.
2. **Recommendation Systems**: Generating a daily batch of personalized item recommendations for millions of users by querying the Offline Store.

---

## 4. Real Company Examples

- **Uber (Michelangelo)**: Built one of the first and most famous internal feature stores, allowing them to rapidly deploy thousands of ML models across the company.
- **Feast / Hopsworks**: Popular open-source and commercial Feature Store solutions that standardize how these schemas are built across enterprises.

---

## 5. Coding Examples

### Feature Group Schema Definition (Conceptual SQL)

To support point-in-time correctness, feature tables must always include an entity ID and an event timestamp.

```sql
CREATE TABLE user_transaction_features (
    user_id UUID,                     -- Entity ID
    event_timestamp TIMESTAMP,        -- Time-travel key
    
    -- Features
    tx_count_30d INT,
    total_spend_30d DECIMAL(10, 2),
    avg_tx_amount DECIMAL(10, 2),
    
    PRIMARY KEY (user_id, event_timestamp)
);
```

---

## 6. Hands-on Labs

**Lab: Prevent Data Leakage**
**Objective**: Understand how improper schema joins cause leakage.
**Instructions**:
You have a table of `User_Features` and a table of `Purchases`. You want to predict if a user will buy a product on November 1st. 
Write out why a standard SQL `JOIN` on `user_id` without checking `event_timestamp < '2023-11-01'` will ruin your model's real-world accuracy.

---

## 7. Assignments

**Assignment: Experiment Tracking Schema**
Design a simple SQL database schema for a custom MLflow-like experiment tracker. You need three tables: `Experiments`, `Runs`, and `Metrics`. Establish the Primary and Foreign Keys connecting them.

---

## 8. Interview Questions

1. **What is the difference between an Online Feature Store and an Offline Feature Store?**
   *Answer Hint: Offline stores handle massive historical data for training (high latency, high volume). Online stores hold only the latest feature values for real-time inference (low latency, key-value lookup).*
2. **What is Data Leakage in ML Data Modeling?**
   *Answer Hint: Including data in your training set that would not be available at the time of prediction in production (e.g., using a feature from Nov 2nd to predict an event on Nov 1st).*

---

## 9. Best Practices (FDE Standards)

- **Immutable Features**: Once a feature row is calculated and written for a specific timestamp, it should never be updated. If the feature logic changes, create a new feature version.
- **Unify Feature Logic**: The code that calculates `avg_spend_30d` for the Offline Store must be the exact same code that calculates it for the Online Store, otherwise, Training-Serving Skew occurs.

---

## 10. Common Mistakes

- **Training-Serving Skew**: When the Python code generating features for the Jupyter Notebook (training) is slightly different than the Java code generating features in production (serving), causing the model to fail silently. Feature Stores solve this.
