# Module 9: Probability Distributions (Practical ML Focus)

Probability distributions model how probabilities are distributed over the values of a random variable. Understanding the mathematical properties of standard distributions allows us to simulate events, forecast capacity, and design appropriate algorithms.

---

## 1. Concept Explanation

### The Normal (Gaussian) Distribution
Used for modeling continuous variables that cluster around a mean (e.g., human heights, errors in measurement).
* **Parameters**: Mean ($\mu$), Standard Deviation ($\sigma$).
* **Probability Density Function (PDF)**:
  $$f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x - \mu}{\sigma}\right)^2}$$

### The Binomial Distribution
Models the number of successes in a fixed number of independent trials, where each trial has only two outcomes (Success/Failure) and a constant probability of success.
* **Parameters**: Number of trials ($n$), Probability of success ($p$).
* **Probability Mass Function (PMF)**:
  $$P(X = k) = \binom{n}{k} p^k (1 - p)^{n-k}$$
  *(where $\binom{n}{k} = \frac{n!}{k!(n-k)!}$ is the binomial coefficient).*
* **ML Application**: Modeling conversion counts, churn counts, or click-through counts from a batch of users.

### The Poisson Distribution
Models the number of events occurring within a fixed interval of time or space, assuming these events occur with a known constant rate ($\lambda$) and independently of the time since the last event.
* **Parameters**: Average rate of occurrences ($\lambda$).
* **Probability Mass Function (PMF)**:
  $$P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}$$
* **ML Application**: Modeling the number of API calls per minute, server crashes per day, or cars arriving at a toll booth.

---

## 2. Why It Matters in ML

1. **Synthetic Data Generation**: When bootstrapping new ML features before production data is collected, we use binomial and normal distributions to simulate user populations.
2. **Poisson Regression**: When predicting count-based target variables (e.g., number of taxi rides per hour, number of customer support tickets received), standard linear regression fails because it can predict negative values. We use Poisson Regression (generalized linear models with log links).
3. **Capacity & SLA Planning**: MLOps teams model request rates to model-serving clusters as a Poisson process. This helps calculate the probability of request spikes that would breach latency SLAs.

---

## 3. Business Example

**Scenario**: A cloud-based customer support software provider wants to size their server cluster to handle incoming API queries without crashing.
* **Given**:
  - The average query arrival rate during peak hours is 10 calls per second: $\lambda = 10$.
  - The maximum capacity of a single small server instance is 15 calls per second.
* **The Goal**: Calculate the probability that the system receives more than 15 calls in a given second, triggering a server failure.
* **The Calculation**:
  - We calculate the probability of getting 15 or fewer calls ($P(X \le 15)$) using the Poisson Cumulative Distribution Function (CDF):
    $$P(X \le 15) = \sum_{k=0}^{15} \frac{10^k e^{-10}}{k!} \approx 0.9513$$
  - The probability of a system failure ($P(X > 15)$) is:
    $$P(X > 15) = 1 - P(X \le 15) = 1 - 0.9513 = 0.0487 \text{ (4.87% probability)}$$
* **Decision**: A 4.87% crash risk is too high. The engineering team must spin up a second load-balanced server instance to handle spikes.

---

## 4. Dataset Example

API call log summaries (aggregate events per second):

| Time Window | Rate Parameter ($\lambda$) | Observed Call Count ($k$) | Probability of Event |
|---|---|---|---|
| 12:00:00 - 12:00:01 | 10 | 8 | 0.1126 |
| 12:00:01 - 12:00:02 | 10 | 14 | 0.0521 |
| 12:00:02 - 12:00:03 | 10 | 21 (Overload) | 0.0009 |

---

## 5. Python Example

