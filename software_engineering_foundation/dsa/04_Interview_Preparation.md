# Module 2.4: Interview Preparation (DSA)

Welcome to **Module 2.4**. As an AI Forward Deployed Engineer, you will face rigorous technical interviews. Companies like Palantir, Scale AI, and Databricks will test your coding ability to ensure you can build highly optimized, production-grade logic. You must master algorithmic problem-solving.

---

## 1. Detailed Theory

### The Blind 75 / NeetCode 150
You do not need to memorize 1,000 LeetCode problems. You need to understand the *patterns* behind the top 75 most frequently asked questions (originally curated by a Facebook engineer, known as the "Blind 75").

### Core LeetCode Patterns
Instead of memorizing solutions, memorize these patterns:
1. **Two Pointers**: Used for sorted arrays or strings to find pairs or subsets in O(N) time.
2. **Sliding Window**: Used to find subarrays or substrings that satisfy a condition (e.g., longest substring without repeating characters).
3. **Fast & Slow Pointers (Floyd's Cycle)**: Used in Linked Lists to detect cycles (e.g., does this list loop infinitely?).
4. **Breadth-First Search (BFS) / Depth-First Search (DFS)**: Used for traversing Trees and Graphs (e.g., finding the shortest path out of a maze).
5. **Top 'K' Elements**: Using a Heap (Priority Queue) to find the largest/smallest K elements in an array.

### The Problem Solving Framework
When given a problem in an interview, **DO NOT START CODING IMMEDIATELY**.
1. **Clarify**: Ask clarifying questions. (e.g., "Can the array contain negative numbers?", "Is the array sorted?").
2. **Edge Cases**: Discuss what happens if the input is empty or invalid.
3. **Brute Force**: Verbally explain the naive O(N²) solution.
4. **Optimize**: Discuss how to use a Hash Map or Two Pointers to drop the time to O(N).
5. **Code**: Write the optimized solution cleanly.
6. **Dry Run**: Trace through your code using a small example input.

---

## 2. Architecture Diagram: The Sliding Window Pattern

```mermaid
sequenceDiagram
    participant Window
    participant Array [2, 1, 5, 1, 3, 2]
    
    Note over Window, Array: Target: Find max sum of subarray size 3
    Window->>Array: [2, 1, 5] -> Sum: 8
    Window->>Array: Slide right -> subtract 2, add 1
    Window->>Array: [1, 5, 1] -> Sum: 7
    Window->>Array: Slide right -> subtract 1, add 3
    Window->>Array: [5, 1, 3] -> Sum: 9 (MAX!)
```
*(By subtracting the left element and adding the right element, you avoid re-summing the whole window, dropping time complexity from O(N*K) to O(N)).*

---

## 3. Production Use Cases (Applied LeetCode)

1. **Sliding Window in Rate Limiting**: You need to ensure a specific API key doesn't make more than 10 requests per minute. You maintain a sliding window (using a Queue/Deque in Redis) of timestamps for that API key.
2. **Two Pointers in Data Scrubbing**: You have an array of text tokens and need to remove all PII (Personally Identifiable Information) in-place without allocating a new array (to save RAM on a 10GB dataset). Two pointers allow you to overwrite the array in O(N) time and O(1) space.

---

## 4. Coding Examples

### The Two Pointers Pattern (Valid Palindrome)
```python
def is_palindrome(s: str) -> bool:
    # 1. Clean the string (alphanumeric only, lowercase)
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    
    # 2. Use Two Pointers
    left = 0
    right = len(cleaned) - 1
    
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1
        
    return True

print(is_palindrome("A man, a plan, a canal: Panama")) # True
```

### The Top 'K' Elements Pattern (Heap)
```python
import heapq

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    # 1. Count frequencies using a Hash Map
    count = {}
    for num in nums:
        count[num] = count.get(num, 0) + 1
        
    # 2. Use a Heap to find the top K
    # heapq in Python is a Min-Heap. We push tuples of (frequency, num)
    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        # If heap grows larger than K, pop the smallest frequency
        if len(heap) > k:
            heapq.heappop(heap)
            
    # 3. Extract results from heap
    return [item[1] for item in heap]

print(top_k_frequent([1,1,1,2,2,3], 2)) # Output: [1, 2]
```

---

## 5. Hands-on Labs

**Lab: Identify the Pattern**
**Objective**: Learn to map a problem description to a DSA pattern.
Read the following problem descriptions and write down which pattern you would use:
1. "Given an array of integers, find the contiguous subarray (containing at least one number) which has the largest sum."
2. "Given a string, find the length of the longest substring without repeating characters."
3. "Merge K sorted linked lists into one sorted linked list."

*Answers:*
1. Dynamic Programming (Kadane's Algorithm).
2. Sliding Window (with a Set to track duplicates).
3. Heap (Priority Queue to constantly pull the smallest current node from the K lists).

---

## 6. Assignments

**Assignment: Implement the Sliding Window**
Given an array of positive integers `nums` and a positive integer `target`, return the *minimal length* of a contiguous subarray whose sum is greater than or equal to `target`. If there is no such subarray, return 0 instead.
Example: `target = 7, nums = [2,3,1,2,4,3]`. Output: `2` (The subarray `[4,3]` has the minimal length).
*Task*: Implement this in Python in O(N) time using two pointers (`left` and `right`) to represent a sliding window.

---

## 7. Interview Questions

1. **How do you handle a question where you have absolutely no idea what to do?**
   *Answer Hint: Communicate. Start with a naive Brute Force solution. Say, "The most obvious way is to use a nested loop, which is O(N²)." Often, verbalizing the brute force approach triggers a realization on how to optimize it. If you are still stuck, ask for a small hint. Silence is an automatic failure.*
2. **Why do interviewers ask these questions if we don't use them directly in React or FastAPI development?**
   *Answer Hint: They test raw problem-solving ability, grasp of computer science fundamentals (memory management, time complexity), and how you handle edge cases and debugging under pressure.*

---

## 8. Best Practices (FDE Standards)

- **Think out loud**: In an interview, your thought process is more important than the final code. If you silently stare at the screen for 10 minutes and then write a perfect solution, you will likely fail the interview. The interviewer wants to know what it is like to pair-program with you.
- **Master Python's standard library**: Know `collections.deque`, `collections.defaultdict`, `collections.Counter`, and `heapq`. They are built specifically to solve LeetCode problems in half the lines of code.

---

## 9. Common Mistakes

- **Jumping to code too early**: Writing code before fully understanding the edge cases. You will inevitably write 20 lines of code, realize a flaw in your logic, and have to delete everything while panicking as the clock ticks down.
- **Ignoring Space Complexity**: Being so focused on getting an O(N) Time solution that you create 5 massive arrays inside your function, causing an O(N) or O(N²) Space Complexity, which the interviewer will immediately call out.
