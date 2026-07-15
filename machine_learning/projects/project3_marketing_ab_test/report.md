# Project 3 Report: Marketing Campaign A/B Testing

## 🎯 Executive Summary
We evaluated the effectiveness of a new generative AI-driven marketing campaign against the legacy static campaign using a two-sample proportions Z-test. 

With 15,000 visitors, the new campaign achieved a conversion rate of **5.14%** compared to the baseline of **4.13%** (a **24.4% relative lift**). 

The resulting p-value of **0.0039** is far below our significance threshold ($\alpha = 0.05$), confirming that this difference is statistically significant and recommending a full production release.

---

## 🛠️ Skills Covered
- **Hypothesis Formulation**: Defining Null ($H_0$) and Alternative ($H_a$) hypotheses.
- **Z-Test for Proportions**: Implementing standard error and pooled proportion formulas from scratch.
- **Confidence Intervals**: Constructing 95% error margins for both cohorts and their relative differences.
- **Significance Thresholds**: Using p-value rules to drive data-backed business decisions.

---

## 📈 Methodology & Formulas

### 1. Hypothesis Formulation
- **Null Hypothesis ($H_0$)**: $p_{\text{Treatment}} \le p_{\text{Control}}$ (The new campaign does not increase conversions).
- **Alternative Hypothesis ($H_a$)**: $p_{\text{Treatment}} > p_{\text{Control}}$ (The new campaign increases conversions).

### 2. Two-Sample Z-Test for Proportions
- **Pooled Conversion Rate ($\hat{p}$)**:
  $$\hat{p} = \frac{x_A + x_B}{n_A + n_B}$$
- **Pooled Standard Error ($SE$)**:
  $$SE = \sqrt{\hat{p}(1 - \hat{p})\left(\frac{1}{n_A} + \frac{1}{n_B}\right)}$$
- **Z-Statistic ($z$)**:
  $$z = \frac{p_B - p_A}{SE}$$

---

## 📊 Results Summary

| Cohort | Sample Size ($n$) | Conversions ($x$) | Conversion Rate ($p$) | 95% Confidence Interval |
|---|---|---|---|---|
| **Control (A)** | 7,490 | 309 | 4.126% | [3.676%, 4.575%] |
| **Treatment (B)** | 7,510 | 386 | 5.140% | [4.641%, 5.638%] |
| **Difference ($B - A$)** | - | - | **1.014%** | **[0.347%, 1.681%]** |

### Inferential Metrics
- **Z-Statistic**: **2.9781**
- **p-Value**: **0.0029**
- **Outcome**: Reject $H_0$ in favor of $H_a$ because $p < 0.05$.

---

## 💼 Business Outcomes
1. **Full Rollout Recommended**: Deploy the generative AI campaign to all customers immediately. Based on current traffic levels (1.2 million visitors/year), this 1.014% absolute increase in conversion rate will yield **12,168 additional conversions per year**.
2. **Mitigated False Positives**: By refusing to deploy the campaign until meeting the power-analyzed sample size of 15,000 visitors, the company avoided wasting engineering resources on a false-positive outcome.
3. **Calibrated ROI Forecasts**: The difference confidence interval [0.347%, 1.681%] allows financial teams to model conservative (+4,164 sales) and optimistic (+20,172 sales) revenue scenarios.
