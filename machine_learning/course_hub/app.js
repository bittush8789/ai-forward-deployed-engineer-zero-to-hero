// Unified Quizzes Database (Stats & Prob: 1-10 | Machine Learning: 11-16)
const quizzes = {
    // PART 1: Statistics & Probability (1-10)
    1: [
        {
            q: "Why is the median preferred over the mean for right-skewed salary datasets?",
            options: [
                "The mean only represents categorical values.",
                "The mean is heavily pulled upward by high executive salaries (outliers), whereas the median represents the positional middle value.",
                "The median is always equal to the mode.",
                "The mean has a variance of zero."
            ],
            correct: 1,
            exp: "The mean sums all values, meaning high-value outliers disproportionately drag it upwards. The median, being the physical middle element of the sorted list, remains stable regardless of tail values."
        },
        {
            q: "What is the Tukey IQR outlier detection threshold rule?",
            options: [
                "Any value outside [Mean ± 2 * Standard Deviation]",
                "Any value outside [Median ± 1.5 * IQR]",
                "Any value below Q1 - 1.5 * IQR or above Q3 + 1.5 * IQR",
                "Any value where variance is greater than standard deviation"
            ],
            correct: 2,
            exp: "Tukey's method defines the lower boundary as Q1 - 1.5 * IQR and the upper boundary as Q3 + 1.5 * IQR. Values outside this interval are flagged as outliers."
        },
        {
            q: "If sample size increases, what is the effect on the sample mean?",
            options: [
                "The sample mean becomes more representative of the true population mean (Law of Large Numbers).",
                "The sample mean will always increase.",
                "The sample mean will always decrease.",
                "The sample mean becomes independent of variance."
            ],
            correct: 0,
            exp: "The Law of Large Numbers states that as the sample size grows, the sample mean converges toward the expected value of the population, reducing sample variance impact."
        }
    ],
    2: [
        {
            q: "Which transformation is best suited to normalize a highly right-skewed positive numerical feature?",
            options: [
                "Linear scaling (MinMax)",
                "Standard Scaling (Z-score)",
                "Logarithmic Transformation (log(x))",
                "Square Transformation (x^2)"
            ],
            correct: 2,
            exp: "A logarithmic transformation compresses the right tail of a distribution, pulling extreme large values closer to the center and transforming right-skewed data into a normal-like shape."
        },
        {
            q: "What does a high positive kurtosis (leptokurtic) indicate about a feature distribution?",
            options: [
                "The data is perfectly symmetric with no tail.",
                "The distribution is flat and lacks outliers.",
                "The distribution is heavy-tailed with a high probability of extreme values (outliers).",
                "The mean is smaller than the median."
            ],
            correct: 2,
            exp: "Kurtosis measures the tail weight. High positive kurtosis (> 3 excess kurtosis) indicates a leptokurtic distribution, meaning it has fatter tails and is more prone to extreme events/outliers."
        },
        {
            q: "What percentage of data lies within ±2 standard deviations of the mean in a Normal Distribution?",
            options: [
                "50.0%",
                "68.2%",
                "95.4%",
                "99.7%"
            ],
            correct: 2,
            exp: "According to the empirical 68-95-99.7 rule: ~68.2% of data lies within 1 sigma, ~95.4% lies within 2 sigma, and ~99.7% lies within 3 sigma."
        }
    ],
    3: [
        {
            q: "If feature A and feature B have a Pearson correlation coefficient of 0.93, what does this indicate?",
            options: [
                "Feature A causes feature B to happen.",
                "They have a strong linear relationship and are highly collinear (redundant).",
                "They have no relationship.",
                "Feature B is the target variable."
            ],
            correct: 1,
            exp: "A correlation coefficient of 0.93 indicates a very strong positive linear relationship. In machine learning, features with $r > 0.80$ to $0.85$ are considered collinear and redundant, so one should be dropped."
        },
        {
            q: "When would you prefer Spearman Rank correlation over Pearson correlation?",
            options: [
                "When the relationship is linear and normal.",
                "When modeling categorical binary classifiers.",
                "When the relationship is non-linear but monotonic, or when the data contains extreme outliers.",
                "When variance is zero."
            ],
            correct: 2,
            exp: "Spearman rank correlation calculates correlation on the ranks of the data. It is robust to outliers and can capture non-linear monotonic (continuously increasing/decreasing) relationships."
        },
        {
            q: "If two independent variables are highly collinear, what is the impact on a Linear Regression model?",
            options: [
                "The model accuracy drops to absolute zero.",
                "The regression coefficients become highly unstable and difficult to interpret.",
                "The gradient descent algorithm will never converge.",
                "The target variable log-transforms automatically."
            ],
            correct: 1,
            exp: "Multicollinearity causes overlapping variances. This makes it impossible for linear models to accurately isolate the independent weight of each feature, making coefficients unstable."
        }
    ],
    4: [
        {
            q: "What is a p-value in a hypothesis test?",
            options: [
                "The probability that the alternative hypothesis is true.",
                "The probability of observing our test results (or more extreme) assuming the null hypothesis is true.",
                "The absolute difference in conversion rates.",
                "The percentage of visitors in the control group."
            ],
            correct: 1,
            exp: "The p-value is the probability that the observed differences (like in an A/B test) occurred purely due to random chance under the assumption that the null hypothesis (no effect) is true."
        },
        {
            q: "What is a Type I error?",
            options: [
                "Failing to reject the null hypothesis when it is false (False Negative).",
                "Rejecting the null hypothesis when it is true (False Positive).",
                "A syntax error in your Python pandas code.",
                "Having a sample size that is too small."
            ],
            correct: 1,
            exp: "A Type I error occurs when we reject the Null Hypothesis even though it was true. In business, this is a False Positive (e.g. claiming a marketing campaign works when it doesn't)."
        },
        {
            q: "Why do we use Stratified Sampling when splitting a dataset for training and testing?",
            options: [
                "It makes the training process run faster.",
                "It guarantees that key subgroups (especially rare target classes) are represented in the same proportion in both training and testing sets.",
                "It automatically removes outliers from the dataset.",
                "It converts continuous variables into discrete ones."
            ],
            correct: 1,
            exp: "Stratified sampling ensures the proportions of distinct groups (e.g., a churn rate of 5%) are maintained exactly across train/test splits, preventing evaluation bias."
        }
    ],
    5: [
        {
            q: "If missing values depend systematically on other observed features in the dataset, the missingness mechanism is called:",
            options: [
                "MCAR (Missing Completely at Random)",
                "MAR (Missing at Random)",
                "MNAR (Missing Not at Random)",
                "Imputed Missingness"
            ],
            correct: 1,
            exp: "MAR (Missing at Random) means the probability of a value being missing is related to another observed variable (e.g., older users being less likely to report gender), but not related to the missing value itself."
        },
        {
            q: "How does Winsorization handle outliers in a continuous feature?",
            options: [
                "It deletes all rows containing outliers.",
                "It replaces outliers with the median value of the column.",
                "It caps extreme values at predefined percentile boundaries (e.g., 1st and 99th percentiles).",
                "It converts the values to log space."
            ],
            correct: 2,
            exp: "Winsorization caps outliers by setting extreme values to a specific percentile threshold, limiting their leverage on linear models without reducing the sample size."
        },
        {
            q: "What is a primary danger of 'Data Leakage' during feature scaling/imputation?",
            options: [
                "It makes the model run slower in production.",
                "It leads to over-optimistic performance metrics during training, but poor performance on true unseen production data.",
                "It causes database concurrency crashes.",
                "It violates GDPR compliance rules."
            ],
            correct: 1,
            exp: "Data Leakage occurs when test set statistics (like the mean or median) are accidentally incorporated into the training preprocessing steps, giving the model artificial hints about the test set."
        }
    ],
    6: [
        {
            q: "What is the formula for conditional probability P(A|B)?",
            options: [
                "P(A|B) = P(A) * P(B)",
                "P(A|B) = P(A) + P(B) - P(A ∩ B)",
                "P(A|B) = P(A ∩ B) / P(B)",
                "P(A|B) = P(B|A) * P(B) / P(A)"
            ],
            correct: 2,
            exp: "Conditional probability is defined as the joint probability of both events occurring divided by the probability of the conditioning event: P(A|B) = P(A ∩ B) / P(B)."
        },
        {
            q: "If event A and event B are independent, what is P(A ∩ B)?",
            options: [
                "P(A ∩ B) = P(A) * P(B)",
                "P(A ∩ B) = 0",
                "P(A ∩ B) = P(A|B)",
                "P(A ∩ B) = P(A) / P(B)"
            ],
            correct: 1,
            exp: "For independent events, the occurrence of one does not affect the probability of the other. The probability of both occurring is the simple product of their individual probabilities."
        },
        {
            q: "If events A and B are mutually exclusive, what is P(A ∩ B)?",
            options: [
                "P(A ∩ B) = P(A) * P(B)",
                "P(A ∩ B) = 0",
                "P(A ∩ B) = 1.0",
                "P(A ∩ B) = P(A) + P(B)"
            ],
            correct: 1,
            exp: "Mutually exclusive events cannot occur at the same time. The probability of their intersection is exactly 0."
        }
    ],
    7: [
        {
            q: "What is the Prior Probability P(A) in Bayes' Theorem?",
            options: [
                "The updated probability of hypothesis A after seeing evidence B.",
                "The probability of observing evidence B given hypothesis A.",
                "The baseline probability of hypothesis A before seeing any evidence.",
                "The total probability of the evidence occurring."
            ],
            correct: 2,
            exp: "The Prior Probability P(A) is our initial estimate of the likelihood of hypothesis A before observing any data or evidence."
        },
        {
            q: "What is Laplace Smoothing used for in a Naive Bayes Classifier?",
            options: [
                "To reduce the number of features in text datasets.",
                "To prevent conditional probabilities from becoming absolute zero when encountering words not present in the training set.",
                "To speed up text tokenization.",
                "To normalise log-probabilities into symmetric ranges."
            ],
            correct: 1,
            exp: "If a word never appears in the training set for a class, its probability is 0. Since we multiply probabilities, this zeros-out the entire score. Laplace smoothing adds 1 to count occurrences to prevent this."
        },
        {
            q: "Explain the Base Rate Fallacy.",
            options: [
                "The mistake of ignoring the general frequency of an event (prior) when evaluating diagnostic test results.",
                "Assuming that a model with high precision always has high recall.",
                "Assuming correlation implies causation.",
                "Confusing sample variance with population variance."
            ],
            correct: 0,
            exp: "The Base Rate Fallacy occurs when humans evaluate the probability of a condition based on a test result while ignoring how rare the condition is in the general population (the prior)."
        }
    ],
    8: [
        {
            q: "What is a continuous random variable?",
            options: [
                "A variable that can only take on integer counts.",
                "A variable that can take on an infinite number of values within a range (e.g., transaction dollar amount).",
                "A variable with a variance of absolute zero.",
                "A string-based category column."
            ],
            correct: 1,
            exp: "Continuous random variables can take on any real-valued number in an interval, such as time, weight, or currency value."
        },
        {
            q: "What is the Expected Value of a discrete random variable?",
            options: [
                "The median value of the variable.",
                "The most frequently occurring value (mode).",
                "The sum of all possible values multiplied by their respective probabilities.",
                "The square root of variance."
            ],
            correct: 2,
            exp: "The Expected Value E[X] represents the weighted average of all outcomes, calculated as: Sum of (x_i * P(x_i))."
        },
        {
            q: "Why is Customer Lifetime Value (CLV) modeled using expected values?",
            options: [
                "Because CLV is constant for all users.",
                "Because future customer retention and transaction levels are uncertain, requiring probabilistic discounting.",
                "Because standard scaling doesn't work on user cohorts.",
                "To force the values into normal bell-curves."
            ],
            correct: 1,
            exp: "CLV is a future projection. Since customers churn at random points, we multiply the probability of them staying each year by the revenue they generate, summing these expected values."
        }
    ],
    9: [
        {
            q: "Which distribution is best suited to model the count of events occurring in a fixed time interval (e.g. support tickets arriving per minute)?",
            options: [
                "Normal Distribution",
                "Binomial Distribution",
                "Poisson Distribution",
                "Exponential Distribution"
            ],
            correct: 2,
            exp: "The Poisson distribution models the number of independent events occurring in a fixed interval of time or space, given a constant average rate λ."
        },
        {
            q: "The Binomial distribution models success counts under what conditions?",
            options: [
                "An open interval with unknown parameters.",
                "A fixed number of independent trials, each with only two outcomes and a constant probability of success.",
                "Continuous values that are normally distributed.",
                "Highly correlated features."
            ],
            correct: 1,
            exp: "A Binomial distribution B(n, p) requires a fixed number of trials (n), independent events, binary outcomes (success/failure), and a constant success probability (p)."
        },
        {
            q: "What unique constraint does the Poisson distribution have regarding its parameters?",
            options: [
                "The mean and standard deviation are equal.",
                "The mean and variance are both equal to λ.",
                "The skewness is always negative.",
                "The kurtosis is always exactly 0."
            ],
            correct: 1,
            exp: "In a pure Poisson distribution, the mean (average arrival rate) is mathematically equal to the variance: E[X] = Var(X) = λ."
        }
    ],
    10: [
        {
            q: "Which activation function is used to map a multi-class neural network raw score output to a normalized probability distribution?",
            options: [
                "Sigmoid function",
                "Softmax function",
                "ReLU function",
                "Tanh function"
            ],
            correct: 1,
            exp: "The Softmax function normalizes a vector of raw scores (logits) into a probability distribution over multiple classes, ensuring all elements sum to exactly 1.0."
        },
        {
            q: "What is a Calibrated probability classification model?",
            options: [
                "A model that achieved 100% accuracy.",
                "A model where the predicted probability matches the actual observed frequency of occurrences.",
                "A model trained with a log-transformed target.",
                "A model containing no collinear features."
            ],
            correct: 1,
            exp: "A model is calibrated if its predicted probability corresponds to real-world frequencies (e.g., out of 100 predictions labeled with a probability of 0.80, exactly 80 are true positives)."
        },
        {
            q: "If False Negatives are extremely costly or dangerous (e.g., cancer diagnosis), how should we adjust our classification threshold?",
            options: [
                "Keep it at the default 0.50.",
                "Increase the threshold to 0.90 to make the model certain.",
                "Decrease the threshold (e.g., to 0.10) to make the model highly sensitive to positive cases.",
                "Drop all features and retrain."
            ],
            correct: 2,
            exp: "Decreasing the classification threshold makes the model flag positive cases far more easily. This reduces False Negatives (missing a positive case) at the cost of increasing False Positives."
        }
    ],
    
    // PART 2: Machine Learning Core (11-16)
    11: [
        {
            q: "Which scaling method shifts and rescales data so it has a mean of 0 and a standard deviation of 1?",
            options: [
                "MinMax Scaling",
                "Standardization (StandardScaler)",
                "Robust Scaling",
                "L2 Normalization"
            ],
            correct: 1,
            exp: "Standardization subtracts the mean and divides by the standard deviation, leaving the feature centered at 0 with unit variance."
        },
        {
            q: "What is a severe danger of One-Hot Encoding a feature with 500 unique categories (e.g. ZIP code)?",
            options: [
                "It causes data scaling overflow.",
                "It introduces the 'Curse of Dimensionality', creating 500 sparse binary columns which can lead to severe model overfitting.",
                "It forces the model to assume categories are ordinal.",
                "It deletes missing values automatically."
            ],
            correct: 1,
            exp: "One-hot encoding high-cardinality features drastically increases the feature space dimensions, making the model prone to memorizing training noise."
        },
        {
            q: "Lasso regression (L1 regularization) can be used for feature selection because it:",
            options: [
                "Scales all features to [0, 1].",
                "Estimates the median values of features.",
                "Forces the weights of non-informative features to absolute zero.",
                "Inverts target skewness."
            ],
            correct: 2,
            exp: "L1 regularization adds an absolute weight penalty to the loss function, which mathematically drives non-essential weights to exactly zero, effectively selecting features."
        }
    ],
    12: [
        {
            q: "How does the training process of XGBoost differ from Random Forest?",
            options: [
                "Random Forest trains trees sequentially; XGBoost trains them in parallel.",
                "XGBoost trains trees sequentially, where each new tree corrects the residual errors of the prior ones; Random Forest trains independent trees in parallel.",
                "Random Forest uses gradient descent; XGBoost uses bootstrap bagging.",
                "XGBoost requires scaled features; Random Forest does not."
            ],
            correct: 1,
            exp: "XGBoost is a boosting method (sequential correction of residuals), while Random Forest is a bagging method (parallel averaging of bootstrap samples)."
        },
        {
            q: "If a decision tree model achieves 100% accuracy on the training set but only 55% on the test set, it has:",
            options: [
                "High Bias (Underfit)",
                "Low Variance (Ideal fit)",
                "High Variance (Overfit)",
                "Class Imbalance"
            ],
            correct: 2,
            exp: "A model that memorizes training data (100%) but fails to generalize on test data (55%) suffers from high variance (overfitting)."
        },
        {
            q: "What is the purpose of the 'kernel trick' in Support Vector Machines?",
            options: [
                "It randomly drops features to speed up training.",
                "It maps non-linearly separable data into a higher-dimensional space where a linear decision boundary can separate the classes, without explicitly computing high-dimensional coordinates.",
                "It log-transforms the target variable automatically.",
                "It performs cross-validation in parallel."
            ],
            correct: 1,
            exp: "The kernel trick computes inner products in high-dimensional space implicitly, allowing SVMs to solve complex non-linear classification boundaries efficiently."
        }
    ],
    13: [
        {
            q: "What evaluation metric is commonly used to find the optimal cluster count K in K-Means clustering?",
            options: [
                "Accuracy Score",
                "Silhouette Score or Elbow Method (Inertia)",
                "Log Loss",
                "Root Mean Squared Error"
            ],
            correct: 1,
            exp: "The Elbow Method (plotting inertia/within-cluster sum of squares) and Silhouette Analysis (measuring cluster separation) are standard metrics for evaluating cluster count quality."
        },
        {
            q: "Which unsupervised method is designed specifically to detect anomalies by isolating data points through random feature splits?",
            options: [
                "Principal Component Analysis (PCA)",
                "Hierarchical Clustering",
                "Isolation Forest",
                "DBSCAN"
            ],
            correct: 2,
            exp: "Isolation Forest isolates anomalies by randomly partitioning features. Anomalies require fewer splits (shorter path lengths) to isolate than normal points, making them easy to identify."
        },
        {
            q: "PCA is a dimensionality reduction technique that projects features onto components that maximize:",
            options: [
                "Euclidean distance",
                "Classification Accuracy",
                "Explained Variance",
                "Gini Impurity"
            ],
            correct: 2,
            exp: "PCA projects high-dimensional data onto orthogonal components designed to capture and maximize the explained variance of the dataset."
        }
    ],
    14: [
        {
            q: "In an imbalanced dataset with 1% positive fraud cases, why is Accuracy a poor metric?",
            options: [
                "It is mathematically impossible to calculate accuracy on floats.",
                "A dummy model predicting 'Legitimate' for everything achieves 99% accuracy while catching 0% of the fraud cases.",
                "Accuracy is only used for unsupervised regression.",
                "It requires standard scaling first."
            ],
            correct: 1,
            exp: "Accuracy counts total correct predictions. For highly rare classes, predicting the majority class for all samples yields a high accuracy score while failing to find any positive events."
        },
        {
            q: "What is the R² Score (Coefficient of Determination) in regression models?",
            options: [
                "The average absolute distance between predictions and actuals.",
                "The square root of Mean Squared Error.",
                "The proportion of target variance that is predictable from the features.",
                "The likelihood of class occurrence."
            ],
            correct: 2,
            exp: "R² measures the proportion of variance in the dependent variable explained by the regression model, ranging from negative values (worse than mean) up to 1.0 (perfect fit)."
        },
        {
            q: "What is the difference between Precision and Recall?",
            options: [
                "Precision measures how many actual positives were caught; Recall measures how many predicted positives were correct.",
                "Precision measures the fraction of correct positive alerts; Recall measures the fraction of actual positive cases caught by the model.",
                "Precision is for classification; Recall is for regression.",
                "They are mathematically identical."
            ],
            correct: 1,
            exp: "Precision = TP/(TP+FP) (avoiding false alarms). Recall = TP/(TP+FN) (catching all actual positive events)."
        }
    ],
    15: [
        {
            q: "What is the advantage of RandomizedSearchCV over GridSearchCV?",
            options: [
                "It is guaranteed to find the absolute best parameter combination.",
                "It randomly samples combinations from distributions, running a fixed number of iterations, which is far faster and computationally efficient in high-dimensional spaces.",
                "It doesn't require cross-validation.",
                "It runs without training the estimator."
            ],
            correct: 1,
            exp: "Grid Search exhaustively trains models on all combinations, which scales poorly. Random Search samples widely, finding near-optimal parameters in a fraction of the time."
        },
        {
            q: "What is the role of L2 regularization (Ridge) in model optimization?",
            options: [
                "It forces non-informative coefficients to exactly zero.",
                "It adds a squared weight penalty to the loss function, shrinking weights close to zero, which distributes importance and prevents overfitting.",
                "It normalizes features to [0, 1].",
                "It speeds up tree split times."
            ],
            correct: 1,
            exp: "L2 regularization prevents any single feature from having a massive weight, shrinking coefficients uniformly to stabilize linear models."
        },
        {
            q: "In tuning boosted trees, what is 'Early Stopping' used for?",
            options: [
                "Terminating training when validation set performance stops improving, saving compute resources and preventing overfitting.",
                "Stopping predictions when latency is too high.",
                "Clipping outlier values at the root node.",
                "Dropping features during cross-validation."
            ],
            correct: 0,
            exp: "Early stopping stops tree additions once validation loss plateaus, ensuring the model doesn't continue training and start memorizing training set noise."
        }
    ],
    16: [
        {
            q: "Why is a Scikit-Learn ColumnTransformer crucial in preprocessing?",
            options: [
                "It compiles the code to C++ for faster execution.",
                "It allows applying different preprocessing steps (like scaling vs. one-hot encoding) to specific columns in parallel, returning a unified matrix.",
                "It runs PCA reduction on categorical variables.",
                "It acts as the final classification estimator."
            ],
            correct: 1,
            exp: "ColumnTransformer targets specific feature types (numeric, categorical) with separate parallel transformers, making complex dataset processing modular."
        },
        {
            q: "What package is commonly used in Scikit-Learn pipelines to save (serialize) models to disk?",
            options: [
                "NumPy",
                "Joblib",
                "Pandas",
                "PyTest"
            ],
            correct: 1,
            exp: "Joblib is optimized for serializing large NumPy arrays, making it the standard choice for saving and loading Scikit-Learn pipelines."
        },
        {
            q: "Why does wrapping transformers and estimators in a Pipeline prevent 'Data Leakage' during cross-validation?",
            options: [
                "It encrypts the features to prevent access.",
                "It guarantees that preprocessing scaling parameters are computed *only* on the training folds inside each cross-validation loop, rather than leaking validation fold statistics.",
                "It normalizes target variables automatically.",
                "It deletes outliers from the validation folds."
            ],
            correct: 1,
            exp: "If you scale the whole dataset before cross-validation, validation statistics leak into training. A Pipeline ensures `fit` is called only on training folds during folds evaluation."
        }
    ]
};

