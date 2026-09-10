# Python Programs

Basic Python practice programs plus a curated, interview-ready **FAANG DSA question bank**.

## FAANG DSA solutions

`faang_dsa_solutions.py` contains clean Python implementations of the most frequently tested patterns. Every solution has a docstring with the expected time and space complexity, and the module has no input prompts when imported.

### Problems covered

| Topic | Questions / functions |
|---|---|
| Arrays and hashing | Two Sum, Best Time to Buy/Sell Stock, Product of Array Except Self, Maximum Subarray (Kadane), Longest Consecutive Sequence, Group Anagrams, Top K Frequent Elements |
| Two pointers and sliding window | Valid Palindrome, 3Sum, Longest Substring Without Repeating Characters, Longest Repeating Character Replacement, Minimum Window Substring, Trapping Rain Water |
| Intervals and matrices | Merge Intervals, Rotate Matrix |

| Stack | Valid Parentheses, Daily Temperatures (monotonic stack) |
| Binary search | Binary Search, Search in Rotated Sorted Array, Search a 2-D Matrix |
| Linked list | Reverse Linked List, Linked List Cycle, Merge Two Sorted Lists |
| Trees | Maximum Depth, Binary Tree Level Order Traversal, Lowest Common Ancestor |
| Graphs and grids | Number of Islands, Course Schedule / topological sort |
| Heap | Kth Largest Element |
| Backtracking | Subsets, Combination Sum |
| Dynamic programming and greedy | Climbing Stairs, Coin Change, Word Break, Longest Common Subsequence, House Robber, Jump Game, Edit Distance |

These cover the reusable patterns interviewers look for: hash maps, prefix/suffix products, greedy scans, sorting plus two pointers, sliding windows, monotonic stacks, binary search, fast/slow pointers, BFS/DFS, topological sorting, heaps, backtracking, and 1-D/2-D DP.

## How to run

```bash
python faang_dsa_solutions.py
```

The command runs a few smoke tests. To use any solution in another program:

```python
from faang_dsa_solutions import two_sum, coin_change

print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
print(coin_change([1, 2, 5], 11))   # 3
```

## Interview preparation order

1. Arrays, strings, hash maps, and Big-O.
2. Two pointers, sliding window, stack, and binary search.
3. Linked lists, trees, BFS/DFS, and graphs.
4. Heaps, intervals, and backtracking.
5. Dynamic programming; first write the recurrence, then optimize memory.

For each problem, first explain the brute-force idea, then the optimized pattern, edge cases, complexity, and a small dry run. The functions here intentionally mutate only where stated: `three_sum` sorts its input and `num_islands` marks visited land as `"0"`.

The original beginner exercises (`Program1.py` through `Program9.py` and `Even-or-odd.py`) are retained unchanged.
