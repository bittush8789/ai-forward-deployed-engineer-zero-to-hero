# Module 4: Sampling & Statistical Inference (Practical ML Focus)

Statistical inference is the process of using data analysis to deduce properties of an underlying probability distribution. In the business world, we rarely have access to the entire "population" of future users, so we must make decisions based on "samples."

---

## 1. Concept Explanation

### Population vs. Sample
* **Population**: The complete set of all individuals or events we want to draw conclusions about (e.g., all current and future visitors to a website).
* **Sample**: A subset of the population used to perform the analysis.

### Sampling Techniques
- **Simple Random Sampling**: Every member of the population has an equal chance of selection.
- **Stratified Sampling**: The population is divided into subgroups (strata) based on shared characteristics (e.g., age, gender), and random samples are drawn from each stratum to ensure representation.
- **Systematic Sampling**: Selecting every $k$-th member of the population.

### Confidence Intervals (CI)
A range of values, derived from the sample statistics, that is likely to contain the true population parameter. A **95% Confidence Interval** means that if we repeat the sampling process 100 times, 95 of the calculated intervals will contain the true population parameter.
$$\text{CI} = \hat{p} \pm Z \times \sqrt{\frac{\hat{p}(1 - \hat{p})}{n}}$$
*(For proportions, where $\hat{p}$ is the sample proportion, $n$ is sample size, and $Z$ is the z-score corresponding to the confidence level, e.g., $1.96$ for 95%).*

### Hypothesis Testing & p-Values
Hypothesis testing evaluates two mutually exclusive statements about a population:
- **Null Hypothesis ($H_0$)**: The status quo. There is no effect, no difference, or no change (e.g., the new page design does not improve conversions).
- **Alternative Hypothesis ($H_a$)**: The statement we want to prove (e.g., the new design increases conversions).
- **p-Value**: The probability of obtaining test results at least as extreme as the observed results, assuming the null hypothesis is true.
  - If **p-value < $\alpha$** (Significance level, typically 0.05), we **reject $H_0$** (Statistically Significant).
  - If **p-value $\ge$ $\alpha$**, we **fail to reject $H_0$** (Not Statistically Significant).

---

## 2. Why It Matters in ML

1. **Model Evaluation (Train/Test Split)**: When splitting data into training and testing sets, we use stratified sampling. This ensures that the proportion of target labels (e.g., 90% non-churn / 10% churn) is identical in both sets.
2. **A/B Testing (Product Releases)**: Before deploying an ML model (e.g., a new recommendation engine) to all users, we conduct an A/B test. We split users into a control group (old system) and a treatment group (new ML model) and check if the improvement is statistically significant.
3. **Statistical Power**: Determines how large our sample size needs to be before we can confidently run an experiment without getting false positives or false negatives.

---

## 3. Business Example

**Scenario**: An e-commerce brand wants to test a new AI-driven checkout page.
* **Control Group (A)**: Current checkout page (Historical conversion rate: 5.0%).
* **Treatment Group (B)**: New AI checkout page.
* **The Goal**: Verify if the new checkout page achieves a target 5.5% conversion rate (a 10% relative lift).
* **The Danger**: Running the test for only 1 day with 100 visitors might show a conversion rate of 8.0% for Group B simply due to random luck (small sample variance).
* **The Solution**: 
  1. Determine the sample size required using power analysis (e.g., 20,000 visitors per group).
  2. Run the test until the required sample size is met.
  3. Calculate the z-statistic and p-value. If $p < 0.05$, confidently launch the new AI checkout page.

---

## 4. Dataset Example

Data structure for tracking an A/B test experiment:

| User ID | Group | Visited Page | Converted (1 = Yes, 0 = No) |
|---|---|---|---|
| U_901 | Control (A) | index_v1 | 0 |
| U_902 | Treatment (B) | index_v2 | 1 |
| U_903 | Treatment (B) | index_v2 | 0 |
| U_904 | Control (A) | index_v1 | 0 |
| U_905 | Control (A) | index_v1 | 1 |

---

## 5. Python Example

