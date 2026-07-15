# Module 13: LSTMs (Advanced Sequential Learning)

## 1. Industry Explanation
Vanilla RNNs fail on long sequences because of the **Vanishing Gradient Problem**. They literally "forget" the beginning of a sequence by the time they reach the end.

**Long Short-Term Memory (LSTM)** networks solve this using a complex internal architecture of **Gates** (Forget, Input, Output) and a separate **Cell State**. 
- Think of the **Hidden State** as the short-term memory (what word did I just read?).
- Think of the **Cell State** as the long-term memory (a conveyor belt running straight through the entire sequence, allowing gradients to flow unimpeded without vanishing).

**Industry Reality:** While Transformers dominate NLP (text), **LSTMs are still the industry standard for Time-Series Forecasting** (predicting stock prices, retail demand, IoT sensor anomalies). Transformers are often overkill for numerical time-series data and require far too much memory, making LSTMs the perfect tool for the job.

---

## 2. Why It Matters (The Business Context)
Consider **Retail Demand Forecasting**. A supermarket needs to know exactly how much milk to order for next Tuesday.
If they use a standard regression model, it doesn't understand that sales have a weekly seasonality (Saturdays are always high).
If they use an LSTM, they can feed in a sequence of the last 30 days of sales. The LSTM's "Forget Gate" learns to ignore random daily spikes (like a random Tuesday where someone bought 50 gallons for a party), while its "Input Gate" remembers the strong weekend patterns, producing highly accurate predictions that minimize spoiled inventory.

---

## 3. Python Example (Theory / Conceptual)
*Understanding the LSTM Cell State (The Conveyor Belt).*

```python
import numpy as np

def sigmoid(x): return 1 / (1 + np.exp(-x))
def tanh(x): return np.tanh(x)

# Conceptual LSTM Step
def lstm_step(current_input, prev_hidden_state, prev_cell_state, weights):
    # 1. Forget Gate: What should we delete from long-term memory?
    forget_gate = sigmoid(np.dot(current_input, weights['W_f']) + np.dot(prev_hidden_state, weights['U_f']))
    
    # 2. Input Gate: What new information should we add to long-term memory?
    input_gate = sigmoid(np.dot(current_input, weights['W_i']) + np.dot(prev_hidden_state, weights['U_i']))
    candidate_memory = tanh(np.dot(current_input, weights['W_c']) + np.dot(prev_hidden_state, weights['U_c']))
    
    # Update the Long-Term Memory (The Conveyor Belt)
    # This additive operation is why gradients don't vanish in LSTMs!
    new_cell_state = (forget_gate * prev_cell_state) + (input_gate * candidate_memory)
    
    # 3. Output Gate: What should we output as the new short-term memory?
    output_gate = sigmoid(np.dot(current_input, weights['W_o']) + np.dot(prev_hidden_state, weights['U_o']))
    new_hidden_state = output_gate * tanh(new_cell_state)
    
    return new_hidden_state, new_cell_state
```

---

## 4. PyTorch Example (Production Grade)
*Implementing a Multivariate Time-Series Forecaster using PyTorch `nn.LSTM`.*

```python
import torch
import torch.nn as nn

class TimeSeriesLSTM(nn.Module):
    def __init__(self, num_features, hidden_size, num_layers, output_dim, dropout=0.2):
        super(TimeSeriesLSTM, self).__init__()
        
        # In time-series, num_features is the number of variables (e.g., Temperature, Sales, Price)
        self.lstm = nn.LSTM(
            input_size=num_features,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0
        )
        
        # Regression head
        self.fc = nn.Linear(hidden_size, output_dim)
        
    def forward(self, x):
        # x shape: [batch_size, sequence_length, num_features]
        
        # LSTM returns:
        # out: hidden states for every time step
        # (h_n, c_n): the final hidden state and final cell state
        out, (h_n, c_n) = self.lstm(x)
        
        # Extract the hidden state from the last layer (h_n shape is [num_layers, batch, hidden_size])
        final_hidden = h_n[-1, :, :]
        
        # Predict the next value in the series (Regression)
        prediction = self.fc(final_hidden)
        return prediction
```

