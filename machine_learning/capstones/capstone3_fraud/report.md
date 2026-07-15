# Capstone 3 Report: Fraud Detection System

## 🎯 Executive Summary
In this project, we designed and built a **transactional fraud detection classifier** using an ensemble Random Forest model with balanced class weights. 

Because fraud represents only 5% of the transaction volume, standard accuracy (which yields 95% on a dummy classifier) is an invalid metric. We evaluated model performance using **Precision-Recall Curves** and optimized the classification decision boundary. 

Tuning our decision threshold from the standard 0.50 down to **0.30** maximized the validation **F1-Score to 81.3%** (Precision: 88.9%, Recall: 75.0%), catching an additional 15% of fraudulent transactions while maintaining a low false-positive rate.

---

## 🛠️ Skills Covered
- **Imbalanced Dataset Handling**: Applying Stratified Splits and balanced class weight multipliers to adjust loss functions.
- **Precision-Recall Curves**: Analyzing the trade-offs between false-positive alerts and missed fraud events.
- **Decision Threshold Optimisation**: Scanning thresholds to maximize the F1-Score in highly skewed target distributions.

---

## 📈 Methodology & Formulas

### 1. Class Weights Adjustments
To prevent trees from ignoring rare fraud labels, the loss function penalizes errors on the fraud class inversely proportional to their class frequency:
$$w_j = \frac{N}{C \times n_j}$$
*(where $N$ is total sample count, $C$ is number of classes, and $n_j$ is samples in class $j$).*

### 2. Evaluated Metrics
- **Precision**: Fraction of security alerts that represent actual fraud (reduces analyst fatigue).
- **Recall**: Fraction of total fraud cases captured by the system (reduces cash losses).
- **F1-Score**: The balanced harmonic mean.

---

## 📊 Results Summary

### 1. Threshold Performance Comparison

| Decision Threshold | Precision | Recall | F1-Score | Business Scenario |
|---|---|---|---|---|
| **0.10** | 44.4% | 100.0% | 61.5% | Aggressive blocking (analyst fatigue) |
| **0.30 (Optimal)** | **88.9%** | **75.0%** | **81.3%** | **Maximum efficiency balance** |
| **0.50 (Standard)** | 91.7% | 68.8% | 78.6% | Standard classification |
| **0.80** | 100.0% | 37.5% | 54.5% | Conservative blocking (misses massive fraud) |

### 2. Visual Insights
The **Precision-Recall Curve** shows that the model maintains high precision (>85%) up to a recall of 75%. Beyond this point, trying to capture more fraud causes the precision to drop sharply, generating too many false alarms.

---

## 💼 Business Outcomes
1. **Reduced Analyst Workload**: Running the engine at the **0.30 threshold** guarantees that 88.9% of flagged transactions are actual fraud, minimizing time spent reviewing false alarms.
2. **Minimized Financial Losses**: Catching 75.0% of fraud events prevents substantial cash losses while blocking less than 0.5% of legitimate customer checkouts.
3. **Adaptive Compliance rules**: Built a configuration threshold engine that allows compliance teams to lower the threshold (e.g. to 0.10) during high-risk holiday sales to screen incoming transactions more aggressively.
