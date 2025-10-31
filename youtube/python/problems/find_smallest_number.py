# Finding Smallest Absolute Distance Between Added Numbers
# You are provided with a list of queries. Each query represents an operation in which integers are added to a list. 
# Your task is to implement a Python function, solution(), that processes these queries. 
# After each addition operation, the function returns the smallest absolute distance between any pair of added numbers. 
# If fewer than two numbers have been added, it should return -1.
# The function is defined as solution(queries), where queries is a list of integers to be added. 
# The function should return a list of integers, with each integer representing the smallest absolute distance after each operation.
# For example, given the input queries = [1, 5, 3, 19, 18], the output should be [-1, 4, 2, 2, 1].
# Explanation:
# After adding 1, there is only one number, so the output is -1.
# After adding 5, the numbers are [1, 5], and the smallest distance is |5 - 1| = 4.
# After adding 3, the numbers are [1, 3, 5], and the smallest distance is |3 - 1| = 2.
# After adding 19, the numbers are [1, 3, 5, 19], and the smallest distance remains 2 (between 3 and 5).
# After adding 18, the numbers are [1, 3, 5, 18, 19], and the smallest distance is |19 - 18| = 1.
# Constraints:
# The length of the queries list can be up to 10^5.
# The integers in the queries can range from -10^9 to 10^9.
# To efficiently find the smallest absolute distance between added numbers after each insertion, we can utilize the `SortedList` from the `sortedcontainers` module. 
# This data structure allows us to maintain a sorted list of numbers and perform binary search operations to find the closest neighbors of the newly added number in logarithmic time.

from sortedcontainers import SortedList


def solution(queries):
    result = []
    sorted_list = SortedList()
    distance_global = float('inf')
    
    for query in queries:
        if len(sorted_list) == 0: # Only one element
            result.append(-1)
            sorted_list.add(query)
            continue
        min_dist = float('inf')
        idx_1 = sorted_list.bisect_left(query)
        if idx_1 > 0:
            distance_before = abs(query - sorted_list[idx_1 - 1])
            min_dist = min(min_dist, distance_before)
        if idx_1 < len(sorted_list):
            distance_after  = abs(query - sorted_list[idx_1])
            min_dist = min(min_dist, distance_after)

        distance_global = min(distance_global, min_dist)

        result.append(distance_global)
        sorted_list.add(query)

    return result

if __name__ == "__main__":
    # Test case 1: Original example
    queries = [1, 5, 3, 19, 18]
    print(solution(queries))  # Expected output: [-1, 4, 2, 2, 1]

    # Test case 2: All elements are the same
    queries = [2, 2, 2, 2]
    print(solution(queries))  # Expected output: [-1, 0, 0, 0]

    # Test case 3: Increasing sequence
    queries = [1, 2, 3, 4, 5]
    print(solution(queries))  # Expected output: [-1, 1, 1, 1, 1]

    # Test case 4: Decreasing sequence
    queries = [5, 4, 3, 2, 1]
    print(solution(queries))  # Expected output: [-1, 1, 1, 1, 1]