// Global variables for calculations
let activeModuleForQuiz = 1;
let currentQuestionIndex = 0;
let userAnswers = [];

// DOMContentLoaded Initialisation
document.addEventListener("DOMContentLoaded", () => {
    setupTabNavigation();
    setupQuizEngine();
    setupCalculators();
    
    // Initial renders for visualizers
    renderNormalCurve(); 
    runScalerSimulator();
    renderRegressionFitting();
    runMatrixMetrics();
    renderLearningCurve();
});

// Sidebar & Page Navigation Router
function setupTabNavigation() {
    const navItems = document.querySelectorAll(".nav-item");
    const pages = document.querySelectorAll(".page-view");
    
    navItems.forEach(item => {
        item.addEventListener("click", () => {
            const targetPageId = item.getAttribute("data-page");
            
            // Toggle active navigation classes
            navItems.forEach(i => i.classList.remove("active"));
            item.classList.add("active");
            
            // Toggle visible content views
            pages.forEach(p => p.style.display = "none");
            
            const targetPage = document.getElementById(targetPageId);
            if (targetPage) {
                targetPage.style.display = "block";
                targetPage.classList.add("animate-fade-in");
                setTimeout(() => targetPage.classList.remove("animate-fade-in"), 400);
            }
        });
    });
}

