# Module 6: Probability Fundamentals (Practical ML Focus)

Probability is the mathematical language of uncertainty. In Machine Learning, every prediction, classification, and recommendation is a probabilistic estimate. To build and debug ML systems, you must understand how events interact.

---

## 1. Concept Explanation

### The Basics
- **Experiment**: An action or process that leads to an outcome (e.g., a user visiting our product landing page).
- **Sample Space ($S$)**: The set of all possible outcomes (e.g., $S = \{\text{Purchase}, \text{Leave without purchase}\}$).
- **Event ($A$)**: A subset of the sample space (e.g., $A = \{\text{Purchase}\}$).
- **Probability of an Event ($P(A)$)**: A number between 0 and 1 indicating the likelihood of that event occurring.
  $$P(A) = \frac{\text{Number of favorable outcomes}}{\text{Total number of outcomes in } S}$$

### Intersection ($A \cap B$) & Union ($A \cup B$)
- **Intersection ($A \cap B$)**: Both events $A$ and $B$ occur (e.g., customer clicks an ad AND buys).
- **Union ($A \cup B$)**: Event $A$ or event $B$ (or both) occur (e.g., customer clicks an ad OR signs up for the newsletter).
- **Addition Rule**:
  $$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

### Conditional Probability ($P(A|B)$)
The probability of event $A$ occurring, given that event $B$ has already occurred.
$$P(A|B) = \frac{P(A \cap B)}{P(B)}$$

### Independent Events
Two events $A$ and $B$ are independent if the occurrence of one does not affect the probability of the occurrence of the other.
* **Mathematical Condition**:
  $$P(A \cap B) = P(A) \times P(B)$$
  $$P(A|B) = P(A)$$

---

## 2. Why It Matters in ML

1. **Classification Outputs**: Classification algorithms (like Logistic Regression, Random Forest, or Neural Networks) do not output a label directly; they output a probability score (e.g., $P(\text{Churn} = 1 | \text{User History}) = 0.72$). We apply thresholding to convert this probability into a binary decision.
2. **Sequential Models**: User interaction logs are analyzed using conditional probabilities. For instance, in session-based recommendation models, we calculate:
   $$P(\text{Click Item 3} \mid \text{Clicked Item 1} \cap \text{Clicked Item 2})$$
3. **Feature Engineering**: Understanding correlation and independence allows us to design independent features for models like Naive Bayes, which require features to be conditionally independent.

---

## 3. Business Example

**Scenario**: An entertainment streaming platform wants to predict whether a user will subscribe after starting a free trial.
* **Events**:
  - $A$: User subscribes ($P(A) = 0.15$).
  - $B$: User watches at least 5 hours of content in week 1 ($P(B) = 0.30$).
  - $A \cap B$: User watches 5+ hours AND subscribes ($P(A \cap B) = 0.12$).
* **The Goal**: Should the marketing team target users who watch less than 5 hours with a discount code?
* **The Analysis**:
  - Let's compute the conditional probability of subscribing given they watched 5+ hours:
    $$P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{0.12}{0.30} = 0.40 \text{ (40% subscription probability)}$$
  - Given they did *not* watch 5+ hours ($\neg B$):
    $$P(A|\neg B) = \frac{P(A) - P(A \cap B)}{1 - P(B)} = \frac{0.15 - 0.12}{1 - 0.30} = \frac{0.03}{0.70} \approx 0.043 \text{ (4.3% subscription probability)}$$
* **Decision**: Focus marketing budget on nudging users to cross the 5-hour watch threshold during week 1, as it increases subscription likelihood by nearly 10x.

---

## 4. Dataset Example

User event logs from the streaming platform:

| User ID | Hours Watched Week 1 | Watched 5+ Hours (B) | Subscribed (A) |
|---|---|---|---|
| U_001 | 8.2 | 1 | 1 |
| U_002 | 1.1 | 0 | 0 |
| U_003 | 12.0 | 1 | 0 |
| U_004 | 4.5 | 0 | 0 |
| U_005 | 6.0 | 1 | 1 |

---

## 5. Python Example

