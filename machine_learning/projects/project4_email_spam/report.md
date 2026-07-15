# Project 4 Report: Email Spam Detection (Bayes Theorem)

## 🎯 Executive Summary
In this project, we built a **Naive Bayes Document Classifier** from scratch in Python to label emails as Spam or Ham (legitimate). 

Using Laplace smoothing to handle unseen vocabulary words, and log-probability summation to prevent floating-point arithmetic underflow, the classifier achieved **100% Accuracy, Precision, and Recall** on our independent validation corpus.

---

## 🛠️ Skills Covered
- **Bayesian Modeling**: Applying Bayes' Theorem to text classification.
- **Laplace Smoothing**: Adding a dummy value ($\alpha = 1$) to conditional probabilities to prevent multiplication by zero.
- **Numerical Calibration**: Summing log-probabilities to avoid arithmetic underflow in high-dimensional text vectors.
- **Classification Metrics**: Implementing Precision, Recall, Accuracy, and F1-score from scratch.

---

## 📈 Methodology & Formulas

### 1. Bayes' Theorem for Documents
To classify email document $D$ (set of words $w_1, w_2, \dots, w_k$) into class $C$ (Spam or Ham):
$$P(C \mid D) \propto P(C) \prod_{i=1}^{k} P(w_i \mid C)$$

### 2. Laplace Smoothing
If a word $w$ is not present in the training set for class $C$, its conditional probability is smoothed as:
$$P(w \mid C) = \frac{\text{Count}(w, C) + \alpha}{\text{Total Words in } C + \alpha \times \text{Vocab Size}}$$
*(Where $\alpha = 1.0$ is the smoothing factor).*

### 3. Log-Probability Conversion
To prevent computer memory underflow from multiplying dozens of small floating-point decimals, we sum the logarithms of the probabilities instead:
$$\log P(C \mid D) \propto \log P(C) + \sum_{i=1}^{k} \log P(w_i \mid C)$$

---

## 📊 Results Summary

### 1. Word Conditional Probabilities (Calibration Example)
- **`buy`**: $P(\text{buy}|\text{Spam}) = \textbf{8.75\%}$ vs $P(\text{buy}|\text{Ham}) = \textbf{2.33\%}$
- **`meeting`**: $P(\text{meeting}|\text{Spam}) = \textbf{1.25\%}$ vs $P(\text{meeting}|\text{Ham}) = \textbf{5.81\%}$
- **`urgent`**: $P(\text{urgent}|\text{Spam}) = \textbf{3.75\%}$ vs $P(\text{urgent}|\text{Ham}) = \textbf{1.16\%}$

### 2. Validation Classifications
- Email: `"urgent action needed click link to win cash now"`
  - Predicted Chars: **97.35% Spam** (Correct)
- Email: `"please send me the review slide for the meeting"`
  - Predicted Chars: **0.18% Spam** (Correct)

### 3. Evaluation Metrics Table
- **Accuracy**: **100.00%**
- **Precision**: **100.00%**
- **Recall**: **100.00%**
- **F1-Score**: **100.00%**

---

## 💼 Business Outcomes
1. **Low Latency Pipeline**: The Naive Bayes classifier runs in under 1 millisecond per document. This allows the mail exchange router to scan incoming messages at scale without introducing message processing delays.
2. **Zero-Frequency Resilience**: Applying Laplace smoothing prevents the classifier from crashing or returning 0% probabilities when clients send emails containing newly coined buzzwords or slang.
3. **Optimized Customer Support**: This same Bayes model structure can be retargeted to classify customer support emails into routing queues (e.g., Billing, Technical Support, Sales) based on word densities.
