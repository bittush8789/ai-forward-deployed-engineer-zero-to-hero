# DSA Capstone Project: Workflow Execution Engine

**Difficulty:** ⭐⭐⭐⭐
**Estimated Time:** 8-12 Hours
**Primary Tech Stack:** Core Python (No external frameworks)

---

## 1. Project Overview

You are deployed to a startup building a competitor to LangGraph. They need you to write the core Data Structures and Algorithms for the multi-agent orchestration engine. You must build a system capable of registering nodes (Agents), defining edges (Routing), detecting infinite loops (Cycle Detection), and executing the workflow using Graph Traversal algorithms.

## 2. Requirements

1. **The Graph Structure**: Build a `WorkflowGraph` class that uses an Adjacency List to store nodes and edges.
2. **Cycle Detection**: Implement a Depth-First Search (DFS) algorithm that runs *before* execution to ensure the user hasn't created a graph that is mathematically guaranteed to loop infinitely without an exit condition.
3. **Execution Engine**: Implement a Breadth-First Search (BFS) or iterative routing loop to pass a `State` object through the graph from the `START` node to the `END` node.
4. **Conditional Edges**: Allow edges to have a "condition" function. (e.g., Node A goes to Node B *if* `state["score"] > 0.8`, else it goes to Node C).

## 3. Architecture Specifications

- **Node Class**: Represents an agent. Takes a function that mutates a state dictionary.
- **Edge Class**: Connects two Nodes. Can optionally take a `condition_callable`.
- **State**: A simple Python dictionary `{"messages": [], "metadata": {}}`.

## 4. Tasks to Complete

1. **Build the Classes**: Implement `Node`, `Edge`, and `WorkflowGraph`.
2. **Implement Cycle Detection**: Write `def validate_dag(self) -> bool:`. It must return `False` if a cycle is found in standard (non-conditional) edges.
3. **Implement the Runner**: Write `def invoke(self, initial_state: dict) -> dict:`. This function manages the `while` loop, executing nodes and evaluating conditional edges to find the next node.
4. **The Infinite Loop Guard**: Inside `invoke`, implement a Hash Set that tracks visited states or a `max_steps` counter to forcefully terminate the execution if an agent gets stuck in a loop during runtime.

## 5. Submission Checklist
- [ ] Core OOP implementation of the Graph.
- [ ] Unit tests proving the Cycle Detection algorithm catches `A -> B -> A`.
- [ ] A mock test run simulating an AI workflow (e.g., Triage -> TechSupport -> Escalation -> End) successfully mutating the state at each step.
- [ ] Code is strictly typed using Python type hints (`typing.Callable`, `typing.Dict`).