```python
import numpy as np
import scipy.stats as stats

# 1. Simulated A/B test results
n_A = 10000  # Visitors to Control
n_B = 10000  # Visitors to Treatment

conversions_A = 500  # 5.0% conversion
conversions_B = 560  # 5.6% conversion

p_A = conversions_A / n_A
p_B = conversions_B / n_B

print(f"Control Conversion Rate: {p_A*100:.2f}%")
print(f"Treatment Conversion Rate: {p_B*100:.2f}%")

# 2. Two-Sample Z-Test for Proportions
# Pooled proportion
p_pooled = (conversions_A + conversions_B) / (n_A + n_B)

# Standard error
se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n_A + 1/n_B))

# Z-score
z_stat = (p_B - p_A) / se

# Two-tailed p-value
p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

print(f"\nZ-statistic: {z_stat:.4f}")
print(f"p-Value: {p_value:.4f}")

# 3. Decision
alpha = 0.05
if p_value < alpha:
    print("Decision: Reject Null Hypothesis. The AI checkout page significantly improves conversions.")
else:
    print("Decision: Fail to Reject Null Hypothesis. The difference is not statistically significant.")
```

---

## 6. Mini Project Context: Marketing Campaign A/B Testing

In `projects/project3_marketing_ab_test/`, you will:
1. Generate synthetic logs for a marketing A/B test across multiple regions.
2. Build statistical test modules from scratch to calculate Z-scores, T-scores, p-values, and 95% confidence intervals.
3. Determine if differences in click-through rates (CTR) are truly significant or just random noise.
4. Save bar charts showing the conversion rates and confidence intervals.

---

## 7. Interview Questions

1. **What is a p-value? Explain it to a non-technical product manager.**
   *Answer*: A p-value is the probability that the differences we see between our groups (like Control and Treatment) are due to random luck rather than our changes. A p-value of 0.01 means there is only a 1% chance we would see this big of a difference if the new design actually had zero impact. Hence, we can be confident the new design works.
2. **What is Type I vs Type II error, and how are they related to statistical power?**
   *Answer*: 
   - **Type I Error ($\alpha$)**: Rejecting the null hypothesis when it is true (False Positive - claiming a model works when it doesn't).
   - **Type II Error ($\beta$)**: Failing to reject the null hypothesis when it is false (False Negative - missing a real improvement).
   - **Statistical Power ($1 - \beta$)**: The probability of correctly rejecting the null hypothesis (detecting a real improvement). Higher sample sizes increase power and reduce Type II errors.
3. **Why do we use stratified sampling over random sampling when training a model for fraud detection?**
   *Answer*: Fraud is rare (e.g., 0.1% of transactions). If we use simple random sampling, our test set might accidentally contain zero fraud cases, making it impossible to evaluate model performance on fraud. Stratified sampling guarantees that both training and testing datasets contain the exact same 0.1% proportion of fraud cases.

---

## 8. Common Mistakes

- **Peeking at p-values**: Stopping an A/B test early because the p-value momentarily dropped below 0.05. This dramatically increases Type I error rate. You *must* define sample size beforehand and run the experiment to completion.
- **p-Hacking**: Running 50 different hypothesis tests on different subgroups until one yields $p < 0.05$ by chance, then publishing that result.
- **Confusing Statistical Significance with Practical Significance**: A conversion rate increase from 10.00% to 10.01% can be statistically significant with 10 million users, but the cost of implementing the change might outweigh the 0.01% gain.

---

## 9. Production Usage & MLOps

During shadow deployments and canary releases:
* **Canary Testing**: Route 5% of traffic to a new LLM model container and 95% to the legacy container. A background cron job continually checks latency and safety guardrails. If a z-test on error rates indicates a statistically significant increase in the new container, the system triggers an automatic rollback.

---

## 10. AI FDE Perspective

In enterprise software projects, client executives will often ask you to deploy an AI system and prove its ROI immediately. If they see a slight increase in sales the week after deployment, they might credit the AI, or if they see a drop, they might blame it.

As an FDE, you must establish an experimental framework before writing code. Agree on the significance level ($\alpha$), the metric (e.g., conversion rate), and the sample size. This statistical framework protects your work from external seasonal factors (like a holiday sale) and provides mathematically sound proof of your model's value.