```python
import scipy.stats as stats

# 1. Binomial Distribution: Conversion modeling
# 100 users land on a page. Conversion probability is 5%.
# What is the probability of getting exactly 8 conversions?
binom_dist = stats.binom(n=100, p=0.05)
prob_exactly_8 = binom_dist.pmf(8)
prob_at_least_8 = 1 - binom_dist.cdf(7)

print("=== Binomial Conversion Modeling ===")
print(f"P(Exactly 8 Conversions) = {prob_exactly_8*100:.2f}%")
print(f"P(At Least 8 Conversions) = {prob_at_least_8*100:.2f}%")

# 2. Poisson Distribution: Server Traffic modeling
# Average arrival rate = 10 queries/sec.
# What is the probability of overload (> 15 queries)?
poisson_dist = stats.poisson(mu=10)
prob_overload = 1 - poisson_dist.cdf(15)

print("\n=== Poisson Traffic Modeling ===")
print(f"P(Overload: >15 Queries/sec) = {prob_overload*100:.2f}%")
```

---

## 6. Mini Project Context: Website Traffic Analysis

In `projects/project3_marketing_ab_test/` and user traffic studies, you evaluate traffic distributions. For this topic:
- We analyze the arrival distribution of users using Poisson parameters.
- We simulate user conversion patterns using Binomial models.
- We check if standard conversion rates deviate from Gaussian baselines using normal approximations.

---

## 7. Interview Questions

1. **What is the difference between a Probability Mass Function (PMF) and a Probability Density Function (PDF)?**
   *Answer*: PMF is used for **discrete** random variables and gives the probability that the variable is exactly equal to a specific value (e.g., $P(X = 3)$). PDF is used for **continuous** random variables; the probability of the variable taking a specific point value is always 0. Instead, we integrate the PDF over a range to find the probability of the variable falling within that interval.
2. **Under what conditions does a Binomial distribution look like a Normal distribution?**
   *Answer*: According to the **Central Limit Theorem**, a Binomial distribution $B(n, p)$ can be approximated by a Normal distribution $N(\mu = np, \sigma^2 = np(1-p))$ as the number of trials $n$ becomes large. A common rule of thumb is that the approximation is valid if $np \ge 5$ and $n(1-p) \ge 5$.
3. **What is the Poisson distribution's key limitation regarding variance and mean?**
   *Answer*: In a Poisson distribution, the mean ($\mu$) and variance ($\sigma^2$) are assumed to be equal ($\text{Mean} = \text{Variance} = \lambda$). In real-world data, the variance is often larger than the mean (known as **overdispersion**). When this occurs, models like Negative Binomial regression are preferred.

---

## 8. Common Mistakes

- **Using Binomial instead of Poisson for open intervals**: Attempting to model visitor counts over a month as a Binomial distribution. If there is no fixed upper limit $n$ of visitors, use a Poisson process.
- **Comparing PDF heights directly**: Confusing the value of a continuous PDF at a point (which can be $> 1.0$) with a probability. Probabilities for continuous variables are only defined as areas under the curve.
- **Ignoring independence assumptions**: Using a Poisson model to represent support ticket arrivals when a single system failure triggers thousands of correlated tickets at once (violates the independence of events assumption).

---

## 9. Production Usage & MLOps

In cloud auto-scaling scripts:
* Predict queue lengths using a Poisson process. If the probability of queue length exceeding threshold $Q$ within the next 5 minutes is $> 0.10$, proactively trigger the provisioning of new virtual machines (VMs) to handle the load before latency begins to spike.

---

## 10. AI FDE Perspective

When designing systems for forecasting demand (e.g., warehousing inventory for retail clients), clients will often ask for a single point estimate (e.g., "Predict the exact number of jackets we will sell next week"). 

As an FDE, always provide a **probabilistic forecast**. Explain that demand is a random variable (often modeled via a Negative Binomial or Poisson distribution). Give them intervals: "We are 95% confident you will sell between 450 and 520 jackets. Sizing inventory at 510 jackets minimizes stockout risk to less than 5%." This shifts the client's mindset from simple predictions to strategic risk optimization.