// Quizzes Engine Logic
function setupQuizEngine() {
    const select = document.getElementById("quiz-module-select");
    
    // Change selected quiz module
    select.addEventListener("change", (e) => {
        activeModuleForQuiz = parseInt(e.target.value);
        startQuiz();
    });
    
    startQuiz();
}

function startQuiz() {
    currentQuestionIndex = 0;
    userAnswers = [];
    showQuizQuestion();
}

function showQuizQuestion() {
    const quizContent = document.getElementById("quiz-questions-container");
    const progressText = document.getElementById("quiz-progress-text");
    
    const questions = quizzes[activeModuleForQuiz];
    const qData = questions[currentQuestionIndex];
    
    progressText.innerText = `Question ${currentQuestionIndex + 1} of ${questions.length}`;
    
    let optionsHtml = qData.options.map((opt, idx) => `
        <div class="quiz-option" onclick="handleOptionSelect(${idx})">
            ${opt}
        </div>
    `).join("");
    
    quizContent.innerHTML = `
        <div class="quiz-question-card">
            <div class="quiz-question-text">${qData.q}</div>
            <div class="quiz-options">${optionsHtml}</div>
            <div id="quiz-feedback-box" style="display:none;"></div>
            <div style="margin-top: 1.5rem; text-align: right;">
                <button class="btn-primary" id="quiz-next-btn" style="display:none;" onclick="handleNextQuestion()">
                    ${currentQuestionIndex === questions.length - 1 ? 'Finish Quiz' : 'Next Question'}
                </button>
            </div>
        </div>
    `;
}

