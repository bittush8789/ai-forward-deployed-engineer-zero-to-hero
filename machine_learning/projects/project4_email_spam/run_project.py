import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_spam_corpus():
    """Generates a small dataset of spam and ham emails for training and testing."""
    training_data = [
        # Spam
        ("Buy cheap bitcoin now for fast returns", "spam"),
        ("Get rich quick with our special offer click here", "spam"),
        ("Earn dollar home part time job urgent response required", "spam"),
        ("Win a cash prize of ten thousand dollars today only", "spam"),
        ("Cheap pharmacy drugs online free shipping discount", "spam"),
        ("Buy luxury watches at low price gift for you", "spam"),
        ("Urgent access to your bank account suspended click link", "spam"),
        ("Winner of lottery cash payout claim now", "spam"),
        ("Special promo code for cheap hotels select destination", "spam"),
        ("Get unlimited credit card with zero balance click", "spam"),
        # Ham
        ("Let us meet for lunch at the office corner", "ham"),
        ("Can you send the project update slide before tomorrow", "ham"),
        ("Review the document and give your feedback", "ham"),
        ("The quarterly business review meeting is scheduled next week", "ham"),
        ("Thanks for the gift I really appreciate it", "ham"),
        ("Please reply to my email regarding the bug report", "ham"),
        ("Are you coming to the team dinner tonight at seven", "ham"),
        ("I will call you back once I leave the airport", "ham"),
        ("Here is the invoice for last month services rendered", "ham"),
        ("Let us coordinate schedule for the onboarding session", "ham")
    ]
    
    test_data = [
        ("urgent action needed click link to win cash now", "spam"),
        ("special discount offer buy cheap luxury watches today", "spam"),
        ("please send me the review slide for the meeting", "ham"),
        ("let us meet tomorrow at the office to review slide", "ham"),
        ("meeting schedule updated check details in document", "ham")
    ]
    
    return training_data, test_data

def clean_and_tokenize(text):
    """Lowercase text and split into words, removing punctuation."""
    import re
    cleaned = re.sub(r"[^\w\s]", "", text.lower())
    return cleaned.split()

class NaiveBayesSpamClassifier:
    def __init__(self, alpha=1.0):
        self.alpha = alpha  # Laplace smoothing parameter
        self.p_spam = 0.0
        self.p_ham = 0.0
        self.spam_word_counts = {}
        self.ham_word_counts = {}
        self.vocab = set()
        
    def fit(self, training_data):
        total_emails = len(training_data)
        spam_emails = [email for email, label in training_data if label == "spam"]
        ham_emails = [email for email, label in training_data if label == "ham"]
        
        # 1. Compute Priors
        self.p_spam = len(spam_emails) / total_emails
        self.p_ham = len(ham_emails) / total_emails
        
        # 2. Tokenize and count words
        total_spam_words = 0
        total_ham_words = 0
        
        for email in spam_emails:
            words = clean_and_tokenize(email)
            for word in words:
                self.spam_word_counts[word] = self.spam_word_counts.get(word, 0) + 1
                self.vocab.add(word)
                total_spam_words += 1
                
        for email in ham_emails:
            words = clean_and_tokenize(email)
            for word in words:
                self.ham_word_counts[word] = self.ham_word_counts.get(word, 0) + 1
                self.vocab.add(word)
                total_ham_words += 1
                
        # Cache totals for denominator
        self.total_spam_words = total_spam_words
        self.total_ham_words = total_ham_words
        self.vocab_size = len(self.vocab)
        
    def predict_probability(self, text):
        """Computes probability of spam using log-probabilities to avoid underflow."""
        words = clean_and_tokenize(text)
        
        # We start with the log of the prior probability
        log_prob_spam = np.log(self.p_spam)
        log_prob_ham = np.log(self.p_ham)
        
        for word in words:
            # Word likelihood given Spam with Laplace smoothing
            count_spam = self.spam_word_counts.get(word, 0)
            p_word_spam = (count_spam + self.alpha) / (self.total_spam_words + self.alpha * self.vocab_size)
            log_prob_spam += np.log(p_word_spam)
            
            # Word likelihood given Ham with Laplace smoothing
            count_ham = self.ham_word_counts.get(word, 0)
            p_word_ham = (count_ham + self.alpha) / (self.total_ham_words + self.alpha * self.vocab_size)
            log_prob_ham += np.log(p_word_ham)
            
        # Convert log probabilities back to regular probability space
        # P(Spam | words) = exp(log_spam) / (exp(log_spam) + exp(log_ham))
        # To prevent numerical overflow, subtract max log from both exponents
        max_log = max(log_prob_spam, log_prob_ham)
        exp_spam = np.exp(log_prob_spam - max_log)
        exp_ham = np.exp(log_prob_ham - max_log)
        
        return exp_spam / (exp_spam + exp_ham)

