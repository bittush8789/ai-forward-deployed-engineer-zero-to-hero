# Module 3: Functions for AI Forward Deployed Engineers

Welcome to **Module 3**. Functions are the core of reusable code. In AI engineering, functions allow you to wrap API calls, parse responses, and build modular pipelines that can be tested independently.

---

## 1. Detailed Theory

### Functions, Parameters, and Return Values
Functions are defined using `def`. They take inputs (parameters) and optionally return an output (return values). Functions should ideally do **one thing well** (Single Responsibility Principle).

### Lambda Functions
Anonymous, one-line functions defined using the `lambda` keyword. Often used for short callbacks or sorting logic.

### `*args` and `**kwargs`
- `*args`: Collects positional arguments into a tuple. Useful when you don't know how many arguments will be passed.
- `**kwargs`: Collects keyword arguments into a dictionary. Highly useful for passing arbitrary configuration settings to underlying AI models.

### Recursion
A function calling itself. While elegant for tree traversals (like traversing a JSON response or DOM tree), Python has a recursion limit (default 1000) and lacks tail-call optimization.

### Decorators
Decorators (`@decorator_name`) are functions that wrap other functions to modify their behavior without changing their source code. They are ubiquitous in backend frameworks (like FastAPI) and AI tooling (like caching LLM responses or adding retry logic).

---

## 2. Architecture Diagram: The Decorator Pattern

How decorators wrap a core function to add pre/post-processing logic (like timing or retrying).

```mermaid
graph TD
    A[Call: get_llm_response()] --> B(Retry Decorator)
    B --> C(Timing Decorator)
    C --> D[Actual LLM API Call]
    D --> C
    C --> B
    B --> E[Return Final Result]
    
    style D fill:#f96,stroke:#333,stroke-width:2px
```

---

## 3. Production Use Cases

1. **`**kwargs` for Model Parameters**: Wrapping an OpenAI API call where users might want to pass arbitrary parameters (`temperature`, `top_p`, `frequency_penalty`) without hardcoding every single one in the function signature.
2. **Retry Decorator**: Wrapping flaky API calls (like scraping or LLM generation) with a `@retry(max_attempts=3)` decorator to automatically handle transient failures.
3. **Lambda for Sorting**: Sorting a list of AI-generated responses based on their `confidence_score` extracted from the JSON.

---

## 4. Real Company Examples

- **LangChain / LlamaIndex**: Both frameworks heavily use `**kwargs` in their base LLM classes to pass provider-specific arguments down the stack transparently.
- **Palantir**: Uses decorators extensively to enforce Access Control (e.g., `@requires_permission('read_sensitive_data')`) on functions that fetch data for analytics.

---

## 5. Coding Examples

### Using `**kwargs` for AI Configuration
```python
def generate_text(prompt, model="gpt-4", **kwargs):
    # kwargs is a dictionary of extra parameters
    api_payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    # Update payload with any extra parameters provided (e.g., temperature)
    api_payload.update(kwargs)
    
    print(f"Sending payload: {api_payload}")
    return "Mock Response"

# Passing arbitrary arguments!
generate_text("Hello", temperature=0.7, max_tokens=150, user="usr_123")
```

### A Practical Retry Decorator
```python
import time
from functools import wraps

def retry_api(retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt == retries:
                        print("Max retries reached. Raising error.")
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

@retry_api(retries=2, delay=2)
def unstable_external_api():
    print("Calling API...")
    raise ConnectionError("Timeout!")

# unstable_external_api() # Uncomment to see the retry in action
```

---

## 6. Hands-on Labs

**Lab: The Lambda Sorter**
**Objective**: Sort AI search results.
**Instructions**:
1. You have a list of dictionaries:
   `results = [{"doc": "A", "score": 0.8}, {"doc": "B", "score": 0.95}, {"doc": "C", "score": 0.4}]`
2. Use Python's built-in `sorted()` function combined with a `lambda` function to sort the list in descending order based on the "score" key.
3. Print the top document.

---

## 7. Assignments

**Assignment: The Timing Decorator**
Create a decorator called `@timer` that measures the execution time of a function.
1. Use the `time.time()` module.
2. The decorator should print `"Function <func_name> took <time> seconds to execute."`
3. Apply it to a function that uses a `time.sleep(1)` to simulate a long-running LLM query.

---

## 8. Interview Questions

1. **What is the difference between `*args` and `**kwargs`?**
   *Answer Hint: `*args` takes positional arguments as a tuple, `**kwargs` takes named arguments as a dictionary.*
2. **Why do we use `@wraps(func)` from `functools` inside a decorator?**
   *Answer Hint: It preserves the original function's metadata (name, docstring). Without it, debugging becomes a nightmare because all decorated functions appear as the `wrapper` function in stack traces.*
3. **Can a function return another function in Python?**
   *Answer Hint: Yes, Python treats functions as First-Class Citizens. This is the core mechanism that makes decorators possible.*

---

## 9. Best Practices (FDE Standards)

- **Type Hinting (Preview)**: Always type hint function arguments and return types. `def get_user(id: int) -> dict:` (Covered deeply in Module 16).
- **Don't use mutable default arguments**:
  *Bad:* `def add_item(item, my_list=[]):` -> `my_list` is shared across all function calls!
  *Good:* `def add_item(item, my_list=None): if my_list is None: my_list = []`
- **Docstrings**: Every production function must have a docstring (Google or Sphinx style) explaining arguments, return values, and exceptions raised.

---

## 10. Common Mistakes

- **Forgetting to return a value**: If you don't explicitly `return` in Python, the function returns `None`.
- **Misunderstanding Scope**: Modifying a global variable inside a function without the `global` keyword will create a new local variable instead, leading to bugs.

---

## 11. End-to-End Project: Modular AI Text Processing Pipeline

**Scenario**: Build a text processing pipeline that cleans data before sending it to a model. The pipeline must be extensible.

**Code:**
```python
# 1. Base processing functions
def remove_whitespace(text):
    return text.strip()

def to_lowercase(text):
    return text.lower()

def remove_special_chars(text):
    import re
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

# 2. Pipeline engine utilizing *args
def process_text_pipeline(text, *functions):
    """
    Runs a piece of text through a variable number of processing functions.
    """
    current_text = text
    for func in functions:
        current_text = func(current_text)
    return current_text

# 3. Execution
def main():
    raw_document = "   BREAKING: AI Models are getting SMARTER! @2023...   "
    
    # We can pass as many functions as we want via *args
    cleaned_doc = process_text_pipeline(
        raw_document, 
        remove_whitespace, 
        to_lowercase, 
        remove_special_chars
    )
    
    print(f"Original: '{raw_document}'")
    print(f"Cleaned : '{cleaned_doc}'")

if __name__ == "__main__":
    main()
```