window.handleOptionSelect = function(selectedIndex) {
    const questions = quizzes[activeModuleForQuiz];
    const qData = questions[currentQuestionIndex];
    
    const options = document.querySelectorAll(".quiz-option");
    
    options.forEach(opt => opt.removeAttribute("onclick"));
    
    options.forEach((opt, idx) => {
        if (idx === qData.correct) {
            opt.classList.add("correct");
        } else if (idx === selectedIndex) {
            opt.classList.add("incorrect");
        }
    });
    
    const feedbackBox = document.getElementById("quiz-feedback-box");
    feedbackBox.innerHTML = `
        <div class="quiz-explanation">
            <strong>${selectedIndex === qData.correct ? '✓ Correct!' : '✗ Incorrect.'}</strong> 
            ${qData.exp}
        </div>
    `;
    feedbackBox.style.display = "block";
    
    document.getElementById("quiz-next-btn").style.display = "inline-block";
    userAnswers.push(selectedIndex === qData.correct);
};

window.handleNextQuestion = function() {
    const questions = quizzes[activeModuleForQuiz];
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        showQuizQuestion();
    } else {
        showQuizResults();
    }
};

function showQuizResults() {
    const quizContent = document.getElementById("quiz-questions-container");
    const progressText = document.getElementById("quiz-progress-text");
    const questions = quizzes[activeModuleForQuiz];
    
    const correctCount = userAnswers.filter(x => x).length;
    const scorePct = Math.round((correctCount / questions.length) * 100);
    
    progressText.innerText = "Quiz Completed";
    
    quizContent.innerHTML = `
        <div class="quiz-question-card" style="text-align: center;">
            <div class="quiz-question-text">Quiz Results Summary</div>
            <div style="font-size: 3rem; font-weight: 700; color: var(--accent-purple); margin-bottom: 1rem;">
                ${scorePct}%
            </div>
            <p style="color: var(--text-muted); margin-bottom: 1.5rem;">
                You answered <strong>${correctCount}</strong> out of <strong>${questions.length}</strong> questions correctly.
            </p>
            <button class="btn-primary" onclick="startQuiz()">Try Again</button>
        </div>
    `;
}

