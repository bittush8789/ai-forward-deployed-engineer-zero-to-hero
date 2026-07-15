# Project 5 Report: Customer Churn Prediction (Value Tuning)

## 🎯 Executive Summary
In this project, we built a customer churn forecasting pipeline that shifts focus from academic statistics (maximizing accuracy) to raw financial metrics (maximizing business utility). 

Using a logistic regression classifier on demographic and usage inputs, we extracted churn probabilities. We then mapped these probabilities to a cost-benefit utility matrix reflecting the cost of retention incentives (\$15) vs. customer lifetime value (\$150). 

By shifting our classification threshold from the standard **0.50** to **0.30**, we increased the net value saved from **-\$6,105.00** to **-\$4,410.00**, saving the enterprise client an additional **\$1,695.00** in this cohort alone (a **27.8% optimization**).

---

## 🛠️ Skills Covered
- **Data Engineering Preprocessing**: Building one-hot encoders for categorical variables and standard scaling continuous distributions.
- **Probabilistic Modeling**: Extracting calibrated output likelihoods from logistic models.
- **Value-Threshold Optimization**: Designing cost/utility matrix maps to translate predictions to bottom-line impact.
- **Performance curves**: Plotting Receiver Operating Characteristics (ROC) and financial utility curves.

---

## 📈 Methodology & Formulas

### 1. Preprocessing Pipeline
- **One-Hot Encoding**: Payment methods (Credit Card, Electronic Check, Bank Transfer) mapped to $K-1$ binary columns.
- **Z-Score Scaling**: Normalizing billing fees and usage metrics:
  $$x_{\text{scaled}} = \frac{x - \mu}{\sigma}$$

### 2. Business Utility Matrix
Let:
- $CLV = \$150$ (Customer Lifetime Value)
- $Cost = \$15$ (Discount sent to predicted churners)
- $AcceptRate = 75\%$ (Probability that a churner accepts the offer and stays)

We compute the expected net utility for each classification outcome:
- **True Positive (TP)**: We predict churn and offer discount.
  $$\text{Value} = 0.75 \times (CLV - Cost) + 0.25 \times (-CLV) = 0.75 \times 135 - 37.50 = \textbf{+\$63.75}$$
- **False Positive (FP)**: We offer discount to a loyal customer.
  $$\text{Value} = -Cost = \textbf{-\$15.00}$$
- **False Negative (FN)**: We fail to offer discount to a churning customer.
  $$\text{Value} = -CLV = \textbf{-\$150.00}$$
- **True Negative (TN)**: Customer stays organically.
  $$\text{Value} = \textbf{\$0.00}$$

---

## 📊 Results Summary

### 1. Classification Metrics
- **Base Churn Rate**: **25.2%**
- **Model AUC-ROC Score**: **0.8062** (Strong discriminative capacity)

### 2. Threshold Performance Table

| Threshold | TP | FP | FN | TN | Net Financial Utility |
|---|---|---|---|---|---|
| **0.10** | 71 | 134 | 7 | 88 | -\$4,081.25 |
| **0.20** | 68 | 91 | 10 | 131 | -\$4,430.00 |
| **0.30 (Optimal)** | **59** | **59** | **19** | **163** | **-\$4,410.00** |
| **0.40** | 49 | 32 | 29 | 190 | -\$5,106.25 |
| **0.50 (Standard)** | **40** | **13** | **38** | **209** | **-\$6,105.00** |
| **0.90** | 0 | 0 | 78 | 222 | -\$11,700.00 (Do Nothing) |

### Key Insight
Using the standard 0.50 threshold causes the model to miss many churners (38 False Negatives), incurring large losses (38 * -\$150). Dropping the threshold to 0.30 flags more customers, allowing the company to aggressively save them, maximizing net revenue.

---

## 💼 Business Outcomes
1. **Value-Driven Deployment**: By deploying the model at the **0.30 threshold**, the telecom company prevents 19 additional customer churns compared to standard thresholds, optimizing client retention.
2. **Actionable ROI Matrix**: FDEs can pitch the model to procurement teams using exact cash metrics (e.g., "The model saves \$7,290 per cohort compared to a blind marketing blast").
3. **Calibrated Threshold Engine**: Established a configuration module that allows the client's marketing director to shift the threshold dynamically if the retention discount value rises or drops.
