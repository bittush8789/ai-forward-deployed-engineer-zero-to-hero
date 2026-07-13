# Module 16: Type Hinting for AI FDEs

Welcome to **Module 16**. Python is dynamically typed, which is great for quick scripts but terrible for million-line enterprise applications. If an AI agent returns a dictionary, you need to know *exactly* what keys are in that dictionary without running the code. Type Hinting (and static analysis tools like `mypy`) solves this, providing autocomplete and catching bugs before the code ever runs.

---

## 1. Detailed Theory

### Type Annotations
Introduced in Python 3.5, they allow you to declare the expected types of variables, function arguments, and return values.
- `def process(text: str) -> list[str]:`
- Note: Python does *not* enforce these at runtime. They are hints for your IDE (VSCode/PyCharm) and static analysis tools.

### Advanced Types (`typing` module)
- **`Optional[str]`**: Means the value can be a string OR `None`. (In Python 3.10+, you write `str | None`).
- **`Any`**: Opt-out of type checking. (Avoid this!).
- **`Callable`**: A function passed as an argument.
- **`Dict[str, Any]`**: A dictionary with string keys and any value.

### Dataclasses
Introduced in Python 3.7 (`@dataclass`). A decorator that automatically generates boilerplate code like `__init__`, `__repr__`, and `__eq__` for classes that primarily store data.

### Pydantic Models
Similar to Dataclasses, but heavily focused on **Runtime Validation**. If you say `age: int` and pass `"25"`, Pydantic will cast it to an integer. If you pass `"twenty"`, it throws a ValidationError. Essential for AI structured outputs.

---

## 2. Architecture Diagram: The Type Safety Net

```mermaid
graph TD
    A[Raw AI JSON Output] -->|Unsafe dict| B{Pydantic Model Validation}
    
    B -->|Fails Validation| C[Raise ValidationError (Triggers LLM Retry)]
    B -->|Passes Validation| D[Strictly Typed Python Object]
    
    D --> E(Python Logic: Autocomplete works!)
    D --> F(Mypy: Static checks pass!)
    
    style B fill:#f9f,stroke:#333
    style C fill:#ffcccc,stroke:#333
    style D fill:#d5e8d4,stroke:#333
```

---

## 3. Production Use Cases

1. **LLM Structured Output**: When asking OpenAI to return JSON, passing that JSON directly into a Pydantic Model. If the LLM hallucinates a field, Pydantic catches it immediately so your downstream logic doesn't crash with a `KeyError`.
2. **FastAPI Endpoints**: FastAPI uses Type Hints to automatically generate Swagger documentation and validate incoming HTTP request payloads.
3. **Refactoring**: In a massive 100,000-line codebase, if you change a function signature from `def fetch(id: str)` to `def fetch(id: int)`, running `mypy` will instantly list every single place in the codebase you forgot to update.

---

## 4. Real Company Examples

- **Dropbox**: Started as a massive, untyped Python monolith. They created `mypy` (the static type checker) specifically to gradually add types to millions of lines of code because it became unmaintainable.
- **Microsoft**: Pushes heavily for strict typing in Python via their Pyright/Pylance engine in VSCode, which is now the industry standard for AI developers.

---

## 5. Coding Examples

### Basic Type Annotations
```python
# Modern Python 3.10+ Syntax
def get_user_metadata(user_id: int, include_history: bool = False) -> dict[str, str | int]:
    # Returns a dict with string keys, and values that are either strings or ints
    return {"name": "Alice", "tokens": 150}

# Your IDE will now warn you if you do this:
# get_user_metadata("user_123") # WARNING: Expected int, got str
```

### Dataclasses vs Pydantic

```python
from dataclasses import dataclass
from pydantic import BaseModel, field_validator

# 1. Dataclass: Great for internal state, no runtime validation
@dataclass
class InternalState:
    session_id: str
    active: bool

state = InternalState(session_id="123", active="Yes") 
# "Yes" is a string, not a boolean, but Dataclasses don't care at runtime!

# 2. Pydantic: Great for external/AI data, strict runtime validation
class AgentResponse(BaseModel):
    tool_name: str
    confidence: float
    
    @field_validator('confidence')
    def check_confidence(cls, v):
        if not (0.0 <= v <= 1.0):
            raise ValueError('Confidence must be between 0 and 1')
        return v

# valid_response = AgentResponse(tool_name="Search", confidence=0.9)
# invalid_response = AgentResponse(tool_name="Search", confidence="high") # THROWS ERROR!
```

---

## 6. Hands-on Labs

