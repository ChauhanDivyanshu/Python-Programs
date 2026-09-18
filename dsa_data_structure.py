"""Practice-friendly implementations of common DSA data structures.

Run this file directly to see a small demonstration:
    python dsa_data_structures.py

The classes use Python's standard library where appropriate, while keeping the
underlying DSA operations visible for interview practice.
"""
from collections import deque
from heapq import heappop, heappush
from typing import Generic, Iterable, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    """LIFO stack with O(1) push, pop, peek, and is_empty operations."""

    def __init__(self, values: Iterable[T] = ()) -> None:
        self._items = list(values)

    def push(self, value: T) -> None:
        self._items.append(value)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> T:
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)


class Queue(Generic[T]):
    """FIFO queue backed by deque; enqueue and dequeue are O(1)."""

    def __init__(self, values: Iterable[T] = ()) -> None:
        self._items = deque(values)

    def enqueue(self, value: T) -> None:
        self._items.append(value)

    def dequeue(self) -> T:
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def front(self) -> T:
        if not self._items:
            raise IndexError("front from empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)


class MinHeap:
    """Min-heap wrapper demonstrating insert, minimum, and remove-min."""

    def __init__(self, values: Iterable[int] = ()) -> None:
        self._heap = list(values)
        # heapify changes the list in-place in O(n).
        from heapq import heapify
        heapify(self._heap)

    def push(self, value: int) -> None:
        heappush(self._heap, value)

    def pop_min(self) -> int:
        if not self._heap:
            raise IndexError("pop from empty heap")
        return heappop(self._heap)

    def peek_min(self) -> int:
        if not self._heap:
            raise IndexError("peek from empty heap")
        return self._heap[0]

    def __len__(self) -> int:
        return len(self._heap)


class Graph:
    """Undirected graph with BFS and DFS traversal methods."""

    def __init__(self) -> None:
        self._adjacency: dict[T, list[T]] = {}

    def add_vertex(self, vertex: T) -> None:
        self._adjacency.setdefault(vertex, [])

    def add_edge(self, first: T, second: T) -> None:
        self.add_vertex(first)
        self.add_vertex(second)
        if second not in self._adjacency[first]:
            self._adjacency[first].append(second)
        if first not in self._adjacency[second]:
            self._adjacency[second].append(first)

    def bfs(self, start: T) -> list[T]:
        """Visit reachable vertices level by level in O(V + E)."""
        if start not in self._adjacency:
            return []
        visited = {start}
        order: list[T] = []
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            order.append(vertex)
            for neighbour in self._adjacency[vertex]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        return order

    def dfs(self, start: T) -> list[T]:
        """Visit reachable vertices depth first in O(V + E)."""
        if start not in self._adjacency:
            return []
        visited: set[T] = set()
        order: list[T] = []
        stack = [start]
        while stack:
            vertex = stack.pop()
            if vertex in visited:
                continue
            visited.add(vertex)
            order.append(vertex)
            # Reverse keeps insertion order predictable in the iterative DFS.
            stack.extend(reversed(self._adjacency[vertex]))
        return order


if __name__ == "__main__":
    stack = Stack([10, 20])
    stack.push(30)
    assert stack.pop() == 30 and stack.peek() == 20

    queue = Queue(["A", "B"])
    queue.enqueue("C")
    assert queue.dequeue() == "A" and queue.front() == "B"

    heap = MinHeap([5, 1, 4, 2])
    assert [heap.pop_min() for _ in range(len(heap))] == [1, 2, 4, 5]

    graph = Graph()
    for edge in (("A", "B"), ("A", "C"), ("B", "D"), ("C", "E")):
        graph.add_edge(*edge)
    assert graph.bfs("A") == ["A", "B", "C", "D", "E"]
    assert graph.dfs("A") == ["A", "B", "D", "C", "E"]

    print("Stack, queue, min-heap, BFS, and DFS demos passed.")
