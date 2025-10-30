# You are provided with a list of integers, and your task is to define a function named solution that takes this list as input and returns another list. 
# The returned list should contain the floor(k/3)-th smallest element for each prefix of the original list, prefix_numbers[0..k]
# For example, if the input list is [4, 1, 3, 5, 6, 2], the output should be [4, 1, 1, 3, 3, 2].
# This means:
# For the prefix [4], the floor(1/3) = 0-th smallest element is 4.
# For the prefix [4, 1], the floor(2/3) = 0-th smallest element is 1.
# For the prefix [4, 1, 3], the floor(3/3) = 1-th smallest element is 1.
# For the prefix [4, 1, 3, 5], the floor(4/3) = 1-th smallest element is 3.
# For the prefix [4, 1, 3, 5, 6], the floor(5/3) = 1-th smallest element is 3.
# For the prefix [4, 1, 3, 5, 6, 2], the floor(6/3) = 2-th smallest element is 2.
# Constraint: The input list will contain at least one integer and can contain both positive and negative integers.

import heapq

def solution(numbers):
    res = []
    min_heap = []
    max_heap = []

    for i, num in enumerate(numbers):
        if max_heap and num < -max_heap[0]:
            heapq.heappush(max_heap, -num)
        else:
            heapq.heappush(min_heap, num)
    
        # Calculate target size for max_heap
        target = (i + 1) // 3
        
        # Balance: move between heaps until max_heap has exactly 'target' elements
        while len(max_heap) > target:
            heapq.heappush(min_heap, -heapq.heappop(max_heap))
        while len(max_heap) < target:
            heapq.heappush(max_heap, -heapq.heappop(min_heap))
            
        # The answer for this prefix is min_heap[0]
        res.append(min_heap[0])
    
    return res

if __name__ == "__main__":
    # Test case 1: Original example
    numbers = [4, 1, 3, 5, 6, 2]
    result = solution(numbers)
    print(f"Test 1 - numbers: {numbers}")
    print(f"Output: {result}")  # Expected: [4, 1, 1, 3, 3, 2]
    print()
    
    # Test case 2: Single element
    numbers = [10]
    result = solution(numbers)
    print(f"Test 2 - numbers: {numbers}")
    print(f"Output: {result}")  # Expected: [10]
    print()
    
    # Test case 3: Negative numbers
    numbers = [-1, -3, -2, -5, -4]
    result = solution(numbers)
    print(f"Test 3 - numbers: {numbers}")
    print(f"Output: {result}")  # Expected: [-1, -3, -3, -3, -4]
    print()
    
    # Test case 4: Mixed positive and negative
    numbers = [3, -1, 2, -4, 5, 0]
    result = solution(numbers)
    print(f"Test 4 - numbers: {numbers}")
    print(f"Output: {result}")  # Expected: [3, -1, -1, -1, 0, 0]
    print()
    
    # Test case 5: All same elements
    numbers = [7, 7, 7, 7]
    result = solution(numbers)
    print(f"Test 5 - numbers: {numbers}")
    print(f"Output: {result}")  # Expected: [7, 7, 7, 7]

    # Test case 6: Unsorted elements
    numbers = [33, 11, 44, 22, 55, 77]
    result = solution(numbers)
    print(f"Test 6 - numbers: {numbers}")
    print(f"Output: {result}")  # Expected: [33, 11, 11, 22, 33, 44]