// Interactive Simulators Setup
function setupCalculators() {
    // 1. A/B Testing Inputs
    const abInputs = ["ab-n-a", "ab-c-a", "ab-n-b", "ab-c-b"];
    abInputs.forEach(id => {
        document.getElementById(id).addEventListener("input", runABSimulator);
    });
    runABSimulator();
    
    // 2. Bayes Theorem Inputs
    const bayesInputs = ["bayes-prior", "bayes-sens", "bayes-fpr"];
    bayesInputs.forEach(id => {
        document.getElementById(id).addEventListener("input", runBayesSimulator);
    });
    runBayesSimulator();
    
    // 3. Distribution Adjustment Inputs
    document.getElementById("dist-skew").addEventListener("input", (e) => {
        document.getElementById("dist-skew-val").innerText = parseFloat(e.target.value).toFixed(1);
        renderNormalCurve();
    });
    document.getElementById("dist-kurt").addEventListener("input", (e) => {
        document.getElementById("dist-kurt-val").innerText = parseFloat(e.target.value).toFixed(1);
        renderNormalCurve();
    });
    
    // 4. Correlation Interactive Inputs
    const cells = document.querySelectorAll(".corr-input");
    cells.forEach(cell => {
        cell.addEventListener("input", (e) => {
            let val = parseFloat(e.target.value);
            if (isNaN(val)) val = 0.0;
            if (val > 1.0) val = 1.0;
            if (val < -1.0) val = -1.0;
            e.target.value = val;
            
            colorMatrixCell(e.target, val);
            checkCollinearity();
        });
        colorMatrixCell(cell, parseFloat(cell.value));
    });
    checkCollinearity();
    
    // 5. Churn Pricing Optimiser Inputs
    const churnInputs = ["churn-thresh", "churn-clv", "churn-incentive"];
    churnInputs.forEach(id => {
        document.getElementById(id).addEventListener("input", runChurnOptimizer);
    });
    runChurnOptimizer();

    // 6. ML Scaling Simulator Inputs
    document.getElementById("scaler-raw-inputs").addEventListener("input", runScalerSimulator);
    document.getElementById("scaler-type-select").addEventListener("change", runScalerSimulator);

    // 7. ML Regression Fitting Canvas Inputs
    document.getElementById("reg-noise").addEventListener("input", (e) => {
        document.getElementById("reg-noise-val").innerText = e.target.value;
        renderRegressionFitting();
    });
    document.getElementById("reg-model-select").addEventListener("change", renderRegressionFitting);

    // 8. ML Confusion Matrix Inputs
    const matrixInputs = ["matrix-tp", "matrix-fp", "matrix-fn", "matrix-tn"];
    matrixInputs.forEach(id => {
        document.getElementById(id).addEventListener("input", runMatrixMetrics);
    });

    // 9. ML HPO Learning Curve Canvas Inputs
    document.getElementById("hpo-depth").addEventListener("input", (e) => {
        document.getElementById("hpo-depth-val").innerText = e.target.value;
        renderLearningCurve();
    });
}

// 1. A/B Testing Proportions Z-Test Simulator
function runABSimulator() {
    const nA = parseInt(document.getElementById("ab-n-a").value) || 1000;
    const cA = parseInt(document.getElementById("ab-c-a").value) || 50;
    const nB = parseInt(document.getElementById("ab-n-b").value) || 1000;
    const cB = parseInt(document.getElementById("ab-c-b").value) || 68;
    
    const pA = cA / nA;
    const pB = cB / nB;
    
    document.getElementById("res-p-a").innerText = `${(pA * 100).toFixed(2)}%`;
    document.getElementById("res-p-b").innerText = `${(pB * 100).toFixed(2)}%`;
    
    const pPooled = (cA + cB) / (nA + nB);
    const se = Math.sqrt(pPooled * (1 - pPooled) * (1/nA + 1/nB));
    
    let zStat = 0.0;
    let pValue = 1.0;
    if (se > 0) {
        zStat = (pB - pA) / se;
        pValue = 2 * (1 - normalCDF(Math.abs(zStat)));
    }
    
    document.getElementById("res-z").innerText = zStat.toFixed(4);
    
    const pValueEl = document.getElementById("res-pval");
    pValueEl.innerText = pValue.toFixed(6);
    
    const decisionEl = document.getElementById("res-decision");
    if (pValue < 0.05) {
        pValueEl.className = "result-value significant";
        decisionEl.innerText = "Significant! Reject Null Hypothesis.";
        decisionEl.style.color = "var(--accent-emerald)";
    } else {
        pValueEl.className = "result-value not-significant";
        decisionEl.innerText = "Not Significant. Fail to Reject.";
        decisionEl.style.color = "var(--text-muted)";
    }
}

