# Practice Tasks: Module 3 - Weaviate Hybrid Search

## Task 1: Run the Weaviate Hybrid Search Lab
**Goal**: Observe how BM25 and vector search results are merged using RRF.

### Step-by-Step
1. Run the Weaviate hybrid search lab:
   ```bash
   python3 d:/ai-forward-deployed-engineer-zero-to-hero/vector_databases/labs/weaviate_hybrid.py
   ```
2. Verify the output shows:
   - Separate BM25 top result and dense vector top result
   - RRF merged final ranking

---

## Task 2: Change Alpha and Compare Results
**Goal**: Understand the effect of the alpha parameter on hybrid search rankings.

### Step-by-Step
1. Modify the `alpha` variable in the lab script to `0.0` (BM25 only) and observe rankings.
2. Change to `1.0` (vector only) and compare.
3. Document which alpha gives better results for the test query.

---

## Task 3: Interview Scenario Practice
1. Explain the RRF formula: `score = 1 / (60 + rank)`. Why is 60 used?
2. What does alpha=0 vs alpha=1 mean in Weaviate Hybrid Search?
3. How do you enable multi-tenancy in Weaviate?