**Lab: The Strict Agent Tool**
**Objective**: Use Pydantic to validate tool inputs.
*Pre-requisite: `pip install pydantic`*
**Instructions**:
1. Create a `class EmailToolInput(BaseModel):`.
2. Add `email: str` and `subject: str`.
3. Import `EmailStr` from `pydantic` and change `email: str` to `email: EmailStr`.
4. Try to instantiate `EmailToolInput(email="not_an_email", subject="Hi")`.
5. Observe the beautiful runtime validation error Pydantic gives you!

---

## 7. Assignments

**Assignment: Typing an old script**
Take this old, un-typed script and add strict Python 3.10+ type hints to everything.
```python
# BEFORE
def analyze(data, threshold):
    results = []
    for item in data:
        if item['score'] > threshold:
            results.append(item['id'])
    return results

# AFTER (Your Task)
# Hint: data should be a list of dicts. results should be a list of strings or ints.
```

---

## 8. Interview Questions

1. **Does Python enforce type hints at runtime?**
   *Answer Hint: No. Python remains dynamically typed. Type hints are ignored by the Python interpreter. They are used by external tools like `mypy` for static analysis, and by libraries like `pydantic` or `fastapi` which inspect the hints via the `typing` module to perform their own runtime validation.*
2. **What is the difference between `@dataclass` and `pydantic.BaseModel`?**
   *Answer Hint: Dataclasses are built into Python, generate boilerplate (`__init__`), and do not validate types at runtime. Pydantic is an external library that actively parses, coerces, and validates data at runtime based on the type hints.*
3. **What does the `Any` type do, and why should you avoid it?**
   *Answer Hint: `Any` turns off type checking for that variable. It defeats the entire purpose of type hinting. It should only be used when dealing with wildly unpredictable third-party legacy APIs.*

---

## 9. Best Practices (FDE Standards)

- **Use Mypy in CI/CD**: Type hints are useless if nobody checks them. Configure a GitHub action to run `mypy . --strict` on your codebase on every PR.
- **Type Hint all function signatures**: In an enterprise codebase, every single `def` must have argument types and a return type. If a function returns nothing, explicitly state `-> None:`.
- **Prefer modern syntax**: Instead of `from typing import List, Optional, Union`, use Python 3.10+ syntax: `list[str]`, `str | None`, `str | int`.

---

## 10. Common Mistakes

- **Mutating arguments with type hints**: 
  ```python
  def process(items: list = []) -> None: # BAD
  ```
  Type hinting doesn't solve the mutable default argument bug! Still use `items: list | None = None`.
- **Forgetting that Dicts have two types**: `data: dict` is bad. `data: dict[str, Any]` is better. `data: dict[str, int]` is perfect.

---

## 11. End-to-End Project: LLM Structured Output Parser

**Scenario**: You are interacting with an LLM that is instructed to return JSON. You must parse this JSON safely into a Pydantic model so the rest of your application can rely on autocomplete and type safety.

**Code:**
```python
import json
from pydantic import BaseModel, ValidationError, Field

# 1. Define the strict schema we expect from the LLM
class SentimentAnalysisResult(BaseModel):
    sentiment: str = Field(..., pattern="^(Positive|Negative|Neutral)$")
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    keywords: list[str] = Field(default_factory=list, max_length=5)

def parse_llm_output(raw_json_string: str) -> SentimentAnalysisResult | None:
    try:
        # 1. Parse string to Python dictionary
        data_dict = json.loads(raw_json_string)
        
        # 2. Validate dictionary via Pydantic
        # If the LLM returned "confidence_score": "high", this will throw a ValidationError!
        validated_data = SentimentAnalysisResult(**data_dict)
        
        print("[SUCCESS] Data parsed and validated.")
        return validated_data
        
    except json.JSONDecodeError:
        print("[ERROR] LLM did not return valid JSON syntax.")
        return None
    except ValidationError as e:
        print("[ERROR] LLM JSON structure is invalid according to schema:")
        print(e.json())
        return None

def main():
    # Mocking LLM outputs
    
    # Happy Path
    good_llm_output = '{"sentiment": "Positive", "confidence_score": 0.95, "keywords": ["fast", "clean"]}'
    
    # Bad Path (Hallucinated schema)
    bad_llm_output = '{"sentiment": "Happy", "confidence_score": "very high", "keywords": []}'
    
    print("--- Parsing Good Output ---")
    result = parse_llm_output(good_llm_output)
    if result:
        # Now we get IDE autocomplete for result.sentiment!
        print(f"Sentiment: {result.sentiment}")
        
    print("\n--- Parsing Bad Output ---")
    parse_llm_output(bad_llm_output)

if __name__ == "__main__":
    main()
```