function normalCDF(x) {
    const p = 0.2316419;
    const b1 = 0.319381530;
    const b2 = -0.356563782;
    const b3 = 1.781477937;
    const b4 = -1.821255978;
    const b5 = 1.330274429;
    
    const t = 1 / (1 + p * Math.abs(x));
    const sigma = 1 - (1 / Math.sqrt(2 * Math.PI)) * Math.exp(-x * x / 2) * 
                  (b1 * t + b2 * t*t + b3 * Math.pow(t,3) + b4 * Math.pow(t,4) + b5 * Math.pow(t,5));
    return x >= 0 ? sigma : 1 - sigma;
}

// 2. Bayes Theorem Simulator
function runBayesSimulator() {
    const prior = parseFloat(document.getElementById("bayes-prior").value);
    const sens = parseFloat(document.getElementById("bayes-sens").value);
    const fpr = parseFloat(document.getElementById("bayes-fpr").value);
    
    document.getElementById("bayes-prior-val").innerText = prior.toFixed(3);
    document.getElementById("bayes-sens-val").innerText = sens.toFixed(2);
    document.getElementById("bayes-fpr-val").innerText = fpr.toFixed(2);
    
    const numerator = sens * prior;
    const denominator = (sens * prior) + (fpr * (1 - prior));
    const posterior = denominator > 0 ? numerator / denominator : 0.0;
    
    document.getElementById("res-bayes-post").innerText = `${(posterior * 100).toFixed(2)}%`;
    document.getElementById("res-bayes-evidence").innerText = `${(denominator * 100).toFixed(2)}%`;
}

// 3. Distribution Curve Simulator
function renderNormalCurve() {
    const canvas = document.getElementById("dist-chart-canvas");
    if (!canvas) return;
    
    const ctx = canvas.getContext("2d");
    const width = canvas.width;
    const height = canvas.height;
    ctx.clearRect(0, 0, width, height);
    
    const skew = parseFloat(document.getElementById("dist-skew").value);
    const kurt = parseFloat(document.getElementById("dist-kurt").value);
    
    const points = [];
    const step = 1;
    const mean = width / 2;
    const stdDev = (kurt > 0) ? 60 / (1 + kurt * 0.4) : 60 * (1 - kurt * 0.2);
    
    for (let x = 20; x < width - 20; x += step) {
        let z = (x - mean) / stdDev;
        let skewedZ = z;
        if (skew > 0) {
            skewedZ = z * (1 - skew * 0.12 * z);
        } else if (skew < 0) {
            skewedZ = z * (1 + Math.abs(skew) * 0.12 * z);
        }
        
        let pdf = (1 / (Math.sqrt(2 * Math.PI))) * Math.exp(-0.5 * skewedZ * skewedZ);
        if (kurt > 0) {
            pdf = pdf * (1 + kurt * 0.2);
        }
        
        const canvasY = height - 30 - (pdf * 200);
        points.push({ x, y: canvasY });
    }
    
    ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(20, height - 30);
    ctx.lineTo(width - 20, height - 30);
    ctx.stroke();
    
    ctx.strokeStyle = "var(--accent-purple)";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);
    for (let i = 1; i < points.length; i++) {
        ctx.lineTo(points[i].x, points[i].y);
    }
    ctx.stroke();
    
    const gradient = ctx.createLinearGradient(0, 0, 0, height);
    gradient.addColorStop(0, "rgba(139, 92, 246, 0.3)");
    gradient.addColorStop(1, "rgba(139, 92, 246, 0.0)");
    
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.moveTo(points[0].x, height - 30);
    for (let i = 0; i < points.length; i++) {
        ctx.lineTo(points[i].x, points[i].y);
    }
    ctx.lineTo(points[points.length - 1].x, height - 30);
    ctx.closePath();
    ctx.fill();
}

// 4. Matrix Colorizer
function colorMatrixCell(inputEl, val) {
    let r = 0, g = 0, b = 0, opacity = Math.abs(val);
    if (val > 0) {
        r = 236; g = 72; b = 153;
    } else {
        r = 59; g = 130; b = 246;
    }
    inputEl.parentElement.style.backgroundColor = `rgba(${r}, ${g}, ${b}, ${opacity * 0.4})`;
}

function checkCollinearity() {
    const val1 = parseFloat(document.getElementById("corr-r1").value) || 0.0;
    const reportBox = document.getElementById("res-collinear-report");
    
    if (Math.abs(val1) >= 0.80) {
        reportBox.innerHTML = `
            <div style="color: var(--accent-pink); font-weight: bold; margin-bottom: 0.5rem;">
                ⚠ High Collinearity Detected (r = ${val1.toFixed(2)})
            </div>
            <p style="font-size: 0.85rem; color: var(--text-muted);">
                Living Area and Room count contain redundant variables. Keeping both in linear models will yield unstable regression weights. Recommend dropping Room count.
            </p>
        `;
    } else {
        reportBox.innerHTML = `
            <div style="color: var(--accent-emerald); font-weight: bold; margin-bottom: 0.5rem;">
                ✓ Multi-feature Stability Confirmed
            </div>
            <p style="font-size: 0.85rem; color: var(--text-muted);">
                Features are within safe boundaries (r = ${val1.toFixed(2)}). Coefficients will remain stable.
            </p>
        `;
    }
}

