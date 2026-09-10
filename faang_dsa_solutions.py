"""FAANG-style Python DSA interview solutions.

Each function is small, interview-ready, and side-effect free.  Run this file
with ``python faang_dsa_solutions.py`` for a tiny smoke test.  The examples in
this module use zero-based indexing and return an empty result when no answer
exists unless the function's docstring says otherwise.
"""
from collections import Counter, defaultdict, deque
from bisect import bisect_left
from heapq import heapify, heappop, heappush
from typing import Optional


# ---------- Arrays and hashing ----------
def two_sum(nums: list[int], target: int) -> list[int]:
    """Return indices of two values adding to target. O(n) time, O(n) space."""
    seen: dict[int, int] = {}
    for i, value in enumerate(nums):
        if target - value in seen:
            return [seen[target - value], i]
        seen[value] = i
    return []


def max_profit(prices: list[int]) -> int:
    """Best profit from one buy and one later sell. O(n) time, O(1) space."""
    best, lowest = 0, float("inf")
    for price in prices:
        lowest = min(lowest, price)
        best = max(best, price - lowest)
    return best


def product_except_self(nums: list[int]) -> list[int]:
    """Product of all values except self, without division. O(n), O(1) extra."""
    result = [1] * len(nums)
    prefix = 1
    for i, value in enumerate(nums):
        result[i] = prefix
        prefix *= value
    suffix = 1
    for i in range(len(nums) - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    return result


def max_subarray(nums: list[int]) -> int:
    """Kadane's algorithm: maximum contiguous-subarray sum. O(n), O(1)."""
    if not nums:
        return 0
    current = answer = nums[0]
    for value in nums[1:]:
        current = max(value, current + value)
        answer = max(answer, current)
    return answer


def longest_consecutive(nums: list[int]) -> int:
    """Length of the longest consecutive run. O(n) average time, O(n) space."""
    values = set(nums)
    longest = 0
    for value in values:
        if value - 1 not in values:
            length = 1
            while value + length in values:
                length += 1
            longest = max(longest, length)
    return longest


def group_anagrams(words: list[str]) -> list[list[str]]:
    """Group anagrams while preserving input order inside each group. O(n*k)."""
    groups: dict[tuple[int, ...], list[str]] = defaultdict(list)
    for word in words:
        key = tuple(sorted(Counter(word).items()))
        groups[key].append(word)
    return list(groups.values())


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """Return k most frequent values using bucket sort. O(n) time, O(n) space."""
    counts = Counter(nums)
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for value, count in counts.items():
        buckets[count].append(value)
    answer = []
    for bucket in reversed(buckets):
        answer.extend(bucket)
        if len(answer) >= k:
            return answer[:k]
    return answer


# ---------- Two pointers, sliding window, and intervals ----------
def is_palindrome(text: str) -> bool:
    """Check an alphanumeric palindrome, ignoring case. O(n) time, O(1) space."""
    left, right = 0, len(text) - 1
    while left < right:
        while left < right and not text[left].isalnum():
            left += 1
        while left < right and not text[right].isalnum():
            right -= 1
        if text[left].lower() != text[right].lower():
            return False
        left, right = left + 1, right - 1
    return True


def three_sum(nums: list[int]) -> list[list[int]]:
    """Unique triplets whose sum is zero. O(n^2) time, O(1) extra (excluding output)."""
    nums.sort()
    answer = []
    for i in range(len(nums) - 2):
        if i and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                answer.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return answer


def length_of_longest_substring(s: str) -> int:
    """Longest substring without repeated characters. O(n) time, O(n) space."""
    last: dict[str, int] = {}
    start = answer = 0
    for end, char in enumerate(s):
        if char in last and last[char] >= start:
            start = last[char] + 1
        last[char] = end
        answer = max(answer, end - start + 1)
    return answer


def character_replacement(s: str, k: int) -> int:
    """Longest same-letter window after at most k replacements. O(n), O(1)."""
    counts = Counter()
    left = best = 0
    for right, char in enumerate(s):
        counts[char] += 1
        while right - left + 1 - max(counts.values()) > k:
            counts[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Merge overlapping intervals. O(n log n) time, O(n) space."""
    if not intervals:
        return []
    intervals = sorted(intervals)
    merged = [intervals[0][:]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


def trap_rain_water(heights: list[int]) -> int:
    """Water trapped between bars using two pointers. O(n) time, O(1) space."""
    left, right = 0, len(heights) - 1
    left_max = right_max = answer = 0
    while left < right:
        if heights[left] <= heights[right]:
            left_max = max(left_max, heights[left])
            answer += left_max - heights[left]
            left += 1
        else:
            right_max = max(right_max, heights[right])
            answer += right_max - heights[right]
            right -= 1
    return answer


def min_window_substring(s: str, target: str) -> str:
    """Smallest window containing target's character counts. O(len(s))."""
    if not s or not target:
        return ""
    need = Counter(target)
    missing, left, best = len(target), 0, (float("inf"), 0, 0)
    for right, char in enumerate(s, 1):
        if need[char] > 0:
            missing -= 1
        need[char] -= 1
        while missing == 0:
            if right - left < best[0]:
                best = (right - left, left, right)
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return s[best[1]:best[2]] if best[0] != float("inf") else ""


def rotate_matrix(matrix: list[list[int]]) -> None:
    """Rotate an n-by-n matrix 90 degrees clockwise in place. O(n^2), O(1)."""
    n = len(matrix)
    for row in range(n):
        for col in range(row, n):
            matrix[row][col], matrix[col][row] = matrix[col][row], matrix[row][col]
    for row in matrix:
        row.reverse()


# ---------- Stack and binary search ----------
def valid_parentheses(s: str) -> bool:
    """Validate (), [], {} nesting. O(n) time, O(n) space."""
    pairs = {")": "(", "]": "[", "}": "{"
    }
    stack: list[str] = []
    for char in s:
        if char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
        else:
            stack.append(char)
    return not stack


def daily_temperatures(temperatures: list[int]) -> list[int]:
    """Days until a warmer temperature using a monotonic stack. O(n), O(n)."""
    answer = [0] * len(temperatures)
    stack: list[int] = []
    for i, temperature in enumerate(temperatures):
        while stack and temperature > temperatures[stack[-1]]:
            old = stack.pop()
            answer[old] = i - old
        stack.append(i)
    return answer


def binary_search(nums: list[int], target: int) -> int:
    """Index of target in sorted nums, or -1. O(log n) time, O(1) space."""
    left, right = 0, len(nums) - 1
    while left <= right:
        middle = (left + right) // 2
        if nums[middle] == target:
            return middle
        if nums[middle] < target:
            left = middle + 1
        else:
            right = middle - 1
    return -1


def search_rotated(nums: list[int], target: int) -> int:
    """Search a sorted array rotated once (distinct values). O(log n), O(1)."""
    left, right = 0, len(nums) - 1
    while left <= right:
        middle = (left + right) // 2
        if nums[middle] == target:
            return middle
        if nums[left] <= nums[middle]:
            if nums[left] <= target < nums[middle]:
                right = middle - 1
            else:
                left = middle + 1
        elif nums[middle] < target <= nums[right]:
            left = middle + 1
        else:
            right = middle - 1
    return -1


def search_matrix(matrix: list[list[int]], target: int) -> bool:
    """Search row/column sorted matrix from top-right. O(rows+cols), O(1)."""
    if not matrix or not matrix[0]:
        return False
    row, col = 0, len(matrix[0]) - 1
    while row < len(matrix) and col >= 0:
        if matrix[row][col] == target:
            return True
        if matrix[row][col] > target:
            col -= 1
        else:
            row += 1
    return False


# ---------- Linked lists ----------
class ListNode:
    def __init__(self, value: int = 0, next_node: Optional["ListNode"] = None):
        self.val, self.next = value, next_node


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverse a singly linked list in place. O(n) time, O(1) space."""
    previous = None
    while head:
        following = head.next
        head.next = previous
        previous, head = head, following
    return previous


def has_cycle(head: Optional[ListNode]) -> bool:
    """Floyd's tortoise-and-hare cycle detection. O(n) time, O(1) space."""
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False


def merge_two_lists(a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:
    """Merge two sorted linked lists. O(m+n) time, O(1) extra space."""
    dummy = ListNode()
    tail = dummy
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


# ---------- Trees, graphs, heaps, and backtracking ----------
class TreeNode:
    def __init__(self, value: int = 0, left: Optional["TreeNode"] = None,
                 right: Optional["TreeNode"] = None):
        self.val, self.left, self.right = value, left, right


def level_order(root: Optional[TreeNode]) -> list[list[int]]:
    """Binary-tree BFS by level. O(n) time and O(n) queue space."""
    if not root:
        return []
    answer, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        answer.append(level)
    return answer


def max_depth(root: Optional[TreeNode]) -> int:
    """Maximum binary-tree depth. O(n) time, O(h) recursion space."""
    return 0 if not root else 1 + max(max_depth(root.left), max_depth(root.right))


def lowest_common_ancestor(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """LCA in a binary tree (nodes are guaranteed to exist). O(n) time."""
    if not root or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    return root if left and right else left or right


def num_islands(grid: list[list[str]]) -> int:
    """Count connected groups of '1' cells. O(rows*cols) time and space."""
    if not grid:
        return 0
    rows, cols, count = len(grid), len(grid[0]), 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1":
                continue
            count += 1
            grid[r][c] = "0"
            queue = deque([(r, c)])
            while queue:
                x, y = queue.popleft()
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "1":
                        grid[nx][ny] = "0"
                        queue.append((nx, ny))
    return count


def course_schedule(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """Whether all courses can be completed (cycle detection via Kahn BFS)."""
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, prerequisite in prerequisites:
        graph[prerequisite].append(course)
        indegree[course] += 1
    queue = deque(i for i, degree in enumerate(indegree) if degree == 0)
    completed = 0
    while queue:
        course = queue.popleft()
        completed += 1
        for nxt in graph[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return completed == num_courses


def kth_largest(nums: list[int], k: int) -> int:
    """Kth largest value using a size-k min heap. O(n log k), O(k) space."""
    heap: list[int] = []
    for value in nums:
        heappush(heap, value)
        if len(heap) > k:
            heappop(heap)
    return heap[0]


def subsets(nums: list[int]) -> list[list[int]]:
    """Return all subsets by iterative expansion. O(n*2^n) output-sensitive."""
    answer = [[]]
    for value in nums:
        answer += [current + [value] for current in answer]
    return answer


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """Unique combinations; each candidate may be reused. Backtracking."""
    answer: list[list[int]] = []
    candidates = sorted(set(candidates))

    def backtrack(start: int, remaining: int, path: list[int]) -> None:
        if remaining == 0:
            answer.append(path[:])
            return
        for i in range(start, len(candidates)):
            value = candidates[i]
            if value > remaining:
                break
            path.append(value)
            backtrack(i, remaining - value, path)
            path.pop()

    backtrack(0, target, [])
    return answer


# ---------- Dynamic programming ----------
def climb_stairs(n: int) -> int:
    """Number of ways to climb 1 or 2 steps. O(n) time, O(1) space."""
    one, two = 1, 1
    for _ in range(n):
        one, two = two, one + two
    return one


def coin_change(coins: list[int], amount: int) -> int:
    """Fewest coins for amount, or -1 if impossible. O(amount*coins)."""
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for current in range(1, amount + 1):
        for coin in coins:
            if coin <= current:
                dp[current] = min(dp[current], dp[current - coin] + 1)
    return -1 if dp[amount] > amount else dp[amount]


def word_break(s: str, word_dict: list[str]) -> bool:
    """Whether s can be segmented into dictionary words. O(n^2) worst case."""
    words = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for end in range(1, len(s) + 1):
        dp[end] = any(dp[start] and s[start:end] in words for start in range(end))
    return dp[-1]


def longest_common_subsequence(a: str, b: str) -> int:
    """Length of LCS using two rows. O(len(a)*len(b)) time, O(min) space."""
    if len(a) < len(b):
        a, b = b, a
    previous = [0] * (len(b) + 1)
    for x in a:
        current = [0]
        for j, y in enumerate(b, 1):
            current.append(previous[j - 1] + 1 if x == y else max(previous[j], current[-1]))
        previous = current
    return previous[-1]


def house_robber(nums: list[int]) -> int:
    """Maximum non-adjacent sum. O(n) time and O(1) space."""
    robbed, skipped = 0, 0
    for money in nums:
        robbed, skipped = skipped + money, max(robbed, skipped)
    return max(robbed, skipped)


def jump_game(nums: list[int]) -> bool:
    """Whether the last index is reachable using a greedy farthest index. O(n)."""
    farthest = 0
    for i, jump in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + jump)
    return True


def edit_distance(a: str, b: str) -> int:
    """Minimum insert/delete/replace operations to change a into b. O(m*n)."""
    previous = list(range(len(b) + 1))
    for i, first in enumerate(a, 1):
        current = [i]
        for j, second in enumerate(b, 1):
            current.append(previous[j - 1] if first == second else 1 + min(previous[j], current[-1], previous[j - 1]))
        previous = current
    return previous[-1]


if __name__ == "__main__":
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert max_profit([7, 1, 5, 3, 6, 4]) == 5
    assert length_of_longest_substring("abcabcbb") == 3
    assert coin_change([1, 2, 5], 11) == 3
    print("Smoke tests passed: FAANG DSA solutions are ready.")
