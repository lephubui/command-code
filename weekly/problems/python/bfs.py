# Implement breadth-first search (BFS) algorithm
# Problem: Given a graph represented as an adjacency list and a starting node, 
# perform a breadth-first search (BFS) and return the list of nodes visited in the order they were visited.
# Example:
# Input: graph = {0: [1, 2], 1: [2], 2: [0, 3], 3: [3]}, start = 2
# Output: [2, 0, 3, 1]
# Explanation: Starting from node 2, we visit nodes in the order: 2 -> 0 -> 3 -> 1.
# Constraints:
# The graph may contain cycles.
from collections import deque

def bfs(graph, start):
    """Implement the BFS algorithm to traverse the graph starting from the start node."""
    visited = set()
    result = []
    queue = deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result

if __name__ == "__main__":
    graph = {
        0: [1, 2],
        1: [2],
        2: [0, 3],
        3: [3]
    }
    print(bfs(graph, 2))  # Output: [2, 0, 3, 1]
    print(bfs(graph, 0))  # Output: [0, 1, 2, 3]
    print(bfs(graph, 3))  # Output: [3]
    print(bfs(graph, 1))  # Output: [1, 2, 0, 3]