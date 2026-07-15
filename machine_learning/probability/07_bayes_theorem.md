# Module 7: Bayes Theorem (Practical ML Focus)

Bayes' Theorem is one of the most powerful concepts in statistics and machine learning. It describes the probability of an event based on prior knowledge of conditions that might be related to the event.

---

## 1. Concept Explanation

Bayes' Theorem allows us to update our beliefs as new evidence becomes available:

$$P(A|B) = \frac{P(B|A) P(A)}{P(B)}$$

Where:
* **$P(A|B)$ (Posterior Probability)**: The probability of hypothesis $A$ given the observed evidence $B$.
* **$P(B|A)$ (Likelihood)**: The probability of evidence $B$ given that hypothesis $A$ is true.
* **$P(A)$ (Prior Probability)**: The initial probability of hypothesis $A$ before seeing any evidence.
* **$P(B)$ (Evidence)**: The total probability of the evidence occurring under all possible hypotheses.
  $$P(B) = P(B|A)P(A) + P(B|\neg A)P(\neg A)$$

### The Bayesian Intuition
Instead of thinking of probability as a static frequency, Bayesians view probability as a "measure of belief" that is dynamically updated when new data arrives:

$$\text{Posterior} \propto \text{Likelihood} \times \text{Prior}$$

---

## 2. Why It Matters in ML

1. **Naive Bayes Classifier**: A classic, highly efficient classifier used for text classification, spam filtering, and sentiment analysis. It assumes that features (e.g., words in an email) are conditionally independent given the class (Spam/Not Spam).
2. **Bayesian Hyperparameter Optimization**: Instead of checking random combinations of hyperparameters (Grid/Random Search), Bayesian optimization builds a probabilistic model of the objective function and uses it to select the best hyperparameters to evaluate next, saving massive GPU computation time.
3. **Handling Imbalanced Datasets**: If a disease affects only 0.1% of the population (Prior = 0.001), a diagnostic model that is 99% accurate will still yield mostly false positives. Bayes' theorem helps us calibrate model thresholds to account for this imbalance.

---

## 3. Business Example

**Scenario**: A cybersecurity startup wants to classify network connections as "Fraudulent" ($F$) or "Legitimate" ($L$).
* **Priors**:
  - Only 0.5% of connections are fraudulent: $P(F) = 0.005$, so $P(L) = 0.995$.
* **Likelihoods**:
  - If a connection is fraudulent, the probability of it originating from an anonymous VPN is 80%: $P(\text{VPN}|F) = 0.80$.
  - If a connection is legitimate, the probability of it originating from an anonymous VPN is only 2%: $P(\text{VPN}|L) = 0.02$.
* **The Goal**: Calculate the probability that a connection originating from an anonymous VPN is actually fraudulent.
* **The Calculation**:
  - First, compute the total evidence $P(\text{VPN})$:
    $$P(\text{VPN}) = P(\text{VPN}|F)P(F) + P(\text{VPN}|L)P(L)$$
    $$P(\text{VPN}) = (0.80 \times 0.005) + (0.02 \times 0.995) = 0.004 + 0.0199 = 0.0239 \text{ (2.39% total VPN traffic)}$$
  - Now, apply Bayes' Theorem:
    $$P(F|\text{VPN}) = \frac{P(\text{VPN}|F) P(F)}{P(\text{VPN})} = \frac{0.80 \times 0.005}{0.0239} = \frac{0.004}{0.0239} \approx 0.1673 \text{ (16.7% probability)}$$
* **Decision**: Even though a VPN source is highly suspicious, a VPN connection has only a 16.7% chance of being fraud because fraud is extremely rare. Rather than blocking VPNs outright, flag them for multi-factor authentication (MFA).

---

## 4. Dataset Example

Spam classifier training records:

| Email Text | Contains "Buy" | Contains "Meeting" | Label (Target) |
|---|---|---|---|
| "Buy cheap stock now" | 1 | 0 | Spam |
| "Let's schedule a meeting" | 0 | 1 | Ham |
| "Buy groceries today" | 1 | 0 | Ham |
| "Urgent: buy gold" | 1 | 0 | Spam |

---

## 5. Python Example