---

## 5. Business Use Case
**Energy Consumption Forecasting (Smart Grid)**
A utility company needs to predict city-wide electricity usage for the next 24 hours to scale power plant output. If they under-predict, rolling blackouts occur. If they over-predict, they burn millions of dollars of coal unnecessarily.

They train a **Multivariate LSTM**. The input sequences include past energy usage, but also *weather forecasts* (temperature, humidity) and *calendar events* (is tomorrow a holiday?). The LSTM learns the complex temporal relationships (e.g., if it's hot for 3 days straight, AC usage spikes non-linearly on day 4 as houses heat up). The model reduces forecasting error by 30% compared to standard ARIMA models, saving the grid $10M annually.

---

## 6. Mini Project: Retail Demand Forecasting (LSTM)
Run the accompanying script `demand_forecasting.py`.
This script builds a multivariate time-series pipeline:
1. It creates overlapping sliding windows of historical data.
2. It trains an LSTM to predict the next day's sales based on the past 14 days of history.

**To run:**
```bash
python demand_forecasting.py
```

---

## 7. Production Considerations
- **The Sliding Window Problem**: Time-series data is just a long list of numbers. PyTorch DataLoaders expect distinct "rows". You must write a function to chunk your time-series into overlapping windows (e.g., `Window 1 = Days 1-14, Target = Day 15`. `Window 2 = Days 2-15, Target = Day 16`).
- **Data Leakage (Lookahead Bias)**: The most common bug in financial/time-series ML. If your features for "Day 14" accidentally include the "Total Weekly Sales" which includes Day 15's data, your model will cheat. In production, it will fail because it doesn't have access to the future. Always split Train/Test chronologically (e.g., Train on 2022, Test on 2023). **Never use `train_test_split` with `shuffle=True` on time-series data!**

---

## 8. Common Failures
1. **Unscaled Targets**: LSTMs use `tanh` internally, which outputs values between -1 and 1. If you try to predict a house price of $500,000 without scaling it down, the gradients will explode and the model will fail instantly. You must scale your target variable (using `MinMaxScaler`), and then inverse-transform the predictions later.
2. **Batch Size vs Sequence Length Confusion**: Pay close attention to `batch_first=True`. If omitted, PyTorch expects the tensor shape to be `[sequence_length, batch_size, features]`, which is highly unintuitive and causes massive matrix shape errors.

---

## 9. Debugging Techniques
If your LSTM is predicting the exact same value (e.g., 0.5) for every single sequence:
1. Your target data isn't scaled, causing the gradients to explode and the weights to collapse.
2. Your learning rate is too high (Adam's default `1e-3` is often too high for complex LSTMs; try `1e-4`).
3. You forgot to apply `torch.nn.utils.clip_grad_norm_`.

---

## 10. Interview Questions

**Q1: How does an LSTM solve the Vanishing Gradient problem present in Vanilla RNNs?**
*Answer*: "LSTMs introduce a separate 'Cell State' alongside the hidden state. The cell state acts as a conveyor belt carrying long-term memory through the sequence. Because information is added or removed from the cell state using element-wise addition (via the Input and Forget gates) rather than repeated matrix multiplication, gradients can flow backwards through time without vanishing."

**Q2: You are building a stock price predictor. You use `train_test_split` to split your data 80/20. What catastrophic mistake did you just make?**
*Answer*: "By randomly splitting time-series data, I introduced Data Leakage (Lookahead Bias). The model is training on data from December, and testing on data from January of the same year. It 'knows' the future. Time-series data must be split chronologically: train on the first 80% of time, test on the strict final 20%."

**Q3: Explain the difference between Univariate and Multivariate time-series forecasting.**
*Answer*: "Univariate forecasting predicts future values based solely on the historical values of that exact same variable (e.g., predicting tomorrow's temperature based only on the past 10 days of temperatures). Multivariate uses multiple distinct variables (e.g., predicting temperature using past temperatures, humidity, wind speed, and cloud cover). LSTMs excel at multivariate forecasting."