// 5. Churn Pricing Optimiser
function runChurnOptimizer() {
    const threshold = parseFloat(document.getElementById("churn-thresh").value);
    const clv = parseFloat(document.getElementById("churn-clv").value) || 150;
    const cost = parseFloat(document.getElementById("churn-incentive").value) || 15;
    
    document.getElementById("churn-thresh-val").innerText = threshold.toFixed(2);
    
    let tp = 0, fp = 0, fn = 0, tn = 0;
    const seed_loyal = 200;
    const seed_churn = 100;
    
    for (let i = 0; i < seed_loyal; i++) {
        let prob = 0.25 + 0.18 * Math.sin(i * 0.4) + 0.1 * Math.cos(i * 0.9);
        prob = Math.max(0, Math.min(1, prob));
        if (prob >= threshold) fp++;
        else tn++;
    }
    for (let i = 0; i < seed_churn; i++) {
        let prob = 0.65 + 0.15 * Math.sin(i * 0.5) + 0.12 * Math.cos(i * 0.7);
        prob = Math.max(0, Math.min(1, prob));
        if (prob >= threshold) tp++;
        else fn++;
    }
    
    const tp_val = 0.75 * (clv - cost) + 0.25 * (-clv);
    const fp_val = -cost;
    
    const netSavings = (tp * tp_val) + (fp * fp_val) + (fn * -clv);
    const baseline = seed_churn * (-clv);
    
    document.getElementById("res-churn-tp").innerText = tp;
    document.getElementById("res-churn-fp").innerText = fp;
    document.getElementById("res-churn-fn").innerText = fn;
    document.getElementById("res-churn-savings").innerText = `$${netSavings.toLocaleString('en-US', {maximumFractionDigits:0})}`;
    
    const improvement = netSavings - baseline;
    const netEl = document.getElementById("res-churn-net");
    netEl.innerText = `$${improvement.toLocaleString('en-US', {maximumFractionDigits:0})}`;
    
    if (improvement > 0) {
        netEl.style.color = "var(--accent-emerald)";
    } else {
        netEl.style.color = "var(--accent-pink)";
    }
}

// 6. ML Scaling Simulator
function runScalerSimulator() {
    const rawInputText = document.getElementById("scaler-raw-inputs").value;
    const scaleType = document.getElementById("scaler-type-select").value;
    const outputListEl = document.getElementById("scaler-output-list");
    
    // Parse values
    const values = rawInputText.split(",").map(val => parseFloat(val.trim())).filter(val => !isNaN(val));
    
    if (values.length === 0) {
        outputListEl.innerHTML = "<p style='color:var(--accent-pink); font-size:0.85rem;'>Please enter valid numerical inputs</p>";
        return;
    }
    
    let outputs = [];
    if (scaleType === "standard") {
        const mean = values.reduce((s, x) => s + x, 0) / values.length;
        const variance = values.reduce((s, x) => s + Math.pow(x - mean, 2), 0) / values.length;
        const std = Math.sqrt(variance) || 1.0;
        outputs = values.map(x => (x - mean) / std);
    } else if (scaleType === "minmax") {
        const min = Math.min(...values);
        const max = Math.max(...values);
        const range = (max - min) || 1.0;
        outputs = values.map(x => (x - min) / range);
    }
    
    outputListEl.innerHTML = values.map((val, idx) => `
        <div style="display:flex; justify-content:space-between; font-size:0.85rem; border-bottom:1px solid rgba(255,255,255,0.03); padding:0.25rem 0;">
            <span style="color:var(--text-muted);">Raw: ${val}</span>
            <span style="color:var(--accent-cyan); font-weight:bold;">Scaled: ${outputs[idx].toFixed(4)}</span>
        </div>
    `).join("");
}

// 7. ML Regression Fitting Canvas
function renderRegressionFitting() {
    const canvas = document.getElementById("reg-fit-canvas");
    if (!canvas) return;
    
    const ctx = canvas.getContext("2d");
    const width = canvas.width;
    const height = canvas.height;
    ctx.clearRect(0, 0, width, height);
    
    const noiseLevel = parseFloat(document.getElementById("reg-noise").value);
    const modelType = document.getElementById("reg-model-select").value;
    
    // Generate simulated coordinates along a curved sinusoidal slope
    const points = [];
    const nPoints = 30;
    
    // Fixed seed mapping for points coordinates to prevent jumping
    for (let i = 0; i < nPoints; i++) {
        let x = 40 + (i * (width - 80) / (nPoints - 1));
        // Target curve: y = sin(x)
        let normalizedX = (x - 40) / (width - 80) * Math.PI * 1.5;
        let base_y = height / 2 + Math.sin(normalizedX) * 60;
        
        // Add random seed noise
        let noiseOffset = Math.sin(i * 2.3) * noiseLevel * 2;
        let y = base_y + noiseOffset;
        points.push({ x, y });
    }
    
    // Plot coordinates
    ctx.fillStyle = "var(--text-muted)";
    points.forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, 4, 0, 2 * Math.PI);
        ctx.fill();
    });
    
    // Fit and Draw Regression Curve
    ctx.lineWidth = 3;
    
    if (modelType === "linear") {
        // Fits a simple OLS linear slope
        ctx.strokeStyle = "var(--accent-pink)";
        // Simple OLS fit solver
        let xMean = points.reduce((s, p) => s + p.x, 0) / nPoints;
        let yMean = points.reduce((s, p) => s + p.y, 0) / nPoints;
        
        let num = 0, den = 0;
        points.forEach(p => {
            num += (p.x - xMean) * (p.y - yMean);
            den += Math.pow(p.x - xMean, 2);
        });
        let slope = num / (den || 1.0);
        let intercept = yMean - slope * xMean;
        
        ctx.beginPath();
        ctx.moveTo(20, slope * 20 + intercept);
        ctx.lineTo(width - 20, slope * (width - 20) + intercept);
        ctx.stroke();
        
    } else if (modelType === "tree") {
        // Fits a step function representing a Decision Tree splits
        ctx.strokeStyle = "var(--accent-cyan)";
        ctx.beginPath();
        
        // Let's divide canvas horizontally into 4 partition leaves
        const partitions = [
            { start: 0, end: width * 0.25 },
            { start: width * 0.25, end: width * 0.5 },
            { start: width * 0.5, end: width * 0.75 },
            { start: width * 0.75, end: width }
        ];
        
        partitions.forEach((part, idx) => {
            let partPoints = points.filter(p => p.x >= part.start && p.x < part.end);
            if (partPoints.length === 0) return;
            let avgY = partPoints.reduce((s, p) => s + p.y, 0) / partPoints.length;
            
            if (idx === 0) {
                ctx.moveTo(part.start + 10, avgY);
            }
            ctx.lineTo(part.start, avgY);
            ctx.lineTo(part.end, avgY);
        });
        ctx.stroke();
    }
}