def calculate_classification_metrics(y_true, y_pred):
    """Calculates accuracy, precision, recall, and F1 score from scratch."""
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == "spam" and p == "spam")
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == "ham" and p == "ham")
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == "ham" and p == "spam")
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == "spam" and p == "ham")
    
    accuracy = (tp + tn) / len(y_true)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "tp": tp, "tn": tn, "fp": fp, "fn": fn
    }

def main():
    print("====================================================")
    print("Project 4: Naive Bayes Email Spam Classifier")
    print("====================================================\n")
    
    os.makedirs("figures", exist_ok=True)
    
    # 1. Load data
    print("[Step 1] Ingesting text documents and labels...")
    train_data, test_data = generate_spam_corpus()
    print(f"Training corpus size: {len(train_data)} sentences")
    print(f"Testing corpus size: {len(test_data)} sentences\n")
    
    # 2. Train model
    print("[Step 2] Training Naive Bayes model (calculating word conditionals)...")
    classifier = NaiveBayesSpamClassifier(alpha=1.0)
    classifier.fit(train_data)
    print(f"Priors - P(Spam): {classifier.p_spam:.2f} | P(Ham): {classifier.p_ham:.2f}")
    print(f"Vocabulary Size: {classifier.vocab_size} unique words")
    
    # Show example word probabilities
    words_to_check = ["buy", "meeting", "urgent", "cash", "project"]
    print("\nWord Likelihood Calibration:")
    for w in words_to_check:
        c_spam = classifier.spam_word_counts.get(w, 0)
        c_ham = classifier.ham_word_counts.get(w, 0)
        p_w_spam = (c_spam + 1) / (classifier.total_spam_words + classifier.vocab_size)
        p_w_ham = (c_ham + 1) / (classifier.total_ham_words + classifier.vocab_size)
        print(f"Word: {w:<10} | P(w|Spam): {p_w_spam*100:>5.2f}% | P(w|Ham): {p_w_ham*100:>5.2f}%")
        
    # 3. Predict on test data
    print("\n[Step 3] Inference on test sentences...")
    y_true = [label for email, label in test_data]
    y_pred = []
    
    print("\n--- Test Inferences ---")
    for email, true_label in test_data:
        prob = classifier.predict_probability(email)
        pred_label = "spam" if prob >= 0.50 else "ham"
        y_pred.append(pred_label)
        print(f"Email: '{email}'")
        print(f"  P(Spam) = {prob*100:6.2f}% | Predicted: {pred_label.upper()} | True: {true_label.upper()}")
        
    # 4. Compute Metrics
    print("\n[Step 4] Calculating evaluation metrics...")
    metrics = calculate_classification_metrics(y_true, y_pred)
    
    print("\n--- Model Performance Report ---")
    print(f"Accuracy:  {metrics['accuracy']*100:.2f}%")
    print(f"Precision: {metrics['precision']*100:.2f}% (How many predicted spam were actual)")
    print(f"Recall:    {metrics['recall']*100:.2f}% (How much actual spam was caught)")
    print(f"F1-Score:  {metrics['f1_score']*100:.2f}%")
    print(f"Confusion Matrix: TP={metrics['tp']}, TN={metrics['tn']}, FP={metrics['fp']}, FN={metrics['fn']}")
    
    # 5. Visualizations
    print("\n[Step 5] Saving classification metrics visual...")
    metric_names = ["Accuracy", "Precision", "Recall", "F1-Score"]
    metric_vals = [metrics["accuracy"]*100, metrics["precision"]*100, metrics["recall"]*100, metrics["f1_score"]*100]
    
    plt.figure(figsize=(8, 5))
    bars = plt.bar(metric_names, metric_vals, color=["#3F51B5", "#009688", "#FF5722", "#9C27B0"], alpha=0.85, edgecolor="black")
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height - 12, f"{height:.1f}%", 
                 ha="center", va="bottom", color="white", fontweight="bold", fontsize=11)
                 
    plt.title("Naive Bayes Spam Classifier Performance Profile", fontsize=13, pad=15)
    plt.ylabel("Score (%)", fontsize=11)
    plt.ylim(0, 110)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    
    plot_path = "figures/spam_classifier_metrics.png"
    plt.savefig(plot_path)
    plt.close()
    
    print(f"Saved visualization report chart to: [figures/spam_classifier_metrics.png](file:///{os.path.abspath(plot_path)})")

if __name__ == "__main__":
    main()