Here is a simplified Naive Bayes calculation from scratch:

```python
# Vocabulary mapping: probability of word occurrence given label
# P(Word | Spam) and P(Word | Ham)
p_word_given_spam = {"buy": 0.60, "meeting": 0.05, "urgent": 0.40}
p_word_given_ham = {"buy": 0.01, "meeting": 0.40, "urgent": 0.02}

# Base priors
p_spam = 0.10
p_ham = 0.90

def classify_email(words):
    # Calculate relative posterior numerators: Likelihood * Prior
    # We assume independence between words (Naive Bayes)
    spam_score = p_spam
    ham_score = p_ham
    
    for word in words:
        if word in p_word_given_spam:
            spam_score *= p_word_given_spam[word]
            ham_score *= p_word_given_ham[word]
            
    # Normalize to get actual probabilities
    prob_spam = spam_score / (spam_score + ham_score)
    return prob_spam

# Test email: ["buy", "urgent"]
test_email = ["buy", "urgent"]
prob_is_spam = classify_email(test_email)
print(f"Email: {test_email}")
print(f"Probability of being Spam: {prob_is_spam*100:.2f}%")
```

---

## 6. Mini Project Context: Email Spam Classifier

In `projects/project4_email_spam/`, you will build a complete text-based spam classifier from scratch:
1. Tokenize and clean raw text files.
2. Build vocabulary counters to compute priors and conditional likelihoods for words.
3. Classify test emails using Naive Bayes.
4. Calculate accuracy, precision, and recall metrics to evaluate performance.

---

## 7. Interview Questions

1. **What is Bayes' Theorem? Describe all components of the formula.**
   *Answer*: Bayes' Theorem calculates conditional probability: $P(A|B) = \frac{P(B|A)P(A)}{P(B)}$. 
   - $P(A|B)$ is the **posterior** (updated belief).
   - $P(B|A)$ is the **likelihood** (evidence probability given hypothesis).
   - $P(A)$ is the **prior** (initial belief before evidence).
   - $P(B)$ is the **evidence** (total probability of data under all hypotheses).
2. **Why is the "Naive" Bayes classifier called "naive"?**
   *Answer*: It is called "naive" because it makes the simplifying assumption that all features are conditionally independent of each other given the class label. In reality, features are often correlated (e.g., in text, the words "San" and "Francisco" occur together frequently), but despite this violation, the classifier performs remarkably well in practice.
3. **How does Bayesian classification handle a zero-frequency count for a feature?**
   *Answer*: If a word in a test email never appeared in the spam training set, the conditional probability $P(\text{word}|\text{Spam}) = 0$. Since we multiply all probabilities, this single zero will zero-out the entire spam probability. We solve this using **Laplace Smoothing** (adding a small count $\alpha$, usually 1, to both numerator and denominator).

---

## 8. Common Mistakes

- **Ignoring the Prior (Base Rate Fallacy)**: Assuming a highly accurate test guarantees a diagnosis. If a rare disease occurs in 1 in a million people, and a test has a 99% accuracy rate, a positive test result still only indicates a ~0.01% chance of actually having the disease.
- **Not using Log-probabilities**: In code, multiplying many small probabilities (e.g., $0.001 \times 0.02 \times \dots$) leads to **arithmetic underflow** (numbers rounding to absolute 0). In production, we add log-probabilities instead:
  $$\log(P(A|B)) \propto \log(P(A)) + \sum \log(P(x_i|A))$$

---

## 9. Production Usage & MLOps

In high-throughput microservices:
* **Spam Filters**: Naive Bayes serves as an excellent L1 filter. Because it relies on simple additions and lookups in hash tables, it can run in $<1$ millisecond, acting as a low-cost screening layer before routing suspicious emails to heavier, more expensive LLM-based verification pipelines.

---

## 10. AI FDE Perspective

When presenting model behaviors to clients (e.g., in medical AI or fraud detection), they will often demand models that minimize false positives to 0. 

By framing your model decisions around Bayes' Theorem, you can show them that if the prior rate of fraud is extremely low, any classification boundary will inevitably create false positives. Introducing them to Bayesian trade-offs helps them understand that risk thresholding is a business decision, not a bug in the model.