// 8. ML Confusion Matrix calculator
function runMatrixMetrics() {
    const tp = parseInt(document.getElementById("matrix-tp").value) || 0;
    const fp = parseInt(document.getElementById("matrix-fp").value) || 0;
    const fn = parseInt(document.getElementById("matrix-fn").value) || 0;
    const tn = parseInt(document.getElementById("matrix-tn").value) || 0;
    
    const total = tp + fp + fn + tn;
    
    let accuracy = 0.0;
    let precision = 0.0;
    let recall = 0.0;
    let f1 = 0.0;
    
    if (total > 0) {
        accuracy = (tp + tn) / total;
        if (tp + fp > 0) precision = tp / (tp + fp);
        if (tp + fn > 0) recall = tp / (tp + fn);
        if (precision + recall > 0) f1 = 2 * (precision * recall) / (precision + recall);
    }
    
    document.getElementById("res-matrix-acc").innerText = `${(accuracy * 100).toFixed(1)}%`;
    document.getElementById("res-matrix-prec").innerText = `${(precision * 100).toFixed(1)}%`;
    document.getElementById("res-matrix-rec").innerText = `${(recall * 100).toFixed(1)}%`;
    document.getElementById("res-matrix-f1").innerText = `${(f1 * 100).toFixed(1)}%`;
    
    // Draw basic ROC curve visualization based on TPR (Recall) and FPR
    renderROCCanvas(recall, (fp + tn > 0) ? fp / (fp + tn) : 0.0);
}

function renderROCCanvas(tpr, fpr) {
    const canvas = document.getElementById("matrix-roc-canvas");
    if (!canvas) return;
    
    const ctx = canvas.getContext("2d");
    const width = canvas.width;
    const height = canvas.height;
    ctx.clearRect(0, 0, width, height);
    
    // Draw random guess diagonal
    ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(20, height - 20);
    ctx.lineTo(width - 20, 20);
    ctx.stroke();
    
    // Draw ROC curve path using points coordinates (quadratic bezier mapping)
    // starts at (0, 0) -> (FPR, TPR) -> (1, 1)
    const startX = 20;
    const startY = height - 20;
    const endX = width - 20;
    const endY = 20;
    
    // Scale coordinates
    const ptX = startX + fpr * (endX - startX);
    const ptY = startY - tpr * (startY - endY);
    
    ctx.strokeStyle = "var(--accent-pink)";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(startX, startY);
    // Draw quadratic curve passing through current threshold point
    ctx.quadraticCurveTo(20, 20, endX, endY);
    ctx.stroke();
    
    // Plot current point indicator
    ctx.fillStyle = "var(--accent-cyan)";
    ctx.beginPath();
    ctx.arc(ptX, ptY, 6, 0, 2 * Math.PI);
    ctx.fill();
    
    // Labels
    ctx.fillStyle = "var(--text-muted)";
    ctx.font = "9px Outfit";
    ctx.fillText("FPR", width - 35, height - 5);
    ctx.fillText("TPR", 2, 15);
}

// 9. ML HPO Learning Curves Canvas
function renderLearningCurve() {
    const canvas = document.getElementById("hpo-chart-canvas");
    if (!canvas) return;
    
    const ctx = canvas.getContext("2d");
    const width = canvas.width;
    const height = canvas.height;
    ctx.clearRect(0, 0, width, height);
    
    const maxDepth = parseInt(document.getElementById("hpo-depth").value);
    
    // Plotting simulated scores as depth increases
    const trainPoints = [];
    const valPoints = [];
    
    // We plot curve for depth = 1 to 10
    const paddingX = 30;
    const paddingY = 20;
    
    for (let depth = 1; depth <= 10; depth++) {
        const x = paddingX + (depth - 1) * (width - 2 * paddingX) / 9;
        
        // Train score goes up asymptotically close to 1.0 (100%)
        let trainScore = 0.55 + 0.45 * (1 - Math.exp(-0.4 * depth));
        
        // Validation score increases, then drops if depth > 5 (overfitting)
        let valScore = 0.50 + 0.35 * (1 - Math.exp(-0.5 * depth));
        if (depth > 4) {
            valScore -= 0.045 * (depth - 4); // Overfitting penalty
        }
        
        // Map scores in [0.4, 1.0] to Y coordinates
        const scaleY = (score) => height - paddingY - (score - 0.4) * (height - 2 * paddingY) / 0.6;
        
        trainPoints.push({ x, y: scaleY(trainScore), score: trainScore });
        valPoints.push({ x, y: scaleY(valScore), score: valScore });
    }
    
    // Axis line
    ctx.strokeStyle = "rgba(255, 255, 255, 0.1)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(paddingX, height - paddingY);
    ctx.lineTo(width - paddingX, height - paddingY);
    ctx.stroke();
    
    // Train Curve
    ctx.strokeStyle = "var(--accent-emerald)";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(trainPoints[0].x, trainPoints[0].y);
    for (let i = 1; i < trainPoints.length; i++) {
        ctx.lineTo(trainPoints[i].x, trainPoints[i].y);
    }
    ctx.stroke();
    
    // Validation Curve
    ctx.strokeStyle = "var(--accent-purple)";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(valPoints[0].x, valPoints[0].y);
    for (let i = 1; i < valPoints.length; i++) {
        ctx.lineTo(valPoints[i].x, valPoints[i].y);
    }
    ctx.stroke();
    
    // Current chosen depth marker line
    const currentX = trainPoints[maxDepth - 1].x;
    ctx.strokeStyle = "rgba(255, 255, 255, 0.25)";
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(currentX, paddingY);
    ctx.lineTo(currentX, height - paddingY);
    ctx.stroke();
    ctx.setLineDash([]); // Reset
    
    // Markers at current depth
    ctx.fillStyle = "var(--accent-emerald)";
    ctx.beginPath();
    ctx.arc(currentX, trainPoints[maxDepth - 1].y, 5, 0, 2 * Math.PI);
    ctx.fill();
    
    ctx.fillStyle = "var(--accent-purple)";
    ctx.beginPath();
    ctx.arc(currentX, valPoints[maxDepth - 1].y, 5, 0, 2 * Math.PI);
    ctx.fill();
    
    // Value text displays
    document.getElementById("res-hpo-train").innerText = `${(trainPoints[maxDepth - 1].score * 100).toFixed(1)}%`;
    document.getElementById("res-hpo-val").innerText = `${(valPoints[maxDepth - 1].score * 100).toFixed(1)}%`;
    
    const hpoStatus = document.getElementById("res-hpo-status");
    if (maxDepth <= 2) {
        hpoStatus.innerText = "Underfitting (Depth too small)";
        hpoStatus.style.color = "var(--accent-orange)";
    } else if (maxDepth >= 7) {
        hpoStatus.innerText = "Overfitting (Train high, Validation drops)";
        hpoStatus.style.color = "var(--accent-pink)";
    } else {
        hpoStatus.innerText = "Optimal Balance (High validation accuracy)";
        hpoStatus.style.color = "var(--accent-emerald)";
    }
}