```python
import pandas as pd

# 1. Create simulated user logs
logs = {
    "user_id": [f"U_{i}" for i in range(1000)],
    "watched_5h": [1 if x < 300 else 0 for x in range(1000)],  # 30% watch 5h
    "subscribed": [0] * 1000
}
df = pd.DataFrame(logs)

# Let's seed conversion probabilities
# If watched_5h=1, subscription probability is 40%
# If watched_5h=0, subscription probability is 4.3%
import numpy as np
np.random.seed(42)
df.loc[df["watched_5h"] == 1, "subscribed"] = np.random.choice([1, 0], size=300, p=[0.40, 0.60])
df.loc[df["watched_5h"] == 0, "subscribed"] = np.random.choice([1, 0], size=700, p=[0.043, 0.957])

# 2. Calculate probabilities programmatically
p_subscribed = df["subscribed"].mean()
p_watched = df["watched_5h"].mean()
p_both = len(df[(df["watched_5h"] == 1) & (df["subscribed"] == 1)]) / len(df)

# Conditional Probability P(Subscribe | Watched 5h)
p_sub_given_watch = p_both / p_watched

print(f"P(Subscribe) = {p_subscribed*100:.2f}%")
print(f"P(Watch 5h) = {p_watched*100:.2f}%")
print(f"P(Subscribe and Watch 5h) = {p_both*100:.2f}%")
print(f"P(Subscribe | Watch 5h) = {p_sub_given_watch*100:.2f}%")
```

---

## 6. Mini Project Context: Customer Purchase Prediction

In `projects/project1_customer_spending/` and probability assignments, you analyze behaviors. For this specific topic:
- We track sequential clickstreams.
- We evaluate the probability of transition between states (e.g., Homepage -> Product Page -> Add to Cart -> Purchase).
- We use conditional probabilities to trigger personalized checkout reminders.

---

## 7. Interview Questions

1. **What is conditional probability? State the mathematical formula.**
   *Answer*: Conditional probability is the probability of an event $A$ occurring, given that another event $B$ has already occurred. The formula is $P(A|B) = \frac{P(A \cap B)}{P(B)}$, where $P(A \cap B)$ is the joint probability of both events occurring, and $P(B)$ is the probability of the condition.
2. **If $P(A) = 0.5$ and $P(B) = 0.3$, and we know $A$ and $B$ are independent, what is $P(A \cup B)$?**
   *Answer*: Since $A$ and $B$ are independent, $P(A \cap B) = P(A) \times P(B) = 0.5 \times 0.3 = 0.15$.
   Using the addition rule: $P(A \cup B) = P(A) + P(B) - P(A \cap B) = 0.5 + 0.3 - 0.15 = 0.65$ (or 65%).
3. **What is the difference between mutually exclusive events and independent events?**
   *Answer*: 
   - **Mutually Exclusive**: The events cannot occur at the same time. If $A$ happens, $B$ cannot ($P(A \cap B) = 0$).
   - **Independent**: The occurrence of one event has no influence on the probability of the other occurring ($P(A|B) = P(A)$). Mutually exclusive events are actually highly *dependent*: if $A$ occurs, the probability of $B$ drops to 0.

---

## 8. Common Mistakes

- **Assuming independence blindly**: Multiplying $P(A) \times P(B)$ to get $P(A \cap B)$ without verifying independence. For example, $P(\text{Rain}) \times P(\text{Umbrella sales}) \ne P(\text{Rain and Umbrella sales})$, because they are highly dependent.
- **Confusing $P(A|B)$ with $P(B|A)$**: (Also known as the Prosecutor's Fallacy). The probability that a suspect is guilty given matching DNA is not the same as the probability of matching DNA given the suspect is guilty.
- **Ignoring the base rate**: Assuming that because a test is 99% accurate, a positive result implies a 99% chance of disease, ignoring how rare the disease is in the population.

---

## 9. Production Usage & MLOps

In marketing automation systems:
* Calculate user conversion probabilities in real-time. If $P(\text{Purchase} \mid \text{Cart Abandoned}) < 0.10$, enqueue the user ID into an automated email campaign offering a 15% discount. If the probability is already high, save the discount cost and let them convert organically.

---

## 10. AI FDE Perspective

In real enterprise deployments, your AI solutions will run on messy human data. 

When predicting user actions, never build model outputs as absolute "Yes/No" categorizations. Always return the prediction as a calibrated probability score. Calibrated probabilities allow client operations teams to configure their own decision-making thresholds based on business budgets and risk tolerance, making your AI tool infinitely more flexible.
