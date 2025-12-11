# Implement a deepth-first search (DFS) algorithm
# Problem: Given a graph represented as an adjacency list and a starting node, perform a depth-first search (DFS) and return the list of nodes visited in the order they were visited.
# Example:
# Input: graph = {0: [1, 2], 1: [2], 2: [0, 3], 3: [3]}, start = 2
# Output: [2, 0, 1, 3]
# Explanation: Starting from node 2, we visit nodes in the order: 2 -> 0 -> 1 -> 3.
# Constraints:
# The graph may contain cycles.

from unittest import result

def dfs(graph, start, visited=None, result=None):
    """Implement the DFS algorithm to traverse the graph starting from the start node."""
    if visited is None:
        visited = set()
        result = []

    visited.add(start)
    result.append(start)

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited, result)
    
    return result

if __name__ == "__main__":
    graph = {
        0: [1, 2],
        1: [2],
        2: [0, 3],
        3: [3]
    }
    print(dfs(graph, 2))  # Output: [2, 0, 1, 3]
    print(dfs(graph, 0))  # Output: [0, 1, 2, 3]
    print(dfs(graph, 3))  # Output: [3]
    print(dfs(graph, 1))  # Output: [1, 2, 0, 3]